# -*- coding:utf-8 -*-
import platform
from ctypes import (
    c_int,
    c_long,
    c_longlong,
    c_float,
    c_char_p,
    c_wchar_p,
    c_bool,
    c_void_p,
    POINTER,
    py_object,
    cdll,
    CFUNCTYPE
)
from . import _LRESULT
from .wkeStruct import (wkeProxy,wkePostBodyElements,wkeRect)

def MiniblinkInit(_path):     
    mb = cdll.LoadLibrary(_path)
    mb.wkeInit()

    mb.wkeVersion.restype=_LRESULT
    mb.wkeVersionString.restype=c_char_p
    mb.wkeGC.argtypes=[_LRESULT,c_long]
    mb.wkeGetTitle.restype=c_char_p

    mb.wkeCreateWebWindow.restype=_LRESULT
    mb.wkeCreateWebView.restype=_LRESULT        
    mb.wkeSetWindowTitleW.argtypes=[_LRESULT]
    mb.wkeSetTransparent.argtypes=[_LRESULT]
    mb.wkeSetHandleOffset.argtypes=[_LRESULT]
    mb.wkeSetHandle.argtypes=[_LRESULT]
    mb.wkeKillFocus.argtypes=[_LRESULT]
    mb.wkeRepaintIfNeeded.argtypes=[_LRESULT]
    mb.wkeWake.argtypes=[_LRESULT]
    mb.wkeGetCaretRect.argtypes=[_LRESULT]
    mb.wkeGetCaretRect.restype=wkeRect
    mb.wkeResize.argtypes=[_LRESULT]
    mb.wkeShowWindow.argtypes=[_LRESULT]
    mb.wkeMoveToCenter.argtypes=[_LRESULT]
    mb.wkeGoForward.argtypes=[_LRESULT]
    mb.wkeGoBack.argtypes=[_LRESULT]
    mb.wkeLoadURL.argtypes=[_LRESULT]
    mb.wkeLoadURLW.argtypes=[_LRESULT]
    mb.wkeLoadHTMLW.argtypes=[_LRESULT]
    mb.wkeLoadFile.argtypes=[_LRESULT]
    mb.wkeReload.argtypes=[_LRESULT]
    mb.wkeStopLoading.argtypes=[_LRESULT]
    mb.wkeWidth.argtypes=[_LRESULT]
    mb.wkeWidth.restype=_LRESULT
    mb.wkeHeight.argtypes=[_LRESULT]
    mb.wkeHeight.restype=_LRESULT
    mb.wkeContentsWidth.argtypes=[_LRESULT]
    mb.wkeContentsWidth.restype=_LRESULT
    mb.wkeContentsHeight.argtypes=[_LRESULT]
    mb.wkeContentsHeight.restype=_LRESULT
    mb.wkeGetWindowHandle.argtypes=[_LRESULT]
    mb.wkeGetWindowHandle.restype=_LRESULT
    mb.wkeGetURL.argtypes=[_LRESULT]
    mb.wkeGetURL.restype=c_char_p
    mb.wkeGetFrameUrl.argtypes=[_LRESULT]
    mb.wkeGetFrameUrl.restype=c_char_p
    mb.wkeGetSource.argtypes=[_LRESULT]
    mb.wkeGetSource.restype=c_char_p
    mb.wkeUtilSerializeToMHTML.argtypes=[_LRESULT]
    mb.wkeUtilSerializeToMHTML.restype=c_char_p
    mb.wkeGetViewDC.argtypes=[_LRESULT]
    mb.wkeGetViewDC.restype=_LRESULT
    mb.wkeFireMouseEvent.argtypes=[_LRESULT]
    mb.wkeFireKeyDownEvent.argtypes=[_LRESULT]
    mb.wkeFireKeyUpEvent.argtypes=[_LRESULT]
    mb.wkeFireKeyPressEvent.argtypes=[_LRESULT]
    mb.wkeFireWindowsMessage.argtypes=[_LRESULT]
    mb.wkeFireMouseWheelEvent.argtypes=[_LRESULT,c_int,c_int,_LRESULT,c_int]
    mb.wkeFireContextMenuEvent.argtypes=[_LRESULT]

    mb.wkeOnCreateView.argtypes=[_LRESULT]
    mb.wkeOnPaintUpdated.argtypes=[_LRESULT]
    mb.wkeOnPaintBitUpdated.argtypes=[_LRESULT]
    mb.wkeOnNavigation.argtypes=[_LRESULT]
    mb.wkeOnTitleChanged.argtypes=[_LRESULT]
    mb.wkeOnURLChanged2.argtypes=[_LRESULT]
    mb.wkeOnMouseOverUrlChanged.argtypes=[_LRESULT]
    mb.wkeOnAlertBox.argtypes=[_LRESULT]
    mb.wkeOnConfirmBox.argtypes=[_LRESULT]
    mb.wkeOnPromptBox.argtypes=[_LRESULT]
    mb.wkeOnConsole.argtypes=[_LRESULT]
    mb.wkeOnDownload.argtypes=[_LRESULT]
    mb.wkeOnDocumentReady2.argtypes=[_LRESULT]
    mb.wkeNetOnResponse.argtypes=[_LRESULT]
    mb.wkeOnLoadUrlBegin.argtypes=[_LRESULT]
    mb.wkeOnLoadUrlEnd.argtypes=[_LRESULT]
    mb.wkeOnLoadUrlEnd.argtypes=[_LRESULT]
    mb.wkeOnLoadingFinish.argtypes=[_LRESULT]
    mb.wkeOnLoadUrlFail.argtypes=[_LRESULT]
    mb.wkeNetGetFavicon.argtypes=[_LRESULT]

    mb.wkeOnWindowClosing.argtypes=[_LRESULT,CFUNCTYPE(c_bool,_LRESULT,_LRESULT),_LRESULT]
    mb.wkeOnWindowDestroy.argtypes=[_LRESULT]

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

