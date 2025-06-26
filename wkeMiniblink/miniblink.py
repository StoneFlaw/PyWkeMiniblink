# -*- coding:utf-8 -*-
import platform
from ctypes import (
    c_int,
    c_uint,
    c_long,
    c_longlong,
    c_float,
    c_char_p,
    c_wchar_p,
    c_bool,
    c_size_t,
    c_void_p,
    POINTER,
    py_object,
    cdll,
    CFUNCTYPE
)
from . import _LRESULT
from .wkeStruct import *

def MiniblinkInit(_path):   
    '''
    wkeLoadingResult -> enum ->c_uint
    wkeConsoleLevel -> enum -> c_uint
    wkeNavigationType -> enum -> c_uint
    wkeWindowType -> enum -> c_uint
    wkeString ->CString -> c_char_p
    wkeWebFrameHandle ->c_void_p
    wkeNetJob -> c_void_p
    utf8* -> typedef char utf8 ->c_char_p

    '''  
    mb = cdll.LoadLibrary(_path)
    mb.wkeInit()

    mb.wkeVersion.restype=_LRESULT

    mb.wkeVersionString.restype=c_char_p

    mb.wkeGC.argtypes=[_LRESULT,_LRESULT]

    mb.wkeGetTitle.argtypes=[_LRESULT]
    mb.wkeGetTitle.restype=c_char_p

    mb.wkeCreateWebWindow.argtypes=[_LRESULT,c_uint,_LRESULT,c_uint,c_uint]

    mb.wkeCreateWebWindow.restype=_LRESULT

    mb.wkeCreateWebView.argtypes=[]

    mb.wkeCreateWebView.restype=_LRESULT   

    mb.wkeSetWindowTitleW.argtypes=[_LRESULT,c_wchar_p]

    mb.wkeSetTransparent.argtypes=[_LRESULT,c_bool]

    mb.wkeSetHandleOffset.argtypes=[_LRESULT,c_int,c_int]

    mb.wkeSetHandle.argtypes=[_LRESULT,_LRESULT]

    mb.wkeKillFocus.argtypes=[_LRESULT]

    mb.wkeRepaintIfNeeded.argtypes=[_LRESULT]

    mb.wkeWake.argtypes=[_LRESULT]

    mb.wkeGetCaretRect.argtypes=[_LRESULT]

    mb.wkeGetCaretRect.restype=wkeRect

    mb.wkeResize.argtypes=[_LRESULT,c_int,c_int]

    mb.wkeShowWindow.argtypes=[_LRESULT,c_bool]

    mb.wkeMoveToCenter.argtypes=[_LRESULT]

    mb.wkeGoForward.argtypes=[_LRESULT]
    mb.wkeGoForward.restype=c_bool

    mb.wkeGoBack.argtypes=[_LRESULT]
    mb.wkeGoBack.restype=c_bool

    mb.wkeLoadURL.argtypes=[_LRESULT,c_char_p]

    mb.wkeLoadURLW.argtypes=[_LRESULT,c_wchar_p]

    mb.wkeLoadHTMLW.argtypes=[_LRESULT,c_wchar_p]

    mb.wkeLoadFile.argtypes=[_LRESULT,c_char_p]

    mb.wkeLoadFileW.argtypes=[_LRESULT,c_wchar_p]

    mb.wkeReload.argtypes=[_LRESULT]

    mb.wkeStopLoading.argtypes=[_LRESULT]

    mb.wkeWidth.argtypes=[_LRESULT]

    mb.wkeHeight.argtypes=[_LRESULT]

    mb.wkeContentsWidth.argtypes=[_LRESULT]

    mb.wkeContentsHeight.argtypes=[_LRESULT]

    mb.wkeGetWindowHandle.argtypes=[_LRESULT]
    mb.wkeGetWindowHandle.restype=_LRESULT

    mb.wkeGetURL.argtypes=[_LRESULT]
    mb.wkeGetURL.restype=c_char_p

    mb.wkeGetFrameUrl.argtypes=[_LRESULT,_LRESULT]
    mb.wkeGetFrameUrl.restype=c_char_p

    mb.wkeGetSource.argtypes=[_LRESULT]
    mb.wkeGetSource.restype=c_char_p
    
    mb.wkeUtilSerializeToMHTML.argtypes=[_LRESULT]
    mb.wkeUtilSerializeToMHTML.restype=c_char_p

    #注意：此函数一般给3d游戏使用。另外频繁使用此接口并拷贝像素有性能问题。最好用wkeGetViewDC再去拷贝dc
    mb.wkeGetViewDC.argtypes=[_LRESULT]
    mb.wkeGetViewDC.restype=restype=_LRESULT

    mb.wkeFireMouseEvent.argtypes=[_LRESULT,c_uint,c_int,c_int,c_uint]
    mb.wkeFireMouseEvent.restype=c_bool

    mb.wkeFireKeyDownEvent.argtypes=[_LRESULT,c_uint,c_uint,c_bool]
    mb.wkeFireKeyDownEvent.restype=c_bool

    mb.wkeFireKeyUpEvent.argtypes=[_LRESULT,c_uint,c_uint,c_bool]
    mb.wkeFireKeyUpEvent.restype=c_bool

    mb.wkeFireKeyPressEvent.argtypes=[_LRESULT,c_uint,c_uint,c_bool]
    mb.wkeFireKeyPressEvent.restype=c_bool

    mb.wkeFireWindowsMessage.argtypes=[_LRESULT,_LRESULT,c_uint,_LRESULT,_LRESULT]
    mb.wkeFireWindowsMessage.restype=c_bool

    mb.wkeFireMouseWheelEvent.argtypes=[_LRESULT,c_int,c_int,c_int,c_uint]
    mb.wkeFireMouseWheelEvent.restype=c_bool

    mb.wkeFireContextMenuEvent.argtypes=[_LRESULT,c_int,c_int,c_int,c_uint]
    mb.wkeFireContextMenuEvent.restype=c_bool

    # wkeWebView wkeCreateViewCallback(wkeWebView webView, void* param, wkeNavigationType navigationType, const wkeString url, const wkeWindowFeatures* windowFeatures);
    mb.wkeOnCreateView.argtypes=[_LRESULT,CFUNCTYPE(_LRESULT,_LRESULT,c_void_p,c_uint,c_char_p,POINTER(wkeWindowFeatures)),c_void_p]

    #void wkePaintUpdatedCallback(wkeWebView webView, void* param, const HDC hdc, int x, int y, int cx, int cy);
    mb.wkeOnPaintUpdated.argtypes=[None,CFUNCTYPE(None,_LRESULT,c_void_p,_LRESULT,c_int,c_int,c_int,c_int),c_void_p]

    #void wkePaintBitUpdatedCallback(wkeWebView webView, void* param, const void* buffer, const wkeRect* r, int width, int height);
    mb.wkeOnPaintBitUpdated.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeRect),c_int,c_int),c_void_p]
    
    #bool wkeNavigationCallback(wkeWebView webView, void* param, wkeNavigationType navigationType, wkeString url);
    mb.wkeOnNavigation.argtypes=[_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_char_p),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeTitleChangedCallback)(wkeWebView webView, void* param, const wkeString title);
    mb.wkeOnTitleChanged.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p]    

    #typedef void(WKE_CALL_TYPE*wkeURLChangedCallback2)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, const wkeString url);
    mb.wkeOnURLChanged2.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_char_p),c_void_p]  

    mb.wkeOnMouseOverUrlChanged.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_char_p),c_void_p]  

    #typedef void(WKE_CALL_TYPE*wkeAlertBoxCallback)(wkeWebView webView, void* param, const wkeString msg);
    mb.wkeOnAlertBox.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p] 
    
    #typedef bool(WKE_CALL_TYPE*wkeConfirmBoxCallback)(wkeWebView webView, void* param, const wkeString msg);
    mb.wkeOnConfirmBox.argtypes=[_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p),c_void_p] 

    #typedef bool(WKE_CALL_TYPE*wkePromptBoxCallback)(wkeWebView webView, void* param, const wkeString msg, const wkeString defaultResult, wkeString result);
    mb.wkeOnPromptBox.argtypes=[_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_char_p,c_char_p),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeConsoleCallback)(wkeWebView webView, void* param, wkeConsoleLevel level, const wkeString message, const wkeString sourceName, unsigned sourceLine, const wkeString stackTrace);
    mb.wkeOnConsole.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_uint,c_char_p,c_char_p,c_int,c_char_p),c_void_p]

    #typedef bool(WKE_CALL_TYPE*wkeDownloadCallback)(wkeWebView webView, void* param, const char* url);
    mb.wkeOnDownload.argtypes=[_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p),c_void_p]

    #typedef wkeDownloadOpt(WKE_CALL_TYPE*wkeDownload2Callback)(wkeWebView webView, void* param,size_t expectedContentLength,const char* url, const char* mime, const char* disposition, wkeNetJob job, wkeNetJobDataBind* dataBind);
    mb.wkeOnDownload2.argtypes=[_LRESULT,CFUNCTYPE(wkeNetJobDataBind,_LRESULT,c_void_p,c_size_t,c_char_p,c_char_p,c_char_p,c_void_p,POINTER(wkeNetJobDataBind)),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeDocumentReady2Callback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId);
    mb.wkeOnDocumentReady2.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p),c_void_p]

    #typedef bool(WKE_CALL_TYPE*wkeNetResponseCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);
    mb.wkeNetOnResponse.argtypes=[_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]

    #typedef bool(WKE_CALL_TYPE*wkeLoadUrlBeginCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);
    mb.wkeOnLoadUrlBegin.argtypes=[_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeLoadUrlEndCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job, void* buf, int len);
    mb.wkeOnLoadUrlEnd.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_int),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeLoadingFinishCallback)(wkeWebView webView, void* param, const wkeString url, wkeLoadingResult result, const wkeString failedReason);
    mb.wkeOnLoadingFinish.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_int,c_char_p),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeLoadUrlFailCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);
    mb.wkeOnLoadUrlFail.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeOnNetGetFaviconCallback)(wkeWebView webView, void* param, const utf8* url, wkeMemBuf* buf);
    mb.wkeNetGetFavicon.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMemBuf)),c_void_p]

    #typedef bool(WKE_CALL_TYPE*wkeWindowClosingCallback)(wkeWebView webWindow, void* param);
    mb.wkeOnWindowClosing.argtypes=[_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeWindowDestroyCallback)(wkeWebView webWindow, void* param);
    mb.wkeOnWindowDestroy.argtypes=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeOnScreenshot)(wkeWebView webView, void* param, const char* data, size_t size);
    mb.wkeScreenshot.argtypes=[_LRESULT,POINTER(wkeScreenshotSettings),CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_size_t),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeLoadUrlHeadersReceivedCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);
    mb.wkeOnLoadUrlHeadersReceived = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeLoadUrlFinishCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job, int len);
    mb.wkeLoadUrlFinishCallback=[_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_int),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeOnShowDevtoolsCallback)(wkeWebView webView, void* param);
    mb.wkeShowDevtools = [_LRESULT,c_char_p,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeCaretChangedCallback)(wkeWebView webView, void* param, const wkeRect* r);
    mb.wkeOnCaretChanged = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeRect)),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeDraggableRegionsChangedCallback)(wkeWebView webView, void* param, const wkeDraggableRegion* rects, int rectCount);
    mb.wkeOnDraggableRegionsChanged = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeDraggableRegion),c_int),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeWillMediaLoadCallback)(wkeWebView webView, void* param, const char* url, wkeMediaLoadInfo* info);
    mb.wkeOnWillMediaLoad =  [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMediaLoadInfo)),c_void_p]

    #typedef void(WKE_CALL_TYPE*wkeDidCreateScriptContextCallback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, void* context, int extensionGroup, int worldId);
    mb.wkeOnDidCreateScriptContext =  [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int,c_int),c_void_p] 

    #typedef void(WKE_CALL_TYPE*wkeWillReleaseScriptContextCallback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, void* context, int worldId);
    mb.wkeOnWillReleaseScriptContext = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int),c_void_p] 

    #typedef void(WKE_CALL_TYPE*wkeStartDraggingCallback)(wkeWebView webView,void* param, wkeWebFrameHandle frame,const wkeWebDragData* data,wkeWebDragOperationsMask mask, const void* image, const wkePoint* dragImageOffset);
    mb.wkeOnStartDragging = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeWebDragData),c_uint,c_void_p,POINTER(wkePoint)),c_void_p] 

    #typedef void(WKE_CALL_TYPE*wkeOnPrintCallback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, void* printParams);
    mb.wkeOnPrint = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p),c_void_p] 

    #typedef int(WKE_CALL_TYPE*wkeUiThreadPostTaskCallback)(HWND hWnd, wkeUiThreadRunCallback callback, void* param);
    #typedef void(WKE_CALL_TYPE*wkeUiThreadRunCallback)(HWND hWnd, void* param);
    mb.wkeUtilSetUiCallback =  [_LRESULT,CFUNCTYPE(c_int,_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p)] 

    #typedef void(WKE_CALL_TYPE*wkeOnOtherLoadCallback)(wkeWebView webView, void* param, wkeOtherLoadType type, wkeTempCallbackInfo* info);
    mb.wkeOnOtherLoad = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_int,POINTER(wkeTempCallbackInfo)),c_void_p] 

    #typedef bool(WKE_CALL_TYPE* wkeOnContextMenuItemClickCallback)(wkeWebView webView, void* param, wkeOnContextMenuItemClickType type, wkeOnContextMenuItemClickStep step, wkeWebFrameHandle frameId,void* info);
    mb.wkeOnContextMenuItemClick = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_int,c_void_p,c_void_p),c_void_p] 

    mb.wkeIsDocumentReady.argtypes=[_LRESULT]

    mb.wkeNetHookRequest.argtypes=[_LRESULT]

    mb.wkeNetGetRequestMethod.argtypes=[_LRESULT]

    mb.wkeNetGetRequestMethod.restype=_LRESULT
    mb.jsArgCount.argtypes=[_LRESULT]
    mb.jsArgCount.restype=_LRESULT
    mb.wkeGlobalExec.argtypes=[_LRESULT]
    mb.wkeGlobalExec.restype=_LRESULT
    mb.jsGetGlobal.argtypes=[_LRESULT,c_char_p]
    mb.jsGetGlobal.restype=_LRESULT
    mb.jsGet.argtypes=[_LRESULT]
    mb.jsGet.restype=_LRESULT
    mb.wkeRunJSW.argtypes=[_LRESULT,c_wchar_p]
    mb.wkeRunJSW.restype=c_longlong
    mb.jsToStringW.argtypes=[_LRESULT,c_longlong]
    mb.jsToStringW.restype=c_wchar_p
    mb.wkeRunJsByFrame.argtypes=[_LRESULT]
    mb.wkeRunJsByFrame.restype=_LRESULT
    mb.wkeGetGlobalExecByFrame.argtypes=[_LRESULT]
    mb.wkeGetGlobalExecByFrame.restype=_LRESULT
    #mb.wkeJsBindFunction.argtypes=[c_char_p,py_object,c_void_p,c_int]
    #


    mb.jsToTempStringW.argtypes=[_LRESULT]
    mb.jsToTempStringW.restype=c_wchar_p
    mb.jsArgType.argtypes=[_LRESULT]
    mb.jsArgType.restype=_LRESULT
    mb.jsArg.argtypes=[_LRESULT]
    mb.jsArg.restype=_LRESULT
    mb.jsGetLength.argtypes=[_LRESULT]
    mb.jsGetLength.restype=_LRESULT
    mb.jsGetAt.argtypes=[_LRESULT]
    mb.jsGetAt.restype=_LRESULT
    mb.jsSetAt.argtypes=[_LRESULT]
    mb.jsGetKeys.argtypes=[_LRESULT]

    mb.jsGetWebView.argtypes=[_LRESULT]
    mb.jsGetWebView.restype=_LRESULT

    mb.jsCall.argtypes=[_LRESULT]
    mb.jsCall.restype=_LRESULT
    mb.jsIsNumber.argtypes=[c_longlong]
    mb.jsIsNumber.restype=_LRESULT
    mb.jsToInt.argtypes=[_LRESULT]
    mb.jsToInt.restype=_LRESULT
    mb.jsIsString.argtypes=[c_longlong]
    mb.jsIsString.restype=_LRESULT
    mb.jsIsBoolean.argtypes=[c_longlong]
    mb.jsIsBoolean.restype=_LRESULT
    mb.jsStringW.argtypes=[_LRESULT,c_wchar_p]
    mb.jsEmptyArray.argtypes=[_LRESULT]
    mb.jsEmptyArray.restype=_LRESULT
    mb.jsStringW.restype=_LRESULT
    mb.jsBoolean.argtypes=[c_bool]
    mb.jsBoolean.restype=_LRESULT
    mb.jsFloat.argtypes=[c_float]
    mb.jsInt.argtypes=[_LRESULT]
    mb.jsInt.restype=_LRESULT
    mb.jsEmptyObject.argtypes=[_LRESULT]
    mb.jsEmptyObject.restype=_LRESULT
    mb.jsSet.argtypes=[_LRESULT]


    mb.jsBindGetter.argtypes=[c_char_p]
    mb.jsBindSetter.argtypes=[c_char_p]

    mb.wkeGetTempCallbackInfo.restype=c_void_p
    mb.wkeGetTempCallbackInfo.argtypes=[_LRESULT]

    mb.wkeIsMainFrame.argtypes=[_LRESULT,c_int]
    mb.wkeIsMainFrame.restype=c_bool

    mb.wkeGetZoomFactor.argtypes=[_LRESULT]
    mb.wkeGetZoomFactor.restype = c_float
    mb.wkeWebFrameGetMainFrame.restype = _LRESULT


    mb.wkeSetUserKeyValue.argtypes=[_LRESULT,c_char_p,py_object]
    mb.wkeGetUserKeyValue.argtypes=[_LRESULT,c_char_p]
    mb.wkeSetNavigationToNewWindowEnable.argtypes=[_LRESULT,c_bool]

    mb.wkeSetLocalStorageFullPath.argtypes=[_LRESULT,c_wchar_p]
    mb.wkeSetCookieEnabled.argtypes=[_LRESULT]
    mb.wkeSetCookie.argtypes=[_LRESULT]
    mb.wkePerformCookieCommand.argtypes=[_LRESULT]
    mb.wkeSetCookieJarPath.argtypes=[_LRESULT,c_wchar_p]
    mb.wkeSetCookieJarFullPath.argtypes=[_LRESULT,c_wchar_p]
    mb.wkeClearCookie.argtypes=[_LRESULT]
    mb.wkeSetProxy.argtypes=[POINTER(wkeProxy)]
    mb.wkeSetViewProxy.argtypes=[_LRESULT,POINTER(wkeProxy)]
    mb.wkeNetGetPostBody.argtypes=[_LRESULT]
    mb.wkeNetGetPostBody.restype=POINTER(wkePostBodyElements)
    mb.wkeNetCancelRequest.argtypes=[_LRESULT]
    mb.wkeNetSetData.argtypes=[_LRESULT,c_char_p]
    mb.wkeNetSetMIMEType.argtypes=[_LRESULT,c_char_p]
    mb.wkePostURLW.argtypes=[_LRESULT,c_wchar_p,c_char_p]
    mb.wkeSetTouchEnabled.argtypes=[_LRESULT]
    mb.wkeSetDeviceParameter.argtypes=[_LRESULT]
    mb.wkeSetWebViewName.argtypes=[_LRESULT]
    mb.wkeSetZoomFactor.argtypes=[_LRESULT]
    mb.wkeSetNavigationToNewWindowEnable.argtypes=[_LRESULT]
    mb.wkeSetContextMenuEnabled.argtypes=[_LRESULT]
    mb.wkeSetHeadlessEnabled.argtypes=[_LRESULT]
    mb.wkeSetDragEnable.argtypes=[_LRESULT]
    mb.wkeAddPluginDirectory.argtypes=[_LRESULT,c_wchar_p]
    mb.wkeSetNpapiPluginsEnabled.argtypes=[_LRESULT]
    mb.wkeSetCspCheckEnable.argtypes=[_LRESULT]
    mb.wkeSetDebugConfig.argtypes=[_LRESULT]
    mb.wkeSetString.argtypes=[_LRESULT]
    mb.wkeSetUserAgentW.argtypes=[_LRESULT]
    mb.wkeGetUserAgent.argtypes=[_LRESULT]
    mb.wkeGetUserAgent.restype=c_char_p

    mb.wkeGetCookieW.argtypes=[_LRESULT]
    mb.wkeGetCookieW.restype=c_wchar_p
    mb.wkeCreateStringW.restype=_LRESULT
    mb.wkeGetStringW.argtypes=[_LRESULT]
    mb.wkeGetStringW.restype=c_wchar_p

    return mb

