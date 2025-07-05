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
from . import _LRESULT,GetMiniblinkDLL,SetMiniblinkDLL
from .wkeStruct import *

mb = GetMiniblinkDLL()

def wkeGetString(binary,encoding='utf-8'):
    global mb
    b = mb.wkeGetString(binary)
    if b :
        return b.decode(encoding)
    return ""

def wkeSetString(wkeStr,text,encoding='utf-8'):
    global mb
    utf8 = text.encode(encoding)
    l = len(utf8)
    b = mb.wkeSetString(wkeStr,utf8,l)
    return b

def wkeCreateString(text,encoding='utf-8'):
    global mb
    utf8 = text.encode(encoding)
    l = len(utf8)
    wkeStr = mb.wkeCreateString(utf8,l)
    return wkeStr

def MiniblinkInit(_path):   
    '''
    类型转换见wke.h/wke.h.json/prepare.py
    '''  
    global mb
    mb = cdll.LoadLibrary(_path)

    SetMiniblinkDLL(mb)

    mb.wkeInit()

    #void wkeShutdown()
    mb.wkeShutdown.argtypes = []

    #void wkeShutdownForDebug()//测试使用，不了解千万别用！
    mb.wkeShutdownForDebug.argtypes = []


    #unsigned int wkeVersion()
    mb.wkeVersion.argtypes = []
    mb.wkeVersion.restype = c_uint

    #const utf8* wkeVersionString()
    mb.wkeVersionString.argtypes = []
    mb.wkeVersionString.restype = c_char_p

    #void wkeGC(wkeWebView webView, long intervalSec)
    mb.wkeGC.argtypes = [_LRESULT,c_long]


    #void wkeSetResourceGc(wkeWebView webView, long intervalSec)
    mb.wkeSetResourceGc.argtypes = [_LRESULT,c_long]


    #void wkeSetFileSystem(WKE_FILE_OPEN pfnOpen, WKE_FILE_CLOSE pfnClose, WKE_FILE_SIZE pfnSize, WKE_FILE_READ pfnRead, WKE_FILE_SEEK pfnSeek)
    #WKE_FILE_OPEN CFUNCTYPE(c_void_p,c_char_p) 
    #/*typedef void* (WKE_CALL_TYPE *FILE_OPEN_) (const char* path);*/
    #WKE_FILE_CLOSE CFUNCTYPE(None,c_void_p) 
    #/*typedef void(WKE_CALL_TYPE *FILE_CLOSE_) (void* handle);*/
    #WKE_FILE_SIZE CFUNCTYPE(c_size_t,c_void_p) 
    #/*typedef size_t(WKE_CALL_TYPE *FILE_SIZE) (void* handle);*/
    #WKE_FILE_READ CFUNCTYPE(c_size_t,c_void_p,c_void_p,c_size_t) 
    #/*typedef int(WKE_CALL_TYPE *FILE_READ) (void* handle, void* buffer, size_t size);*/
    #WKE_FILE_SEEK CFUNCTYPE(c_size_t,c_void_p,c_int,c_int) 
    #/*typedef int(WKE_CALL_TYPE *FILE_SEEK) (void* handle, int offset, int origin);*/
    mb.wkeSetFileSystem.argtypes = [CFUNCTYPE(c_void_p,c_char_p),CFUNCTYPE(None,c_void_p),CFUNCTYPE(c_size_t,c_void_p),CFUNCTYPE(c_size_t,c_void_p,c_void_p,c_size_t),CFUNCTYPE(c_size_t,c_void_p,c_int,c_int)]


    #const char* wkeWebViewName(wkeWebView webView)
    mb.wkeWebViewName.argtypes = [_LRESULT]
    mb.wkeWebViewName.restype = c_char_p

    #void wkeSetWebViewName(wkeWebView webView, const char* name)
    mb.wkeSetWebViewName.argtypes = [_LRESULT,c_char_p]


    #BOOL wkeIsLoaded(wkeWebView webView)
    mb.wkeIsLoaded.argtypes = [_LRESULT]
    mb.wkeIsLoaded.restype = c_bool

    #BOOL wkeIsLoadFailed(wkeWebView webView)
    mb.wkeIsLoadFailed.argtypes = [_LRESULT]
    mb.wkeIsLoadFailed.restype = c_bool

    #BOOL wkeIsLoadComplete(wkeWebView webView)
    mb.wkeIsLoadComplete.argtypes = [_LRESULT]
    mb.wkeIsLoadComplete.restype = c_bool

    #const utf8* wkeGetSource(wkeWebView webView)
    mb.wkeGetSource.argtypes = [_LRESULT]
    mb.wkeGetSource.restype = c_char_p

    #const utf8* wkeTitle(wkeWebView webView)
    mb.wkeTitle.argtypes = [_LRESULT]
    mb.wkeTitle.restype = c_char_p

    #const wchar_t* wkeTitleW(wkeWebView webView)
    mb.wkeTitleW.argtypes = [_LRESULT]
    mb.wkeTitleW.restype = c_wchar_p

    #int wkeWidth(wkeWebView webView)
    mb.wkeWidth.argtypes = [_LRESULT]
    mb.wkeWidth.restype = c_int

    #int wkeHeight(wkeWebView webView)
    mb.wkeHeight.argtypes = [_LRESULT]
    mb.wkeHeight.restype = c_int

    #int wkeContentsWidth(wkeWebView webView)
    mb.wkeContentsWidth.argtypes = [_LRESULT]
    mb.wkeContentsWidth.restype = c_int

    #int wkeContentsHeight(wkeWebView webView)
    mb.wkeContentsHeight.argtypes = [_LRESULT]
    mb.wkeContentsHeight.restype = c_int

    #void wkeSelectAll(wkeWebView webView)
    mb.wkeSelectAll.argtypes = [_LRESULT]


    #void wkeCopy(wkeWebView webView)
    mb.wkeCopy.argtypes = [_LRESULT]


    #void wkeCut(wkeWebView webView)
    mb.wkeCut.argtypes = [_LRESULT]


    #void wkePaste(wkeWebView webView)
    mb.wkePaste.argtypes = [_LRESULT]


    #void wkeDelete(wkeWebView webView)
    mb.wkeDelete.argtypes = [_LRESULT]


    #BOOL wkeCookieEnabled(wkeWebView webView)
    mb.wkeCookieEnabled.argtypes = [_LRESULT]
    mb.wkeCookieEnabled.restype = c_bool

    #float wkeMediaVolume(wkeWebView webView)
    mb.wkeMediaVolume.argtypes = [_LRESULT]
    mb.wkeMediaVolume.restype = c_float

    #BOOL wkeMouseEvent(wkeWebView webView, unsigned int message, int x, int y, unsigned int flags)
    mb.wkeMouseEvent.argtypes = [_LRESULT,c_uint,c_int,c_int,c_uint]
    mb.wkeMouseEvent.restype = c_bool

    #BOOL wkeContextMenuEvent(wkeWebView webView, int x, int y, unsigned int flags)
    mb.wkeContextMenuEvent.argtypes = [_LRESULT,c_int,c_int,c_uint]
    mb.wkeContextMenuEvent.restype = c_bool

    #BOOL wkeMouseWheel(wkeWebView webView, int x, int y, int delta, unsigned int flags)
    mb.wkeMouseWheel.argtypes = [_LRESULT,c_int,c_int,c_int,c_uint]
    mb.wkeMouseWheel.restype = c_bool

    #BOOL wkeKeyUp(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
    mb.wkeKeyUp.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
    mb.wkeKeyUp.restype = c_bool

    #BOOL wkeKeyDown(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
    mb.wkeKeyDown.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
    mb.wkeKeyDown.restype = c_bool

    #BOOL wkeKeyPress(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
    mb.wkeKeyPress.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
    mb.wkeKeyPress.restype = c_bool

    #void wkeFocus(wkeWebView webView)
    mb.wkeFocus.argtypes = [_LRESULT]


    #void wkeUnfocus(wkeWebView webView)
    mb.wkeUnfocus.argtypes = [_LRESULT]


    #wkeRect wkeGetCaret(wkeWebView webView)
    mb.wkeGetCaret.argtypes = [_LRESULT]
    mb.wkeGetCaret.restype = wkeRect

    #void wkeAwaken(wkeWebView webView)
    mb.wkeAwaken.argtypes = [_LRESULT]


    #float wkeZoomFactor(wkeWebView webView)
    mb.wkeZoomFactor.argtypes = [_LRESULT]
    mb.wkeZoomFactor.restype = c_float

    #void wkeSetClientHandler(wkeWebView webView, const wkeClientHandler* handler)
    mb.wkeSetClientHandler.argtypes = [_LRESULT,POINTER(wkeClientHandle)]


    #const wkeClientHandler* wkeGetClientHandler(wkeWebView webView)
    mb.wkeGetClientHandler.argtypes = [_LRESULT]
    mb.wkeGetClientHandler.restype = POINTER(wkeClientHandle)

    #const utf8* wkeToString(const wkeString string)
    mb.wkeToString.argtypes = [c_char_p]
    mb.wkeToString.restype = c_char_p

    #const wchar_t* wkeToStringW(const wkeString string)
    mb.wkeToStringW.argtypes = [c_char_p]
    mb.wkeToStringW.restype = c_wchar_p

    #const utf8* jsToString(jsExecState es, jsValue v)
    mb.jsToString.argtypes = [c_void_p,c_longlong]
    mb.jsToString.restype = c_char_p

    #const wchar_t* jsToStringW(jsExecState es, jsValue v)
    mb.jsToStringW.argtypes = [c_void_p,c_longlong]
    mb.jsToStringW.restype = c_wchar_p

    #void wkeConfigure(const wkeSettings* settings)
    mb.wkeConfigure.argtypes = [POINTER(wkeSettings)]


    #BOOL wkeIsInitialize()
    mb.wkeIsInitialize.argtypes = []
    mb.wkeIsInitialize.restype = c_bool

    #void wkeSetViewSettings(wkeWebView webView, const wkeViewSettings* settings)
    mb.wkeSetViewSettings.argtypes = [_LRESULT,POINTER(wkeViewSettings)]


    #void wkeSetDebugConfig(wkeWebView webView, const char* debugString, const char* param)
    mb.wkeSetDebugConfig.argtypes = [_LRESULT,c_char_p,c_char_p]


    #void * wkeGetDebugConfig(wkeWebView webView, const char* debugString)
    mb.wkeGetDebugConfig.argtypes = [_LRESULT,c_char_p]
    mb.wkeGetDebugConfig.restype = c_void_p

    #void wkeFinalize()
    mb.wkeFinalize.argtypes = []


    #void wkeUpdate()
    mb.wkeUpdate.argtypes = []


    #unsigned int wkeGetVersion()
    mb.wkeGetVersion.argtypes = []
    mb.wkeGetVersion.restype = c_uint

    #const utf8* wkeGetVersionString()
    mb.wkeGetVersionString.argtypes = []
    mb.wkeGetVersionString.restype = c_char_p

    #wkeWebView wkeCreateWebView()
    mb.wkeCreateWebView.argtypes = []
    mb.wkeCreateWebView.restype = _LRESULT

    #void wkeDestroyWebView(wkeWebView webView)
    mb.wkeDestroyWebView.argtypes = [_LRESULT]


    #void wkeSetMemoryCacheEnable(wkeWebView webView, bool b)
    mb.wkeSetMemoryCacheEnable.argtypes = [_LRESULT,c_bool]


    #void wkeSetMouseEnabled(wkeWebView webView, bool b)
    mb.wkeSetMouseEnabled.argtypes = [_LRESULT,c_bool]


    #void wkeSetTouchEnabled(wkeWebView webView, bool b)
    mb.wkeSetTouchEnabled.argtypes = [_LRESULT,c_bool]


    #void wkeSetSystemTouchEnabled(wkeWebView webView, bool b)
    mb.wkeSetSystemTouchEnabled.argtypes = [_LRESULT,c_bool]


    #void wkeSetContextMenuEnabled(wkeWebView webView, bool b)
    mb.wkeSetContextMenuEnabled.argtypes = [_LRESULT,c_bool]


    #void wkeSetNavigationToNewWindowEnable(wkeWebView webView, bool b)
    mb.wkeSetNavigationToNewWindowEnable.argtypes = [_LRESULT,c_bool]


    #void wkeSetCspCheckEnable(wkeWebView webView, bool b)
    mb.wkeSetCspCheckEnable.argtypes = [_LRESULT,c_bool]


    #void wkeSetNpapiPluginsEnabled(wkeWebView webView, bool b)
    mb.wkeSetNpapiPluginsEnabled.argtypes = [_LRESULT,c_bool]


    #void wkeSetHeadlessEnabled(wkeWebView webView, bool b)//可以关闭渲染
    mb.wkeSetHeadlessEnabled.argtypes = [_LRESULT,c_bool]


    #void wkeSetDragEnable(wkeWebView webView, bool b)//可关闭拖拽文件加载网页
    mb.wkeSetDragEnable.argtypes = [_LRESULT,c_bool]


    #void wkeSetDragDropEnable(wkeWebView webView, bool b)//可关闭拖拽到其他进程
    mb.wkeSetDragDropEnable.argtypes = [_LRESULT,c_bool]


    #void wkeSetContextMenuItemShow(wkeWebView webView, wkeMenuItemId item, bool isShow)//设置某项menu是否显示
    mb.wkeSetContextMenuItemShow.argtypes = [_LRESULT,c_int,c_bool]


    #void wkeSetLanguage(wkeWebView webView, const char* language)
    mb.wkeSetLanguage.argtypes = [_LRESULT,c_char_p]


    #void wkeSetViewNetInterface(wkeWebView webView, const char* netInterface)
    mb.wkeSetViewNetInterface.argtypes = [_LRESULT,c_char_p]


    #void wkeSetProxy(const wkeProxy* proxy)
    mb.wkeSetProxy.argtypes = [POINTER(wkeProxy)]


    #void wkeSetViewProxy(wkeWebView webView, wkeProxy *proxy)
    mb.wkeSetViewProxy.argtypes = [_LRESULT,wkeProxy]


    #const char* wkeGetName(wkeWebView webView)
    mb.wkeGetName.argtypes = [_LRESULT]
    mb.wkeGetName.restype = c_char_p

    #void wkeSetName(wkeWebView webView, const char* name)
    mb.wkeSetName.argtypes = [_LRESULT,c_char_p]


    #void wkeSetHandle(wkeWebView webView, HWND wnd)
    mb.wkeSetHandle.argtypes = [_LRESULT,_LRESULT]


    #void wkeSetHandleOffset(wkeWebView webView, int x, int y)
    mb.wkeSetHandleOffset.argtypes = [_LRESULT,c_int,c_int]


    #BOOL wkeIsTransparent(wkeWebView webView)
    mb.wkeIsTransparent.argtypes = [_LRESULT]
    mb.wkeIsTransparent.restype = c_bool

    #void wkeSetTransparent(wkeWebView webView, bool transparent)
    mb.wkeSetTransparent.argtypes = [_LRESULT,c_bool]


    #void wkeSetUserAgent(wkeWebView webView, const utf8* userAgent)
    mb.wkeSetUserAgent.argtypes = [_LRESULT,c_char_p]


    #const char* wkeGetUserAgent(wkeWebView webView)
    mb.wkeGetUserAgent.argtypes = [_LRESULT]
    mb.wkeGetUserAgent.restype = c_char_p

    #void wkeSetUserAgentW(wkeWebView webView, const wchar_t* userAgent)
    mb.wkeSetUserAgentW.argtypes = [_LRESULT,c_wchar_p]


    #void wkeShowDevtools(wkeWebView webView, const wchar_t* path, wkeOnShowDevtoolsCallback callback, void* param)
    #wkeOnShowDevtoolsCallback CFUNCTYPE(None,_LRESULT,c_void_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeOnShowDevtoolsCallback)(wkeWebView webView, void* param);*/
    mb.wkeShowDevtools.argtypes = [_LRESULT,c_wchar_p,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p]


    #void wkeLoadW(wkeWebView webView, const wchar_t* url)
    mb.wkeLoadW.argtypes = [_LRESULT,c_wchar_p]


    #void wkeLoadURL(wkeWebView webView, const utf8* url)
    mb.wkeLoadURL.argtypes = [_LRESULT,c_char_p]


    #void wkeLoadURLW(wkeWebView webView, const wchar_t* url)
    mb.wkeLoadURLW.argtypes = [_LRESULT,c_wchar_p]


    #void wkePostURL(wkeWebView wkeView, const utf8* url, const char* postData, int postLen)
    mb.wkePostURL.argtypes = [_LRESULT,c_char_p,c_char_p,c_int]


    #void wkePostURLW(wkeWebView wkeView, const wchar_t* url, const char* postData, int postLen)
    mb.wkePostURLW.argtypes = [_LRESULT,c_wchar_p,c_char_p,c_int]


    #void wkeLoadHTML(wkeWebView webView, const utf8* html)
    mb.wkeLoadHTML.argtypes = [_LRESULT,c_char_p]


    #void wkeLoadHtmlWithBaseUrl(wkeWebView webView, const utf8* html, const utf8* baseUrl)
    mb.wkeLoadHtmlWithBaseUrl.argtypes = [_LRESULT,c_char_p,c_char_p]


    #void wkeLoadHTMLW(wkeWebView webView, const wchar_t* html)
    mb.wkeLoadHTMLW.argtypes = [_LRESULT,c_wchar_p]


    #void wkeLoadFile(wkeWebView webView, const utf8* filename)
    mb.wkeLoadFile.argtypes = [_LRESULT,c_char_p]


    #void wkeLoadFileW(wkeWebView webView, const wchar_t* filename)
    mb.wkeLoadFileW.argtypes = [_LRESULT,c_wchar_p]


    #const utf8* wkeGetURL(wkeWebView webView)
    mb.wkeGetURL.argtypes = [_LRESULT]
    mb.wkeGetURL.restype = c_char_p

    #const utf8* wkeGetFrameUrl(wkeWebView webView, wkeWebFrameHandle frameId)
    mb.wkeGetFrameUrl.argtypes = [_LRESULT,c_void_p]
    mb.wkeGetFrameUrl.restype = c_char_p

    #BOOL wkeIsLoading(wkeWebView webView)
    mb.wkeIsLoading.argtypes = [_LRESULT]
    mb.wkeIsLoading.restype = c_bool

    #BOOL wkeIsLoadingSucceeded(wkeWebView webView)
    mb.wkeIsLoadingSucceeded.argtypes = [_LRESULT]
    mb.wkeIsLoadingSucceeded.restype = c_bool

    #BOOL wkeIsLoadingFailed(wkeWebView webView)
    mb.wkeIsLoadingFailed.argtypes = [_LRESULT]
    mb.wkeIsLoadingFailed.restype = c_bool

    #BOOL wkeIsLoadingCompleted(wkeWebView webView)
    mb.wkeIsLoadingCompleted.argtypes = [_LRESULT]
    mb.wkeIsLoadingCompleted.restype = c_bool

    #BOOL wkeIsDocumentReady(wkeWebView webView)
    mb.wkeIsDocumentReady.argtypes = [_LRESULT]
    mb.wkeIsDocumentReady.restype = c_bool

    #void wkeStopLoading(wkeWebView webView)
    mb.wkeStopLoading.argtypes = [_LRESULT]


    #void wkeReload(wkeWebView webView)
    mb.wkeReload.argtypes = [_LRESULT]


    #void wkeGoToOffset(wkeWebView webView, int offset)
    mb.wkeGoToOffset.argtypes = [_LRESULT,c_int]


    #void wkeGoToIndex(wkeWebView webView, int index)
    mb.wkeGoToIndex.argtypes = [_LRESULT,c_int]


    #int wkeGetWebviewId(wkeWebView webView)
    mb.wkeGetWebviewId.argtypes = [_LRESULT]
    mb.wkeGetWebviewId.restype = c_int

    #BOOL wkeIsWebviewAlive(int id)
    mb.wkeIsWebviewAlive.argtypes = [c_int]
    mb.wkeIsWebviewAlive.restype = c_bool

    #BOOL wkeIsWebviewValid(wkeWebView webView)
    mb.wkeIsWebviewValid.argtypes = [_LRESULT]
    mb.wkeIsWebviewValid.restype = c_bool

    #const utf8* wkeGetDocumentCompleteURL(wkeWebView webView, wkeWebFrameHandle frameId, const utf8* partialURL)
    mb.wkeGetDocumentCompleteURL.argtypes = [_LRESULT,c_void_p,c_char_p]
    mb.wkeGetDocumentCompleteURL.restype = c_char_p

    #wkeMemBuf* wkeCreateMemBuf(wkeWebView webView, void* buf, size_t length)
    mb.wkeCreateMemBuf.argtypes = [_LRESULT,c_void_p,_LRESULT]
    mb.wkeCreateMemBuf.restype = POINTER(wkeMemBuf)

    #void wkeFreeMemBuf(wkeMemBuf* buf)
    mb.wkeFreeMemBuf.argtypes = [POINTER(wkeMemBuf)]


    #const utf8* wkeGetTitle(wkeWebView webView)
    mb.wkeGetTitle.argtypes = [_LRESULT]
    mb.wkeGetTitle.restype = c_char_p

    #const wchar_t* wkeGetTitleW(wkeWebView webView)
    mb.wkeGetTitleW.argtypes = [_LRESULT]
    mb.wkeGetTitleW.restype = c_wchar_p

    #void wkeResize(wkeWebView webView, int w, int h)
    mb.wkeResize.argtypes = [_LRESULT,c_int,c_int]


    #int wkeGetWidth(wkeWebView webView)
    mb.wkeGetWidth.argtypes = [_LRESULT]
    mb.wkeGetWidth.restype = c_int

    #int wkeGetHeight(wkeWebView webView)
    mb.wkeGetHeight.argtypes = [_LRESULT]
    mb.wkeGetHeight.restype = c_int

    #int wkeGetContentWidth(wkeWebView webView)
    mb.wkeGetContentWidth.argtypes = [_LRESULT]
    mb.wkeGetContentWidth.restype = c_int

    #int wkeGetContentHeight(wkeWebView webView)
    mb.wkeGetContentHeight.argtypes = [_LRESULT]
    mb.wkeGetContentHeight.restype = c_int

    #void wkeSetDirty(wkeWebView webView, bool dirty)
    mb.wkeSetDirty.argtypes = [_LRESULT,c_bool]


    #BOOL wkeIsDirty(wkeWebView webView)
    mb.wkeIsDirty.argtypes = [_LRESULT]
    mb.wkeIsDirty.restype = c_bool

    #void wkeAddDirtyArea(wkeWebView webView, int x, int y, int w, int h)
    mb.wkeAddDirtyArea.argtypes = [_LRESULT,c_int,c_int,c_int,c_int]


    #void wkeLayoutIfNeeded(wkeWebView webView)
    mb.wkeLayoutIfNeeded.argtypes = [_LRESULT]


    #void wkePaint2(wkeWebView webView, void* bits, int bufWid, int bufHei, int xDst, int yDst, int w, int h, int xSrc, int ySrc, bool bCopyAlpha)
    mb.wkePaint2.argtypes = [_LRESULT,c_void_p,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_bool]


    #void wkePaint(wkeWebView webView, void* bits, int pitch)
    mb.wkePaint.argtypes = [_LRESULT,c_void_p,c_int]


    #void wkeRepaintIfNeeded(wkeWebView webView)
    mb.wkeRepaintIfNeeded.argtypes = [_LRESULT]


    #HDC wkeGetViewDC(wkeWebView webView)
    mb.wkeGetViewDC.argtypes = [_LRESULT]
    mb.wkeGetViewDC.restype = _LRESULT

    #void wkeUnlockViewDC(wkeWebView webView)
    mb.wkeUnlockViewDC.argtypes = [_LRESULT]


    #HWND wkeGetHostHWND(wkeWebView webView)
    mb.wkeGetHostHWND.argtypes = [_LRESULT]
    mb.wkeGetHostHWND.restype = _LRESULT

    #BOOL wkeCanGoBack(wkeWebView webView)
    mb.wkeCanGoBack.argtypes = [_LRESULT]
    mb.wkeCanGoBack.restype = c_bool

    #BOOL wkeGoBack(wkeWebView webView)
    mb.wkeGoBack.argtypes = [_LRESULT]
    mb.wkeGoBack.restype = c_bool

    #BOOL wkeCanGoForward(wkeWebView webView)
    mb.wkeCanGoForward.argtypes = [_LRESULT]
    mb.wkeCanGoForward.restype = c_bool

    #BOOL wkeGoForward(wkeWebView webView)
    mb.wkeGoForward.argtypes = [_LRESULT]
    mb.wkeGoForward.restype = c_bool

    #BOOL wkeNavigateAtIndex(wkeWebView webView, int index)
    mb.wkeNavigateAtIndex.argtypes = [_LRESULT,c_int]
    mb.wkeNavigateAtIndex.restype = c_bool

    #int wkeGetNavigateIndex(wkeWebView webView)
    mb.wkeGetNavigateIndex.argtypes = [_LRESULT]
    mb.wkeGetNavigateIndex.restype = c_int

    #void wkeEditorSelectAll(wkeWebView webView)
    mb.wkeEditorSelectAll.argtypes = [_LRESULT]


    #void wkeEditorUnSelect(wkeWebView webView)
    mb.wkeEditorUnSelect.argtypes = [_LRESULT]


    #void wkeEditorCopy(wkeWebView webView)
    mb.wkeEditorCopy.argtypes = [_LRESULT]


    #void wkeEditorCut(wkeWebView webView)
    mb.wkeEditorCut.argtypes = [_LRESULT]


    #void wkeEditorPaste(wkeWebView webView)
    mb.wkeEditorPaste.argtypes = [_LRESULT]


    #void wkeEditorDelete(wkeWebView webView)
    mb.wkeEditorDelete.argtypes = [_LRESULT]


    #void wkeEditorUndo(wkeWebView webView)
    mb.wkeEditorUndo.argtypes = [_LRESULT]


    #void wkeEditorRedo(wkeWebView webView)
    mb.wkeEditorRedo.argtypes = [_LRESULT]


    #const wchar_t* wkeGetCookieW(wkeWebView webView)
    mb.wkeGetCookieW.argtypes = [_LRESULT]
    mb.wkeGetCookieW.restype = c_wchar_p

    #const utf8* wkeGetCookie(wkeWebView webView)
    mb.wkeGetCookie.argtypes = [_LRESULT]
    mb.wkeGetCookie.restype = c_char_p

    #void wkeSetCookie(wkeWebView webView, const utf8* url, const utf8* cookie)//cookie格式必须是类似:cna=4UvTFE12fEECAXFKf4SFW5eo; expires=Tue;23-Jan-2029 13:17:21 GMT; path=/; domain=.youku.com
    mb.wkeSetCookie.argtypes = [_LRESULT,c_char_p,c_char_p]


    #void wkeVisitAllCookie(wkeWebView webView, void* params, wkeCookieVisitor visitor)
    #wkeCookieVisitor CFUNCTYPE(c_bool,c_void_p,c_char_p,c_char_p,c_char_p,c_char_p,c_int,c_int,POINTER(c_int)) 
    #/*typedef bool(WKE_CALL_TYPE * wkeCookieVisitor)(void* params,const char* name,const char* value,const char* domain,const char* path, int secure,int httpOnly, int* expires );*/
    mb.wkeVisitAllCookie.argtypes = [_LRESULT,c_void_p,CFUNCTYPE(c_bool,c_void_p,c_char_p,c_char_p,c_char_p,c_char_p,c_int,c_int,POINTER(c_int))]


    #void wkePerformCookieCommand(wkeWebView webView, wkeCookieCommand command)
    mb.wkePerformCookieCommand.argtypes = [_LRESULT,c_int]


    #void wkeSetCookieEnabled(wkeWebView webView, bool enable)
    mb.wkeSetCookieEnabled.argtypes = [_LRESULT,c_bool]


    #BOOL wkeIsCookieEnabled(wkeWebView webView)
    mb.wkeIsCookieEnabled.argtypes = [_LRESULT]
    mb.wkeIsCookieEnabled.restype = c_bool

    #void wkeSetCookieJarPath(wkeWebView webView, const WCHAR* path)
    mb.wkeSetCookieJarPath.argtypes = [_LRESULT,c_wchar_p]


    #void wkeSetCookieJarFullPath(wkeWebView webView, const WCHAR* path)
    mb.wkeSetCookieJarFullPath.argtypes = [_LRESULT,c_wchar_p]


    #void wkeClearCookie(wkeWebView webView)
    mb.wkeClearCookie.argtypes = [_LRESULT]


    #void wkeSetLocalStorageFullPath(wkeWebView webView, const WCHAR* path)
    mb.wkeSetLocalStorageFullPath.argtypes = [_LRESULT,c_wchar_p]


    #void wkeAddPluginDirectory(wkeWebView webView, const WCHAR* path)
    mb.wkeAddPluginDirectory.argtypes = [_LRESULT,c_wchar_p]


    #void wkeSetMediaVolume(wkeWebView webView, float volume)
    mb.wkeSetMediaVolume.argtypes = [_LRESULT,c_float]


    #float wkeGetMediaVolume(wkeWebView webView)
    mb.wkeGetMediaVolume.argtypes = [_LRESULT]
    mb.wkeGetMediaVolume.restype = c_float

    #BOOL wkeFireMouseEvent(wkeWebView webView, unsigned int message, int x, int y, unsigned int flags)
    mb.wkeFireMouseEvent.argtypes = [_LRESULT,c_uint,c_int,c_int,c_uint]
    mb.wkeFireMouseEvent.restype = c_bool

    #BOOL wkeFireContextMenuEvent(wkeWebView webView, int x, int y, unsigned int flags)
    mb.wkeFireContextMenuEvent.argtypes = [_LRESULT,c_int,c_int,c_uint]
    mb.wkeFireContextMenuEvent.restype = c_bool

    #BOOL wkeFireMouseWheelEvent(wkeWebView webView, int x, int y, int delta, unsigned int flags)
    mb.wkeFireMouseWheelEvent.argtypes = [_LRESULT,c_int,c_int,c_int,c_uint]
    mb.wkeFireMouseWheelEvent.restype = c_bool

    #BOOL wkeFireKeyUpEvent(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
    mb.wkeFireKeyUpEvent.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
    mb.wkeFireKeyUpEvent.restype = c_bool

    #BOOL wkeFireKeyDownEvent(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
    mb.wkeFireKeyDownEvent.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
    mb.wkeFireKeyDownEvent.restype = c_bool

    #BOOL wkeFireKeyPressEvent(wkeWebView webView, unsigned int charCode, unsigned int flags, bool systemKey)
    mb.wkeFireKeyPressEvent.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
    mb.wkeFireKeyPressEvent.restype = c_bool

    #BOOL wkeFireWindowsMessage(wkeWebView webView, HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam, LRESULT* result)
    mb.wkeFireWindowsMessage.argtypes = [_LRESULT,_LRESULT,c_uint,_LRESULT,_LRESULT,c_void_p]
    mb.wkeFireWindowsMessage.restype = c_bool

    #void wkeSetFocus(wkeWebView webView)
    mb.wkeSetFocus.argtypes = [_LRESULT]


    #void wkeKillFocus(wkeWebView webView)
    mb.wkeKillFocus.argtypes = [_LRESULT]


    #wkeRect wkeGetCaretRect(wkeWebView webView)
    mb.wkeGetCaretRect.argtypes = [_LRESULT]
    mb.wkeGetCaretRect.restype = wkeRect

    #wkeRect* wkeGetCaretRect2(wkeWebView webView)//给一些不方便获取返回结构体的语言调用
    mb.wkeGetCaretRect2.argtypes = [_LRESULT]
    mb.wkeGetCaretRect2.restype = POINTER(wkeRect)

    #jsValue wkeRunJS(wkeWebView webView, const utf8* script)
    mb.wkeRunJS.argtypes = [_LRESULT,c_char_p]
    mb.wkeRunJS.restype = c_longlong

    #jsValue wkeRunJSW(wkeWebView webView, const wchar_t* script)
    mb.wkeRunJSW.argtypes = [_LRESULT,c_wchar_p]
    mb.wkeRunJSW.restype = c_longlong

    #jsExecState wkeGlobalExec(wkeWebView webView)
    mb.wkeGlobalExec.argtypes = [_LRESULT]
    mb.wkeGlobalExec.restype = c_void_p

    #jsExecState wkeGetGlobalExecByFrame(wkeWebView webView, wkeWebFrameHandle frameId)
    mb.wkeGetGlobalExecByFrame.argtypes = [_LRESULT,c_void_p]
    mb.wkeGetGlobalExecByFrame.restype = c_void_p

    #void wkeSleep(wkeWebView webView)
    mb.wkeSleep.argtypes = [_LRESULT]


    #void wkeWake(wkeWebView webView)
    mb.wkeWake.argtypes = [_LRESULT]


    #BOOL wkeIsAwake(wkeWebView webView)
    mb.wkeIsAwake.argtypes = [_LRESULT]
    mb.wkeIsAwake.restype = c_bool

    #void wkeSetZoomFactor(wkeWebView webView, float factor)
    mb.wkeSetZoomFactor.argtypes = [_LRESULT,c_float]


    #float wkeGetZoomFactor(wkeWebView webView)
    mb.wkeGetZoomFactor.argtypes = [_LRESULT]
    mb.wkeGetZoomFactor.restype = c_float

    #void wkeEnableHighDPISupport()
    mb.wkeEnableHighDPISupport.argtypes = []


    #void wkeSetEditable(wkeWebView webView, bool editable)
    mb.wkeSetEditable.argtypes = [_LRESULT,c_bool]


    #const utf8* wkeGetString(const wkeString string)
    mb.wkeGetString.argtypes = [c_char_p]
    mb.wkeGetString.restype = c_char_p

    #const wchar_t* wkeGetStringW(const wkeString string)
    mb.wkeGetStringW.argtypes = [c_char_p]
    mb.wkeGetStringW.restype = c_wchar_p

    #void wkeSetString(wkeString string, const utf8* str, size_t len)
    mb.wkeSetString.argtypes = [c_char_p,c_char_p,_LRESULT]


    #void wkeSetStringWithoutNullTermination(wkeString string, const utf8* str, size_t len)
    mb.wkeSetStringWithoutNullTermination.argtypes = [c_char_p,c_char_p,_LRESULT]


    #void wkeSetStringW(wkeString string, const wchar_t* str, size_t len)
    mb.wkeSetStringW.argtypes = [c_char_p,c_wchar_p,_LRESULT]


    #wkeString wkeCreateString(const utf8* str, size_t len)
    mb.wkeCreateString.argtypes = [c_char_p,_LRESULT]
    mb.wkeCreateString.restype = c_char_p

    #wkeString wkeCreateStringW(const wchar_t* str, size_t len)
    mb.wkeCreateStringW.argtypes = [c_wchar_p,_LRESULT]
    mb.wkeCreateStringW.restype = c_char_p

    #wkeString wkeCreateStringWithoutNullTermination(const utf8* str, size_t len)
    mb.wkeCreateStringWithoutNullTermination.argtypes = [c_char_p,_LRESULT]
    mb.wkeCreateStringWithoutNullTermination.restype = c_char_p

    #size_t wkeGetStringLen(wkeString str)
    mb.wkeGetStringLen.argtypes = [c_char_p]
    mb.wkeGetStringLen.restype = _LRESULT

    #void wkeDeleteString(wkeString str)
    mb.wkeDeleteString.argtypes = [c_char_p]


    #wkeWebView wkeGetWebViewForCurrentContext()
    mb.wkeGetWebViewForCurrentContext.argtypes = []
    mb.wkeGetWebViewForCurrentContext.restype = _LRESULT

    #void wkeSetUserKeyValue(wkeWebView webView, const char* key, void* value)
    mb.wkeSetUserKeyValue.argtypes = [_LRESULT,c_char_p,c_void_p]


    #void* wkeGetUserKeyValue(wkeWebView webView, const char* key)
    mb.wkeGetUserKeyValue.argtypes = [_LRESULT,c_char_p]
    mb.wkeGetUserKeyValue.restype = c_void_p

    #int wkeGetCursorInfoType(wkeWebView webView)
    mb.wkeGetCursorInfoType.argtypes = [_LRESULT]
    mb.wkeGetCursorInfoType.restype = c_int

    #void wkeSetCursorInfoType(wkeWebView webView, int type)
    mb.wkeSetCursorInfoType.argtypes = [_LRESULT,c_int]


    #void wkeSetDragFiles(wkeWebView webView, const POINT* clintPos, const POINT* screenPos, wkeString* files, int filesCount)
    mb.wkeSetDragFiles.argtypes = [_LRESULT,POINTER(wkePoint),POINTER(wkePoint),POINTER(c_char_p),c_int]


    #void wkeSetDeviceParameter(wkeWebView webView, const char* device, const char* paramStr, int paramInt, float paramFloat)
    mb.wkeSetDeviceParameter.argtypes = [_LRESULT,c_char_p,c_char_p,c_int,c_float]


    #wkeTempCallbackInfo* wkeGetTempCallbackInfo(wkeWebView webView)
    mb.wkeGetTempCallbackInfo.argtypes = [_LRESULT]
    mb.wkeGetTempCallbackInfo.restype = POINTER(wkeTempCallbackInfo)

    #void wkeOnCaretChanged(wkeWebView webView, wkeCaretChangedCallback callback, void* callbackParam)
    #wkeCaretChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeRect)) 
    #/*typedef void(WKE_CALL_TYPE*wkeCaretChangedCallback)(wkeWebView webView, void* param, const wkeRect* r);*/
    mb.wkeOnCaretChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeRect)),c_void_p]


    #void wkeOnMouseOverUrlChanged(wkeWebView webView, wkeTitleChangedCallback callback, void* callbackParam)
    #wkeTitleChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeTitleChangedCallback)(wkeWebView webView, void* param, const wkeString title);*/
    mb.wkeOnMouseOverUrlChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p]


    #void wkeOnTitleChanged(wkeWebView webView, wkeTitleChangedCallback callback, void* callbackParam)
    #wkeTitleChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeTitleChangedCallback)(wkeWebView webView, void* param, const wkeString title);*/
    mb.wkeOnTitleChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p]


    #void wkeOnURLChanged(wkeWebView webView, wkeURLChangedCallback callback, void* callbackParam)
    #wkeURLChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeURLChangedCallback)(wkeWebView webView, void* param, const wkeString url);*/
    mb.wkeOnURLChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p]


    #void wkeOnURLChanged2(wkeWebView webView, wkeURLChangedCallback2 callback, void* callbackParam)
    #wkeURLChangedCallback2 CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_char_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeURLChangedCallback2)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, const wkeString url);*/
    mb.wkeOnURLChanged2.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_char_p),c_void_p]


    #void wkeOnPaintUpdated(wkeWebView webView, wkePaintUpdatedCallback callback, void* callbackParam)
    #wkePaintUpdatedCallback CFUNCTYPE(None,_LRESULT,c_void_p,_LRESULT,c_int,c_int,c_int,c_int) 
    #/*typedef void(WKE_CALL_TYPE*wkePaintUpdatedCallback)(wkeWebView webView, void* param, const HDC hdc, int x, int y, int cx, int cy);*/
    mb.wkeOnPaintUpdated.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,_LRESULT,c_int,c_int,c_int,c_int),c_void_p]


    #void wkeOnPaintBitUpdated(wkeWebView webView, wkePaintBitUpdatedCallback callback, void* callbackParam)
    #wkePaintBitUpdatedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeRect),c_int,c_int) 
    #/*typedef void(WKE_CALL_TYPE*wkePaintBitUpdatedCallback)(wkeWebView webView, void* param, const void* buffer, const wkeRect* r, int width, int height);*/
    mb.wkeOnPaintBitUpdated.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeRect),c_int,c_int),c_void_p]


    #void wkeOnAlertBox(wkeWebView webView, wkeAlertBoxCallback callback, void* callbackParam)
    #wkeAlertBoxCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeAlertBoxCallback)(wkeWebView webView, void* param, const wkeString msg);*/
    mb.wkeOnAlertBox.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p]


    #void wkeOnConfirmBox(wkeWebView webView, wkeConfirmBoxCallback callback, void* callbackParam)
    #wkeConfirmBoxCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p) 
    #/*typedef bool(WKE_CALL_TYPE*wkeConfirmBoxCallback)(wkeWebView webView, void* param, const wkeString msg);*/
    mb.wkeOnConfirmBox.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p),c_void_p]


    #void wkeOnPromptBox(wkeWebView webView, wkePromptBoxCallback callback, void* callbackParam)
    #wkePromptBoxCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_char_p,c_char_p) 
    #/*typedef bool(WKE_CALL_TYPE*wkePromptBoxCallback)(wkeWebView webView, void* param, const wkeString msg, const wkeString defaultResult, wkeString result);*/
    mb.wkeOnPromptBox.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_char_p,c_void_p),c_void_p]


    #void wkeOnNavigation(wkeWebView webView, wkeNavigationCallback callback, void* param)
    #wkeNavigationCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_char_p) 
    #/*typedef bool(WKE_CALL_TYPE*wkeNavigationCallback)(wkeWebView webView, void* param, wkeNavigationType navigationType, wkeString url);*/
    mb.wkeOnNavigation.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_char_p),c_void_p]


    #void wkeOnCreateView(wkeWebView webView, wkeCreateViewCallback callback, void* param)
    #wkeCreateViewCallback CFUNCTYPE(_LRESULT,_LRESULT,c_void_p,c_int,c_char_p,POINTER(wkeWindowFeatures)) 
    #/*typedef wkeWebView(WKE_CALL_TYPE*wkeCreateViewCallback)(wkeWebView webView, void* param, wkeNavigationType navigationType, const wkeString url, const wkeWindowFeatures* windowFeatures);*/
    mb.wkeOnCreateView.argtypes = [_LRESULT,CFUNCTYPE(_LRESULT,_LRESULT,c_void_p,c_int,c_char_p,POINTER(wkeWindowFeatures)),c_void_p]


    #void wkeOnDocumentReady(wkeWebView webView, wkeDocumentReadyCallback callback, void* param)
    #wkeDocumentReadyCallback CFUNCTYPE(None,_LRESULT,c_void_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeDocumentReadyCallback)(wkeWebView webView, void* param);*/
    mb.wkeOnDocumentReady.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p]


    #void wkeOnDocumentReady2(wkeWebView webView, wkeDocumentReady2Callback callback, void* param)
    #wkeDocumentReady2Callback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeDocumentReady2Callback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId);*/
    mb.wkeOnDocumentReady2.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p),c_void_p]


    #void wkeOnLoadingFinish(wkeWebView webView, wkeLoadingFinishCallback callback, void* param)
    #wkeLoadingFinishCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_int,c_char_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeLoadingFinishCallback)(wkeWebView webView, void* param, const wkeString url, wkeLoadingResult result, const wkeString failedReason);*/
    mb.wkeOnLoadingFinish.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_int,c_char_p),c_void_p]


    #void wkeOnDownload(wkeWebView webView, wkeDownloadCallback callback, void* param)
    #wkeDownloadCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p) 
    #/*typedef bool(WKE_CALL_TYPE*wkeDownloadCallback)(wkeWebView webView, void* param, const char* url);*/
    mb.wkeOnDownload.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p),c_void_p]


    #void wkeOnDownload2(wkeWebView webView, wkeDownload2Callback callback, void* param)
    #wkeDownload2Callback CFUNCTYPE(wkeNetJobDataBind,_LRESULT,c_void_p,c_size_t,c_char_p,c_char_p,c_char_p,c_void_p,POINTER(wkeNetJobDataBind)) 
    #/*typedef wkeDownloadOpt(WKE_CALL_TYPE*wkeDownload2Callback)(wkeWebView webView, void* param,size_t expectedContentLength,const char* url, const char* mime, const char* disposition, wkeNetJob job, wkeNetJobDataBind* dataBind);*/
    mb.wkeOnDownload2.argtypes = [_LRESULT,CFUNCTYPE(wkeNetJobDataBind,_LRESULT,c_void_p,c_size_t,c_char_p,c_char_p,c_char_p,c_void_p,POINTER(wkeNetJobDataBind)),c_void_p]


    #void wkeOnConsole(wkeWebView webView, wkeConsoleCallback callback, void* param)
    #wkeConsoleCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_uint,c_char_p,c_char_p,c_int,c_char_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeConsoleCallback)(wkeWebView webView, void* param, wkeConsoleLevel level, const wkeString message, const wkeString sourceName, unsigned sourceLine, const wkeString stackTrace);*/
    mb.wkeOnConsole.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_uint,c_char_p,c_char_p,c_int,c_char_p),c_void_p]


    #void wkeSetUIThreadCallback(wkeWebView webView, wkeCallUiThread callback, void* param)
    #wkeCallUiThread CFUNCTYPE(None,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeCallUiThread)(wkeWebView webView, wkeOnCallUiThread func, void* param);*/
    mb.wkeSetUIThreadCallback.argtypes = [_LRESULT,CFUNCTYPE(None,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p),c_void_p]


    #void wkeOnLoadUrlBegin(wkeWebView webView, wkeLoadUrlBeginCallback callback, void* callbackParam)
    #wkeLoadUrlBeginCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p) 
    #/*typedef bool(WKE_CALL_TYPE*wkeLoadUrlBeginCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/
    mb.wkeOnLoadUrlBegin.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]


    #void wkeOnLoadUrlEnd(wkeWebView webView, wkeLoadUrlEndCallback callback, void* callbackParam)
    #wkeLoadUrlEndCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_int) 
    #/*typedef void(WKE_CALL_TYPE*wkeLoadUrlEndCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job, void* buf, int len);*/
    mb.wkeOnLoadUrlEnd.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_int),c_void_p]


    #void wkeOnLoadUrlHeadersReceived(wkeWebView webView, wkeLoadUrlHeadersReceivedCallback callback, void* callbackParam)
    #wkeLoadUrlHeadersReceivedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeLoadUrlHeadersReceivedCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/
    mb.wkeOnLoadUrlHeadersReceived.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]


    #void wkeOnLoadUrlFinish(wkeWebView webView, wkeLoadUrlFinishCallback callback, void* callbackParam)
    #wkeLoadUrlFinishCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_int) 
    #/*typedef void(WKE_CALL_TYPE*wkeLoadUrlFinishCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job, int len);*/
    mb.wkeOnLoadUrlFinish.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_int),c_void_p]


    #void wkeOnLoadUrlFail(wkeWebView webView, wkeLoadUrlFailCallback callback, void* callbackParam)
    #wkeLoadUrlFailCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeLoadUrlFailCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/
    mb.wkeOnLoadUrlFail.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]


    #void wkeOnDidCreateScriptContext(wkeWebView webView, wkeDidCreateScriptContextCallback callback, void* callbackParam)
    #wkeDidCreateScriptContextCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int,c_int) 
    #/*typedef void(WKE_CALL_TYPE*wkeDidCreateScriptContextCallback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, void* context, int extensionGroup, int worldId);*/
    mb.wkeOnDidCreateScriptContext.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int,c_int),c_void_p]


    #void wkeOnWillReleaseScriptContext(wkeWebView webView, wkeWillReleaseScriptContextCallback callback, void* callbackParam)
    #wkeWillReleaseScriptContextCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int) 
    #/*typedef void(WKE_CALL_TYPE*wkeWillReleaseScriptContextCallback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, void* context, int worldId);*/
    mb.wkeOnWillReleaseScriptContext.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int),c_void_p]


    #void wkeOnWindowClosing(wkeWebView webWindow, wkeWindowClosingCallback callback, void* param)
    #wkeWindowClosingCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p) 
    #/*typedef bool(WKE_CALL_TYPE*wkeWindowClosingCallback)(wkeWebView webWindow, void* param);*/
    mb.wkeOnWindowClosing.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p),c_void_p]


    #void wkeOnWindowDestroy(wkeWebView webWindow, wkeWindowDestroyCallback callback, void* param)
    #wkeWindowDestroyCallback CFUNCTYPE(None,_LRESULT,c_void_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeWindowDestroyCallback)(wkeWebView webWindow, void* param);*/
    mb.wkeOnWindowDestroy.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p]


    #void wkeOnDraggableRegionsChanged(wkeWebView webView, wkeDraggableRegionsChangedCallback callback, void* param)
    #wkeDraggableRegionsChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeDraggableRegion),c_int) 
    #/*typedef void(WKE_CALL_TYPE*wkeDraggableRegionsChangedCallback)(wkeWebView webView, void* param, const wkeDraggableRegion* rects, int rectCount);*/
    mb.wkeOnDraggableRegionsChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeDraggableRegion),c_int),c_void_p]


    #void wkeOnWillMediaLoad(wkeWebView webView, wkeWillMediaLoadCallback callback, void* param)
    #wkeWillMediaLoadCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMediaLoadInfo)) 
    #/*typedef void(WKE_CALL_TYPE*wkeWillMediaLoadCallback)(wkeWebView webView, void* param, const char* url, wkeMediaLoadInfo* info);*/
    mb.wkeOnWillMediaLoad.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMediaLoadInfo)),c_void_p]


    #void wkeOnStartDragging(wkeWebView webView, wkeStartDraggingCallback callback, void* param)
    #wkeStartDraggingCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeWebDragData),c_uint,c_void_p,POINTER(wkePoint)) 
    #/*typedef void(WKE_CALL_TYPE*wkeStartDraggingCallback)(wkeWebView webView,void* param, wkeWebFrameHandle frame,const wkeWebDragData* data,wkeWebDragOperationsMask mask, const void* image, const wkePoint* dragImageOffset);*/
    mb.wkeOnStartDragging.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeWebDragData),c_uint,c_void_p,POINTER(wkePoint)),c_void_p]


    #void wkeOnPrint(wkeWebView webView, wkeOnPrintCallback callback, void* param)
    #wkeOnPrintCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeOnPrintCallback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, void* printParams);*/
    mb.wkeOnPrint.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p),c_void_p]


    #void wkeScreenshot(wkeWebView webView, const wkeScreenshotSettings* settings, wkeOnScreenshot callback, void* param)
    #wkeOnScreenshot CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_size_t) 
    #/*typedef void(WKE_CALL_TYPE*wkeOnScreenshot)(wkeWebView webView, void* param, const char* data, size_t size);typedef void(WKE_CALL_TYPE*wkeUiThreadRunCallback)(HWND hWnd, void* param);*/
    mb.wkeScreenshot.argtypes = [_LRESULT,POINTER(wkeScreenshotSettings),CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_size_t),c_void_p]


    #void wkeOnOtherLoad(wkeWebView webView, wkeOnOtherLoadCallback callback, void* param)
    #wkeOnOtherLoadCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_int,POINTER(wkeTempCallbackInfo)) 
    #/*typedef void(WKE_CALL_TYPE*wkeOnOtherLoadCallback)(wkeWebView webView, void* param, wkeOtherLoadType type, wkeTempCallbackInfo* info);*/
    mb.wkeOnOtherLoad.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_int,POINTER(wkeTempCallbackInfo)),c_void_p]


    #void wkeOnContextMenuItemClick(wkeWebView webView, wkeOnContextMenuItemClickCallback callback, void* param)
    #wkeOnContextMenuItemClickCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_int,c_void_p,c_void_p) 
    #/*typedef bool(WKE_CALL_TYPE* wkeOnContextMenuItemClickCallback)(wkeWebView webView, void* param, wkeOnContextMenuItemClickType type, wkeOnContextMenuItemClickStep step, wkeWebFrameHandle frameId,void* info);*/
    mb.wkeOnContextMenuItemClick.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_int,c_void_p,c_void_p),c_void_p]


    #BOOL wkeIsProcessingUserGesture(wkeWebView webView)
    mb.wkeIsProcessingUserGesture.argtypes = [_LRESULT]
    mb.wkeIsProcessingUserGesture.restype = c_bool

    #void wkeNetSetMIMEType(wkeNetJob jobPtr, const char* type)//设置response的mime
    mb.wkeNetSetMIMEType.argtypes = [c_void_p,c_char_p]


    #const char* wkeNetGetMIMEType(wkeNetJob jobPtr, wkeString mime)//获取response的mime
    mb.wkeNetGetMIMEType.argtypes = [c_void_p,c_char_p]
    mb.wkeNetGetMIMEType.restype = c_char_p

    #const char* wkeNetGetReferrer(wkeNetJob jobPtr)//获取request的referrer
    mb.wkeNetGetReferrer.argtypes = [c_void_p]
    mb.wkeNetGetReferrer.restype = c_char_p

    #void wkeNetSetHTTPHeaderField(wkeNetJob jobPtr, const wchar_t* key, const wchar_t* value, bool response)
    mb.wkeNetSetHTTPHeaderField.argtypes = [c_void_p,c_wchar_p,c_wchar_p,c_bool]


    #const char* wkeNetGetHTTPHeaderField(wkeNetJob jobPtr, const char* key)
    mb.wkeNetGetHTTPHeaderField.argtypes = [c_void_p,c_char_p]
    mb.wkeNetGetHTTPHeaderField.restype = c_char_p

    #const char* wkeNetGetHTTPHeaderFieldFromResponse(wkeNetJob jobPtr, const char* key)
    mb.wkeNetGetHTTPHeaderFieldFromResponse.argtypes = [c_void_p,c_char_p]
    mb.wkeNetGetHTTPHeaderFieldFromResponse.restype = c_char_p

    #void wkeNetHookRequest(wkeNetJob jobPtr)
    mb.wkeNetHookRequest.argtypes = [c_void_p]


    #void wkeNetOnResponse(wkeWebView webView, wkeNetResponseCallback callback, void* param)
    #wkeNetResponseCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p) 
    #/*typedef bool(WKE_CALL_TYPE*wkeNetResponseCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/
    mb.wkeNetOnResponse.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]


    #wkeRequestType wkeNetGetRequestMethod(wkeNetJob jobPtr)
    mb.wkeNetGetRequestMethod.argtypes = [c_void_p]
    mb.wkeNetGetRequestMethod.restype = c_int

    #int wkeNetGetFavicon(wkeWebView webView, wkeOnNetGetFaviconCallback callback, void* param)
    #wkeOnNetGetFaviconCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMemBuf)) 
    #/*typedef void(WKE_CALL_TYPE*wkeOnNetGetFaviconCallback)(wkeWebView webView, void* param, const utf8* url, wkeMemBuf* buf);*/
    mb.wkeNetGetFavicon.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMemBuf)),c_void_p]
    mb.wkeNetGetFavicon.restype = c_int

    #void wkeNetContinueJob(wkeNetJob jobPtr)
    mb.wkeNetContinueJob.argtypes = [c_void_p]


    #const char* wkeNetGetUrlByJob(wkeNetJob jobPtr)
    mb.wkeNetGetUrlByJob.argtypes = [c_void_p]
    mb.wkeNetGetUrlByJob.restype = c_char_p

    #const wkeSlist* wkeNetGetRawHttpHead(wkeNetJob jobPtr)
    mb.wkeNetGetRawHttpHead.argtypes = [c_void_p]
    mb.wkeNetGetRawHttpHead.restype = POINTER(wkeSlist)

    #const wkeSlist* wkeNetGetRawResponseHead(wkeNetJob jobPtr)
    mb.wkeNetGetRawResponseHead.argtypes = [c_void_p]
    mb.wkeNetGetRawResponseHead.restype = POINTER(wkeSlist)

    #void wkeNetCancelRequest(wkeNetJob jobPtr)
    mb.wkeNetCancelRequest.argtypes = [c_void_p]


    #BOOL wkeNetHoldJobToAsynCommit(wkeNetJob jobPtr)
    mb.wkeNetHoldJobToAsynCommit.argtypes = [c_void_p]
    mb.wkeNetHoldJobToAsynCommit.restype = c_bool

    #void wkeNetChangeRequestUrl(wkeNetJob jobPtr, const char* url)
    mb.wkeNetChangeRequestUrl.argtypes = [c_void_p,c_char_p]


    #wkeWebUrlRequestPtr wkeNetCreateWebUrlRequest(const utf8* url, const utf8* method, const utf8* mime)
    mb.wkeNetCreateWebUrlRequest.argtypes = [c_char_p,c_char_p,c_char_p]
    mb.wkeNetCreateWebUrlRequest.restype = c_void_p

    #wkeWebUrlRequestPtr wkeNetCreateWebUrlRequest2(const blinkWebURLRequestPtr request)
    mb.wkeNetCreateWebUrlRequest2.argtypes = [c_void_p]
    mb.wkeNetCreateWebUrlRequest2.restype = c_void_p

    #blinkWebURLRequestPtr wkeNetCopyWebUrlRequest(wkeNetJob jobPtr, bool needExtraData)
    mb.wkeNetCopyWebUrlRequest.argtypes = [c_void_p,c_bool]
    mb.wkeNetCopyWebUrlRequest.restype = c_void_p

    #void wkeNetDeleteBlinkWebURLRequestPtr(blinkWebURLRequestPtr request)
    mb.wkeNetDeleteBlinkWebURLRequestPtr.argtypes = [c_void_p]


    #void wkeNetAddHTTPHeaderFieldToUrlRequest(wkeWebUrlRequestPtr request, const utf8* name, const utf8* value)
    mb.wkeNetAddHTTPHeaderFieldToUrlRequest.argtypes = [c_void_p,c_char_p,c_char_p]


    #int wkeNetStartUrlRequest(wkeWebView webView, wkeWebUrlRequestPtr request, void* param, const wkeUrlRequestCallbacks* callbacks)
    mb.wkeNetStartUrlRequest.argtypes = [_LRESULT,c_void_p,c_void_p,POINTER(wkeUrlRequestCallbacks)]
    mb.wkeNetStartUrlRequest.restype = c_int

    #int wkeNetGetHttpStatusCode(wkeWebUrlResponsePtr response)
    mb.wkeNetGetHttpStatusCode.argtypes = [c_void_p]
    mb.wkeNetGetHttpStatusCode.restype = c_int

    #__int64 wkeNetGetExpectedContentLength(wkeWebUrlResponsePtr response)
    mb.wkeNetGetExpectedContentLength.argtypes = [c_void_p]
    mb.wkeNetGetExpectedContentLength.restype = c_longlong

    #const utf8* wkeNetGetResponseUrl(wkeWebUrlResponsePtr response)
    mb.wkeNetGetResponseUrl.argtypes = [c_void_p]
    mb.wkeNetGetResponseUrl.restype = c_char_p

    #void wkeNetCancelWebUrlRequest(int requestId)
    mb.wkeNetCancelWebUrlRequest.argtypes = [c_int]


    #wkePostBodyElements* wkeNetGetPostBody(wkeNetJob jobPtr)
    mb.wkeNetGetPostBody.argtypes = [c_void_p]
    mb.wkeNetGetPostBody.restype = POINTER(wkePostBodyElements)

    #wkePostBodyElements* wkeNetCreatePostBodyElements(wkeWebView webView, size_t length)
    mb.wkeNetCreatePostBodyElements.argtypes = [_LRESULT,_LRESULT]
    mb.wkeNetCreatePostBodyElements.restype = POINTER(wkePostBodyElements)

    #void wkeNetFreePostBodyElements(wkePostBodyElements* elements)
    mb.wkeNetFreePostBodyElements.argtypes = [POINTER(wkePostBodyElements)]


    #wkePostBodyElement* wkeNetCreatePostBodyElement(wkeWebView webView)
    mb.wkeNetCreatePostBodyElement.argtypes = [_LRESULT]
    mb.wkeNetCreatePostBodyElement.restype = POINTER(wkePostBodyElement)

    #void wkeNetFreePostBodyElement(wkePostBodyElement* element)
    mb.wkeNetFreePostBodyElement.argtypes = [POINTER(wkePostBodyElement)]


    #BOOL wkeIsMainFrame(wkeWebView webView, wkeWebFrameHandle frameId)
    mb.wkeIsMainFrame.argtypes = [_LRESULT,c_void_p]
    mb.wkeIsMainFrame.restype = c_bool

    #BOOL wkeIsWebRemoteFrame(wkeWebView webView, wkeWebFrameHandle frameId)
    mb.wkeIsWebRemoteFrame.argtypes = [_LRESULT,c_void_p]
    mb.wkeIsWebRemoteFrame.restype = c_bool

    #wkeWebFrameHandle wkeWebFrameGetMainFrame(wkeWebView webView)
    mb.wkeWebFrameGetMainFrame.argtypes = [_LRESULT]
    mb.wkeWebFrameGetMainFrame.restype = c_void_p

    #jsValue wkeRunJsByFrame(wkeWebView webView, wkeWebFrameHandle frameId, const utf8* script, bool isInClosure)
    mb.wkeRunJsByFrame.argtypes = [_LRESULT,c_void_p,c_char_p,c_bool]
    mb.wkeRunJsByFrame.restype = c_longlong

    #void wkeInsertCSSByFrame(wkeWebView webView, wkeWebFrameHandle frameId, const utf8* cssText)
    mb.wkeInsertCSSByFrame.argtypes = [_LRESULT,c_void_p,c_char_p]


    #void wkeWebFrameGetMainWorldScriptContext(wkeWebView webView, wkeWebFrameHandle webFrameId, v8ContextPtr contextOut)
    mb.wkeWebFrameGetMainWorldScriptContext.argtypes = [_LRESULT,c_void_p,c_void_p]


    #v8Isolate wkeGetBlinkMainThreadIsolate()
    mb.wkeGetBlinkMainThreadIsolate.argtypes = []
    mb.wkeGetBlinkMainThreadIsolate.restype = c_void_p

    #wkeWebView wkeCreateWebWindow(wkeWindowType type, HWND parent, int x, int y, int width, int height)
    mb.wkeCreateWebWindow.argtypes = [c_int,_LRESULT,c_int,c_int,c_int,c_int]
    mb.wkeCreateWebWindow.restype = _LRESULT

    #wkeWebView wkeCreateWebCustomWindow(const wkeWindowCreateInfo* info)
    mb.wkeCreateWebCustomWindow.argtypes = [POINTER(wkeWindowCreateInfo)]
    mb.wkeCreateWebCustomWindow.restype = _LRESULT

    #void wkeDestroyWebWindow(wkeWebView webWindow)
    mb.wkeDestroyWebWindow.argtypes = [_LRESULT]


    #HWND wkeGetWindowHandle(wkeWebView webWindow)
    mb.wkeGetWindowHandle.argtypes = [_LRESULT]
    mb.wkeGetWindowHandle.restype = _LRESULT

    #void wkeShowWindow(wkeWebView webWindow, bool show)
    mb.wkeShowWindow.argtypes = [_LRESULT,c_bool]


    #void wkeEnableWindow(wkeWebView webWindow, bool enable)
    mb.wkeEnableWindow.argtypes = [_LRESULT,c_bool]


    #void wkeMoveWindow(wkeWebView webWindow, int x, int y, int width, int height)
    mb.wkeMoveWindow.argtypes = [_LRESULT,c_int,c_int,c_int,c_int]


    #void wkeMoveToCenter(wkeWebView webWindow)
    mb.wkeMoveToCenter.argtypes = [_LRESULT]


    #void wkeResizeWindow(wkeWebView webWindow, int width, int height)
    mb.wkeResizeWindow.argtypes = [_LRESULT,c_int,c_int]


    #wkeWebDragOperation wkeDragTargetDragEnter(wkeWebView webView, const wkeWebDragData* webDragData, const POINT* clientPoint, const POINT* screenPoint, wkeWebDragOperationsMask operationsAllowed, int modifiers)
    mb.wkeDragTargetDragEnter.argtypes = [_LRESULT,POINTER(wkeWebDragData),POINTER(wkePoint),POINTER(wkePoint),c_int,c_int]
    mb.wkeDragTargetDragEnter.restype = c_int

    #wkeWebDragOperation wkeDragTargetDragOver(wkeWebView webView, const POINT* clientPoint, const POINT* screenPoint, wkeWebDragOperationsMask operationsAllowed, int modifiers)
    mb.wkeDragTargetDragOver.argtypes = [_LRESULT,POINTER(wkePoint),POINTER(wkePoint),c_int,c_int]
    mb.wkeDragTargetDragOver.restype = c_int

    #void wkeDragTargetDragLeave(wkeWebView webView)
    mb.wkeDragTargetDragLeave.argtypes = [_LRESULT]


    #void wkeDragTargetDrop(wkeWebView webView, const POINT* clientPoint, const POINT* screenPoint, int modifiers)
    mb.wkeDragTargetDrop.argtypes = [_LRESULT,POINTER(wkePoint),POINTER(wkePoint),c_int]


    #void wkeDragTargetEnd(wkeWebView webView, const POINT* clientPoint, const POINT* screenPoint, wkeWebDragOperation operation)
    mb.wkeDragTargetEnd.argtypes = [_LRESULT,POINTER(wkePoint),POINTER(wkePoint),c_int]


    #void wkeUtilSetUiCallback(wkeUiThreadPostTaskCallback callback)
    #wkeUiThreadPostTaskCallback CFUNCTYPE(c_int,_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p) 
    #/*typedef int(WKE_CALL_TYPE*wkeUiThreadPostTaskCallback)(HWND hWnd, wkeUiThreadRunCallback callback, void* param);*/
    mb.wkeUtilSetUiCallback.argtypes = [CFUNCTYPE(c_int,_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p)]


    #const utf8* wkeUtilSerializeToMHTML(wkeWebView webView)
    mb.wkeUtilSerializeToMHTML.argtypes = [_LRESULT]
    mb.wkeUtilSerializeToMHTML.restype = c_char_p

    #const wkePdfDatas* wkeUtilPrintToPdf(wkeWebView webView, wkeWebFrameHandle frameId, const wkePrintSettings* settings)
    mb.wkeUtilPrintToPdf.argtypes = [_LRESULT,c_void_p,POINTER(wkePrintSettings)]
    mb.wkeUtilPrintToPdf.restype = POINTER(wkePdfDatas)

    #const wkeMemBuf* wkePrintToBitmap(wkeWebView webView, wkeWebFrameHandle frameId, const wkeScreenshotSettings* settings)
    mb.wkePrintToBitmap.argtypes = [_LRESULT,c_void_p,POINTER(wkeScreenshotSettings)]
    mb.wkePrintToBitmap.restype = POINTER(wkeMemBuf)

    #void wkeUtilRelasePrintPdfDatas(const wkePdfDatas* datas)
    mb.wkeUtilRelasePrintPdfDatas.argtypes = [POINTER(wkePdfDatas)]


    #void wkeSetWindowTitle(wkeWebView webWindow, const utf8* title)
    mb.wkeSetWindowTitle.argtypes = [_LRESULT,c_char_p]


    #void wkeSetWindowTitleW(wkeWebView webWindow, const wchar_t* title)
    mb.wkeSetWindowTitleW.argtypes = [_LRESULT,c_wchar_p]


    #void wkeNodeOnCreateProcess(wkeWebView webView, wkeNodeOnCreateProcessCallback callback, void* param)
    #wkeNodeOnCreateProcessCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_wchar_p,c_wchar_p,POINTER(STARTUPINFOW)) 
    #/*typedef void(__stdcall *wkeNodeOnCreateProcessCallback)(wkeWebView webView, void* param, const WCHAR* applicationPath, const WCHAR* arguments, STARTUPINFOW* startup);*/
    mb.wkeNodeOnCreateProcess.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_wchar_p,c_wchar_p,POINTER(STARTUPINFOW)),c_void_p]


    #void wkeOnPluginFind(wkeWebView webView, const char* mime, wkeOnPluginFindCallback callback, void* param)
    #wkeOnPluginFindCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_void_p) 
    #/*typedef void(WKE_CALL_TYPE*wkeOnPluginFindCallback)(wkeWebView webView, void* param, const utf8* mime, void* initializeFunc, void* getEntryPointsFunc, void* shutdownFunc);*/
    mb.wkeOnPluginFind.argtypes = [_LRESULT,c_char_p,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_void_p),c_void_p]


    #void wkeAddNpapiPlugin(wkeWebView webView, void* initializeFunc, void* getEntryPointsFunc, void* shutdownFunc)
    mb.wkeAddNpapiPlugin.argtypes = [_LRESULT,c_void_p,c_void_p,c_void_p]


    #void wkePluginListBuilderAddPlugin(void* builder, const utf8* name, const utf8* description, const utf8* fileName)
    mb.wkePluginListBuilderAddPlugin.argtypes = [c_void_p,c_char_p,c_char_p,c_char_p]


    #void wkePluginListBuilderAddMediaTypeToLastPlugin(void* builder, const utf8* name, const utf8* description)
    mb.wkePluginListBuilderAddMediaTypeToLastPlugin.argtypes = [c_void_p,c_char_p,c_char_p]


    #void wkePluginListBuilderAddFileExtensionToLastMediaType(void* builder, const utf8* fileExtension)
    mb.wkePluginListBuilderAddFileExtensionToLastMediaType.argtypes = [c_void_p,c_char_p]


    #wkeWebView wkeGetWebViewByNData(void* ndata)
    mb.wkeGetWebViewByNData.argtypes = [c_void_p]
    mb.wkeGetWebViewByNData.restype = _LRESULT

    #BOOL wkeRegisterEmbedderCustomElement(wkeWebView webView, wkeWebFrameHandle frameId, const char* name, void* options, void* outResult)
    mb.wkeRegisterEmbedderCustomElement.argtypes = [_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p]
    mb.wkeRegisterEmbedderCustomElement.restype = c_bool

    #void wkeSetMediaPlayerFactory(wkeWebView webView, wkeMediaPlayerFactory factory, wkeOnIsMediaPlayerSupportsMIMEType callback)
    #wkeMediaPlayerFactory CFUNCTYPE(c_void_p,_LRESULT,c_void_p,c_void_p,c_void_p) 
    #/*typedef wkeMediaPlayer(WKE_CALL_TYPE* wkeMediaPlayerFactory)(wkeWebView webView, wkeMediaPlayerClient client, void* npBrowserFuncs, void* npPluginFuncs); wkeMediaPlayerClient client unknow */
    #wkeOnIsMediaPlayerSupportsMIMEType CFUNCTYPE(c_bool,c_char_p) 
    #/*typedef bool(WKE_CALL_TYPE* wkeOnIsMediaPlayerSupportsMIMEType)(const utf8* mime);*/
    mb.wkeSetMediaPlayerFactory.argtypes = [_LRESULT,CFUNCTYPE(c_void_p,_LRESULT,c_void_p,c_void_p,c_void_p),CFUNCTYPE(c_bool,c_char_p)]


    #const utf8* wkeGetContentAsMarkup(wkeWebView webView, wkeWebFrameHandle frame, size_t* size)
    mb.wkeGetContentAsMarkup.argtypes = [_LRESULT,c_void_p,POINTER(c_size_t)]
    mb.wkeGetContentAsMarkup.restype = c_char_p

    #const utf8* wkeUtilDecodeURLEscape(const utf8* url)
    mb.wkeUtilDecodeURLEscape.argtypes = [c_char_p]
    mb.wkeUtilDecodeURLEscape.restype = c_char_p

    #const utf8* wkeUtilEncodeURLEscape(const utf8* url)
    mb.wkeUtilEncodeURLEscape.argtypes = [c_char_p]
    mb.wkeUtilEncodeURLEscape.restype = c_char_p

    #const utf8* wkeUtilBase64Encode(const utf8* str)
    mb.wkeUtilBase64Encode.argtypes = [c_char_p]
    mb.wkeUtilBase64Encode.restype = c_char_p

    #const utf8* wkeUtilBase64Decode(const utf8* str)
    mb.wkeUtilBase64Decode.argtypes = [c_char_p]
    mb.wkeUtilBase64Decode.restype = c_char_p

    #const wkeMemBuf* wkeUtilCreateV8Snapshot(const utf8* str)
    mb.wkeUtilCreateV8Snapshot.argtypes = [c_char_p]
    mb.wkeUtilCreateV8Snapshot.restype = POINTER(wkeMemBuf)

    #void wkeRunMessageLoop()
    mb.wkeRunMessageLoop.argtypes = []


    #void wkeSaveMemoryCache(wkeWebView webView)
    mb.wkeSaveMemoryCache.argtypes = [_LRESULT]


    #void jsBindFunction(const char* name, jsNativeFunction fn, unsigned int argCount)
    #jsNativeFunction CFUNCTYPE(c_longlong,c_void_p) 
    #/*typedef jsValue(JS_CALL* jsNativeFunction) (jsExecState es);*/
    mb.jsBindFunction.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p),c_uint]


    #void jsBindGetter(const char* name, jsNativeFunction fn)
    #jsNativeFunction CFUNCTYPE(c_longlong,c_void_p) 
    #/*typedef jsValue(JS_CALL* jsNativeFunction) (jsExecState es);*/
    mb.jsBindGetter.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p)]


    #void jsBindSetter(const char* name, jsNativeFunction fn)
    #jsNativeFunction CFUNCTYPE(c_longlong,c_void_p) 
    #/*typedef jsValue(JS_CALL* jsNativeFunction) (jsExecState es);*/
    mb.jsBindSetter.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p)]


    #void wkeJsBindFunction(const char* name, wkeJsNativeFunction fn, void* param, unsigned int argCount)
    #wkeJsNativeFunction CFUNCTYPE(c_longlong,c_void_p,c_void_p) 
    #/*typedef jsValue(WKE_CALL_TYPE* wkeJsNativeFunction) (jsExecState es, void* param);*/
    mb.wkeJsBindFunction.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p,c_void_p),c_void_p,c_uint]


    #void wkeJsBindGetter(const char* name, wkeJsNativeFunction fn, void* param)
    #wkeJsNativeFunction CFUNCTYPE(c_longlong,c_void_p,c_void_p) 
    #/*typedef jsValue(WKE_CALL_TYPE* wkeJsNativeFunction) (jsExecState es, void* param);*/
    mb.wkeJsBindGetter.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p,c_void_p),c_void_p]


    #void wkeJsBindSetter(const char* name, wkeJsNativeFunction fn, void* param)
    #wkeJsNativeFunction CFUNCTYPE(c_longlong,c_void_p,c_void_p) 
    #/*typedef jsValue(WKE_CALL_TYPE* wkeJsNativeFunction) (jsExecState es, void* param);*/
    mb.wkeJsBindSetter.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p,c_void_p),c_void_p]


    #int jsArgCount(jsExecState es)
    mb.jsArgCount.argtypes = [c_void_p]
    mb.jsArgCount.restype = c_int

    #jsType jsArgType(jsExecState es, int argIdx)
    mb.jsArgType.argtypes = [c_void_p,c_int]
    mb.jsArgType.restype = c_int

    #jsValue jsArg(jsExecState es, int argIdx)
    mb.jsArg.argtypes = [c_void_p,c_int]
    mb.jsArg.restype = c_longlong

    #jsType jsTypeOf(jsValue v)
    mb.jsTypeOf.argtypes = [c_longlong]
    mb.jsTypeOf.restype = c_int

    #BOOL jsIsNumber(jsValue v)
    mb.jsIsNumber.argtypes = [c_longlong]
    mb.jsIsNumber.restype = c_bool

    #BOOL jsIsString(jsValue v)
    mb.jsIsString.argtypes = [c_longlong]
    mb.jsIsString.restype = c_bool

    #BOOL jsIsBoolean(jsValue v)
    mb.jsIsBoolean.argtypes = [c_longlong]
    mb.jsIsBoolean.restype = c_bool

    #BOOL jsIsObject(jsValue v)
    mb.jsIsObject.argtypes = [c_longlong]
    mb.jsIsObject.restype = c_bool

    #BOOL jsIsFunction(jsValue v)
    mb.jsIsFunction.argtypes = [c_longlong]
    mb.jsIsFunction.restype = c_bool

    #BOOL jsIsUndefined(jsValue v)
    mb.jsIsUndefined.argtypes = [c_longlong]
    mb.jsIsUndefined.restype = c_bool

    #BOOL jsIsNull(jsValue v)
    mb.jsIsNull.argtypes = [c_longlong]
    mb.jsIsNull.restype = c_bool

    #BOOL jsIsArray(jsValue v)
    mb.jsIsArray.argtypes = [c_longlong]
    mb.jsIsArray.restype = c_bool

    #BOOL jsIsTrue(jsValue v)
    mb.jsIsTrue.argtypes = [c_longlong]
    mb.jsIsTrue.restype = c_bool

    #BOOL jsIsFalse(jsValue v)
    mb.jsIsFalse.argtypes = [c_longlong]
    mb.jsIsFalse.restype = c_bool

    #int jsToInt(jsExecState es, jsValue v)
    mb.jsToInt.argtypes = [c_void_p,c_longlong]
    mb.jsToInt.restype = c_int

    #float jsToFloat(jsExecState es, jsValue v)
    mb.jsToFloat.argtypes = [c_void_p,c_longlong]
    mb.jsToFloat.restype = c_float

    #double jsToDouble(jsExecState es, jsValue v)
    mb.jsToDouble.argtypes = [c_void_p,c_longlong]
    mb.jsToDouble.restype = c_double

    #const char* jsToDoubleString(jsExecState es, jsValue v)
    mb.jsToDoubleString.argtypes = [c_void_p,c_longlong]
    mb.jsToDoubleString.restype = c_char_p

    #BOOL jsToBoolean(jsExecState es, jsValue v)
    mb.jsToBoolean.argtypes = [c_void_p,c_longlong]
    mb.jsToBoolean.restype = c_bool

    #jsValue jsArrayBuffer(jsExecState es, const char* buffer, size_t size)
    mb.jsArrayBuffer.argtypes = [c_void_p,c_char_p,_LRESULT]
    mb.jsArrayBuffer.restype = c_longlong

    #wkeMemBuf* jsGetArrayBuffer(jsExecState es, jsValue value)
    mb.jsGetArrayBuffer.argtypes = [c_void_p,c_longlong]
    mb.jsGetArrayBuffer.restype = POINTER(wkeMemBuf)

    #const utf8* jsToTempString(jsExecState es, jsValue v)
    mb.jsToTempString.argtypes = [c_void_p,c_longlong]
    mb.jsToTempString.restype = c_char_p

    #const wchar_t* jsToTempStringW(jsExecState es, jsValue v)
    mb.jsToTempStringW.argtypes = [c_void_p,c_longlong]
    mb.jsToTempStringW.restype = c_wchar_p

    #void* jsToV8Value(jsExecState es, jsValue v)//return v8::Persistent<v8::Value>*
    mb.jsToV8Value.argtypes = [c_void_p,c_longlong]
    mb.jsToV8Value.restype = c_void_p

    #jsValue jsInt(int n)
    mb.jsInt.argtypes = [c_int]
    mb.jsInt.restype = c_longlong

    #jsValue jsFloat(float f)
    mb.jsFloat.argtypes = [c_float]
    mb.jsFloat.restype = c_longlong

    #jsValue jsDouble(double d)
    mb.jsDouble.argtypes = [c_double]
    mb.jsDouble.restype = c_longlong

    #jsValue jsDoubleString(const char* str)
    mb.jsDoubleString.argtypes = [c_char_p]
    mb.jsDoubleString.restype = c_longlong

    #jsValue jsBoolean(bool b)
    mb.jsBoolean.argtypes = [c_bool]
    mb.jsBoolean.restype = c_longlong

    #jsValue jsUndefined()
    mb.jsUndefined.argtypes = []
    mb.jsUndefined.restype = c_longlong

    #jsValue jsNull()
    mb.jsNull.argtypes = []
    mb.jsNull.restype = c_longlong

    #jsValue jsTrue()
    mb.jsTrue.argtypes = []
    mb.jsTrue.restype = c_longlong

    #jsValue jsFalse()
    mb.jsFalse.argtypes = []
    mb.jsFalse.restype = c_longlong

    #jsValue jsString(jsExecState es, const utf8* str)
    mb.jsString.argtypes = [c_void_p,c_char_p]
    mb.jsString.restype = c_longlong

    #jsValue jsStringW(jsExecState es, const wchar_t* str)
    mb.jsStringW.argtypes = [c_void_p,c_wchar_p]
    mb.jsStringW.restype = c_longlong

    #jsValue jsEmptyObject(jsExecState es)
    mb.jsEmptyObject.argtypes = [c_void_p]
    mb.jsEmptyObject.restype = c_longlong

    #jsValue jsEmptyArray(jsExecState es)
    mb.jsEmptyArray.argtypes = [c_void_p]
    mb.jsEmptyArray.restype = c_longlong

    #jsValue jsObject(jsExecState es, jsData* obj)
    mb.jsObject.argtypes = [c_void_p,POINTER(wkeJsData)]
    mb.jsObject.restype = c_longlong

    #jsValue jsFunction(jsExecState es, jsData* obj)
    mb.jsFunction.argtypes = [c_void_p,POINTER(wkeJsData)]
    mb.jsFunction.restype = c_longlong

    #jsData* jsGetData(jsExecState es, jsValue object)
    mb.jsGetData.argtypes = [c_void_p,c_longlong]
    mb.jsGetData.restype = POINTER(wkeJsData)

    #jsValue jsGet(jsExecState es, jsValue object, const char* prop)
    mb.jsGet.argtypes = [c_void_p,c_longlong,c_char_p]
    mb.jsGet.restype = c_longlong

    #void jsSet(jsExecState es, jsValue object, const char* prop, jsValue v)
    mb.jsSet.argtypes = [c_void_p,c_longlong,c_char_p,c_longlong]


    #jsValue jsGetAt(jsExecState es, jsValue object, int index)
    mb.jsGetAt.argtypes = [c_void_p,c_longlong,c_int]
    mb.jsGetAt.restype = c_longlong

    #void jsSetAt(jsExecState es, jsValue object, int index, jsValue v)
    mb.jsSetAt.argtypes = [c_void_p,c_longlong,c_int,c_longlong]


    #jsKeys* jsGetKeys(jsExecState es, jsValue object)
    mb.jsGetKeys.argtypes = [c_void_p,c_longlong]
    mb.jsGetKeys.restype = POINTER(wkeJsKeys)

    #BOOL jsIsJsValueValid(jsExecState es, jsValue object)
    mb.jsIsJsValueValid.argtypes = [c_void_p,c_longlong]
    mb.jsIsJsValueValid.restype = c_bool

    #BOOL jsIsValidExecState(jsExecState es)
    mb.jsIsValidExecState.argtypes = [c_void_p]
    mb.jsIsValidExecState.restype = c_bool

    #void jsDeleteObjectProp(jsExecState es, jsValue object, const char* prop)
    mb.jsDeleteObjectProp.argtypes = [c_void_p,c_longlong,c_char_p]


    #int jsGetLength(jsExecState es, jsValue object)
    mb.jsGetLength.argtypes = [c_void_p,c_longlong]
    mb.jsGetLength.restype = c_int

    #void jsSetLength(jsExecState es, jsValue object, int length)
    mb.jsSetLength.argtypes = [c_void_p,c_longlong,c_int]


    #jsValue jsGlobalObject(jsExecState es)
    mb.jsGlobalObject.argtypes = [c_void_p]
    mb.jsGlobalObject.restype = c_longlong

    #wkeWebView jsGetWebView(jsExecState es)
    mb.jsGetWebView.argtypes = [c_void_p]
    mb.jsGetWebView.restype = _LRESULT

    #jsValue jsEval(jsExecState es, const utf8* str)
    mb.jsEval.argtypes = [c_void_p,c_char_p]
    mb.jsEval.restype = c_longlong

    #jsValue jsEvalW(jsExecState es, const wchar_t* str)
    mb.jsEvalW.argtypes = [c_void_p,c_wchar_p]
    mb.jsEvalW.restype = c_longlong

    #jsValue jsEvalExW(jsExecState es, const wchar_t* str, bool isInClosure)
    mb.jsEvalExW.argtypes = [c_void_p,c_wchar_p,c_bool]
    mb.jsEvalExW.restype = c_longlong

    #jsValue jsCall(jsExecState es, jsValue func, jsValue thisObject, jsValue* args, int argCount)
    mb.jsCall.argtypes = [c_void_p,c_longlong,c_longlong,POINTER(c_longlong),c_int]
    mb.jsCall.restype = c_longlong

    #jsValue jsCallGlobal(jsExecState es, jsValue func, jsValue* args, int argCount)
    mb.jsCallGlobal.argtypes = [c_void_p,c_longlong,POINTER(c_longlong),c_int]
    mb.jsCallGlobal.restype = c_longlong

    #jsValue jsGetGlobal(jsExecState es, const char* prop)
    mb.jsGetGlobal.argtypes = [c_void_p,c_char_p]
    mb.jsGetGlobal.restype = c_longlong

    #void jsSetGlobal(jsExecState es, const char* prop, jsValue v)
    mb.jsSetGlobal.argtypes = [c_void_p,c_char_p,c_longlong]


    #void jsGC()
    mb.jsGC.argtypes = []


    #BOOL jsAddRef(jsExecState es, jsValue val)
    mb.jsAddRef.argtypes = [c_void_p,c_longlong]
    mb.jsAddRef.restype = c_bool

    #BOOL jsReleaseRef(jsExecState es, jsValue val)
    mb.jsReleaseRef.argtypes = [c_void_p,c_longlong]
    mb.jsReleaseRef.restype = c_bool

    #jsExceptionInfo* jsGetLastErrorIfException(jsExecState es)
    mb.jsGetLastErrorIfException.argtypes = [c_void_p]
    mb.jsGetLastErrorIfException.restype = POINTER(wkeJsExceptionInfo)

    #jsValue jsThrowException(jsExecState es, const utf8* exception)
    mb.jsThrowException.argtypes = [c_void_p,c_char_p]
    mb.jsThrowException.restype = c_longlong

    #const utf8* jsGetCallstack(jsExecState es)
    mb.jsGetCallstack.argtypes = [c_void_p]
    mb.jsGetCallstack.restype = c_char_p



    return mb

