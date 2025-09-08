# -*- coding:utf-8 -*-
import sys,os

from platform import architecture
from pkgutil import extend_path

from .wkeStruct import *
from ctypes import (
    c_int,
    c_uint,
    c_ushort,
    c_long,
    c_longlong,
    c_ulonglong,
    c_char,
    c_char_p,
    c_wchar_p,
    c_bool,
    c_void_p,
    c_size_t,
    c_float,
    c_double,
    Structure,
    POINTER,
    CFUNCTYPE,
    cdll
    )


__version__ = "0.1.17"
__path__ = extend_path(__path__, __name__)

bit=architecture()[0]

_LRESULT=c_int
MINIBLINK_DLL_PATH =""
MINIBLINK_DLL_HANDLE=None

miniblink_core_dll = '\\miniblink.dll'
if bit == '64bit':
    miniblink_core_dll = '\\miniblink_4975_x64.dll'
    _LRESULT=c_longlong
else:
    miniblink_core_dll = '\\miniblink_4975_x32.dll'
    _LRESULT=c_uint

def SetMiniblinkDLL(dll):
    global MINIBLINK_DLL_HANDLE
    MINIBLINK_DLL_HANDLE = dll
    return
def GetMiniblinkDLL():
    global MINIBLINK_DLL_HANDLE
    return MINIBLINK_DLL_HANDLE

def GetMiniblinkPath():
    return MINIBLINK_DLL_PATH

def GetMiniblinkDir():
    return os.path.dirname(MINIBLINK_DLL_PATH)

def find_miniblink():
    global MINIBLINK_DLL_PATH 

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        #print('running in a PyInstaller bundle')
        # sys._MEIPASS -> _internal directory -D/Temp Folder -F   
        #PyInstaller bundle模式下,释放非exe文件目录就是DLL默认目录位置
        dll_dir = os.path.realpath(sys._MEIPASS)
    else:
        #解释器模式下,解释器目录就是DLL默认目录位置
        dll_dir = os.path.dirname(sys.executable)

    if not os.path.isfile(dll_dir + miniblink_core_dll):
        path = os.environ['PATH']

        #wkeMiniblink Package目录   
        dll_dir = os.path.dirname(__file__) + '\\bin'
        if os.path.isfile(dll_dir + miniblink_core_dll):
            path = dll_dir + ';' + path
            os.environ['PATH'] = path
            MINIBLINK_DLL_PATH = dll_dir + miniblink_core_dll
        else:
            #去系统环境变量下找
            for dll_dir in path.split(';'):
                if os.path.isfile(dll_dir + miniblink_core_dll):
                    MINIBLINK_DLL_PATH = dll_dir + miniblink_core_dll
                    break
            else:
                return
    else:
        MINIBLINK_DLL_PATH = dll_dir + miniblink_core_dll

    try:
        os.add_dll_directory(dll_dir)
    except AttributeError:
        pass


find_miniblink()
del find_miniblink


class WkeCallbackError(RuntimeError):
    pass

'''
初始化整个mb。此句必须在所有mb api前最先调用。并且所有mb api必须和调用wkeInit的线程为同个线程
类型转换见wke.h/wke.h.json/prepare.py
'''  

MINIBLINK_DLL_HANDLE = cdll.LoadLibrary(MINIBLINK_DLL_PATH)

SetMiniblinkDLL(MINIBLINK_DLL_HANDLE)

MINIBLINK_DLL_HANDLE.wkeInit()
mb = MINIBLINK_DLL_HANDLE

#void wkeShutdown()
wkeShutdown = mb.wkeShutdown
wkeShutdown.argtypes = []


#void wkeShutdownForDebug()//测试使用，不了解千万别用！
wkeShutdownForDebug = mb.wkeShutdownForDebug
wkeShutdownForDebug.argtypes = []


#unsigned int wkeVersion()
wkeVersion = mb.wkeVersion
wkeVersion.argtypes = []
wkeVersion.restype = c_uint

#const utf8* wkeVersionString()
wkeVersionString = mb.wkeVersionString
wkeVersionString.argtypes = []
wkeVersionString.restype = c_char_p

#void wkeGC(wkeWebView webView, long intervalSec)
wkeGC = mb.wkeGC
wkeGC.argtypes = [_LRESULT,c_long]


#void wkeSetResourceGc(wkeWebView webView, long intervalSec)
wkeSetResourceGc = mb.wkeSetResourceGc
wkeSetResourceGc.argtypes = [_LRESULT,c_long]


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
wkeSetFileSystem = mb.wkeSetFileSystem
wkeSetFileSystem.argtypes = [CFUNCTYPE(c_void_p,c_char_p),CFUNCTYPE(None,c_void_p),CFUNCTYPE(c_size_t,c_void_p),CFUNCTYPE(c_size_t,c_void_p,c_void_p,c_size_t),CFUNCTYPE(c_size_t,c_void_p,c_int,c_int)]


#const char* wkeWebViewName(wkeWebView webView)
wkeWebViewName = mb.wkeWebViewName
wkeWebViewName.argtypes = [_LRESULT]
wkeWebViewName.restype = c_char_p

#void wkeSetWebViewName(wkeWebView webView, const char* name)
wkeSetWebViewName = mb.wkeSetWebViewName
wkeSetWebViewName.argtypes = [_LRESULT,c_char_p]


#BOOL wkeIsLoaded(wkeWebView webView)
wkeIsLoaded = mb.wkeIsLoaded
wkeIsLoaded.argtypes = [_LRESULT]
wkeIsLoaded.restype = c_bool

#BOOL wkeIsLoadFailed(wkeWebView webView)
wkeIsLoadFailed = mb.wkeIsLoadFailed
wkeIsLoadFailed.argtypes = [_LRESULT]
wkeIsLoadFailed.restype = c_bool

#BOOL wkeIsLoadComplete(wkeWebView webView)
wkeIsLoadComplete = mb.wkeIsLoadComplete
wkeIsLoadComplete.argtypes = [_LRESULT]
wkeIsLoadComplete.restype = c_bool

#const utf8* wkeGetSource(wkeWebView webView)
wkeGetSource = mb.wkeGetSource
wkeGetSource.argtypes = [_LRESULT]
wkeGetSource.restype = c_char_p

#const utf8* wkeTitle(wkeWebView webView)
wkeTitle = mb.wkeTitle
wkeTitle.argtypes = [_LRESULT]
wkeTitle.restype = c_char_p

#const wchar_t* wkeTitleW(wkeWebView webView)
wkeTitleW = mb.wkeTitleW
wkeTitleW.argtypes = [_LRESULT]
wkeTitleW.restype = c_wchar_p

#int wkeWidth(wkeWebView webView)
wkeWidth = mb.wkeWidth
wkeWidth.argtypes = [_LRESULT]
wkeWidth.restype = c_int

#int wkeHeight(wkeWebView webView)
wkeHeight = mb.wkeHeight
wkeHeight.argtypes = [_LRESULT]
wkeHeight.restype = c_int

#int wkeContentsWidth(wkeWebView webView)
wkeContentsWidth = mb.wkeContentsWidth
wkeContentsWidth.argtypes = [_LRESULT]
wkeContentsWidth.restype = c_int

#int wkeContentsHeight(wkeWebView webView)
wkeContentsHeight = mb.wkeContentsHeight
wkeContentsHeight.argtypes = [_LRESULT]
wkeContentsHeight.restype = c_int

#void wkeSelectAll(wkeWebView webView)
wkeSelectAll = mb.wkeSelectAll
wkeSelectAll.argtypes = [_LRESULT]


#void wkeCopy(wkeWebView webView)
wkeCopy = mb.wkeCopy
wkeCopy.argtypes = [_LRESULT]


#void wkeCut(wkeWebView webView)
wkeCut = mb.wkeCut
wkeCut.argtypes = [_LRESULT]


#void wkePaste(wkeWebView webView)
wkePaste = mb.wkePaste
wkePaste.argtypes = [_LRESULT]


#void wkeDelete(wkeWebView webView)
wkeDelete = mb.wkeDelete
wkeDelete.argtypes = [_LRESULT]


#BOOL wkeCookieEnabled(wkeWebView webView)
wkeCookieEnabled = mb.wkeCookieEnabled
wkeCookieEnabled.argtypes = [_LRESULT]
wkeCookieEnabled.restype = c_bool

#float wkeMediaVolume(wkeWebView webView)
wkeMediaVolume = mb.wkeMediaVolume
wkeMediaVolume.argtypes = [_LRESULT]
wkeMediaVolume.restype = c_float

#BOOL wkeMouseEvent(wkeWebView webView, unsigned int message, int x, int y, unsigned int flags)
wkeMouseEvent = mb.wkeMouseEvent
wkeMouseEvent.argtypes = [_LRESULT,c_uint,c_int,c_int,c_uint]
wkeMouseEvent.restype = c_bool

#BOOL wkeContextMenuEvent(wkeWebView webView, int x, int y, unsigned int flags)
wkeContextMenuEvent = mb.wkeContextMenuEvent
wkeContextMenuEvent.argtypes = [_LRESULT,c_int,c_int,c_uint]
wkeContextMenuEvent.restype = c_bool

#BOOL wkeMouseWheel(wkeWebView webView, int x, int y, int delta, unsigned int flags)
wkeMouseWheel = mb.wkeMouseWheel
wkeMouseWheel.argtypes = [_LRESULT,c_int,c_int,c_int,c_uint]
wkeMouseWheel.restype = c_bool

#BOOL wkeKeyUp(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
wkeKeyUp = mb.wkeKeyUp
wkeKeyUp.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
wkeKeyUp.restype = c_bool

#BOOL wkeKeyDown(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
wkeKeyDown = mb.wkeKeyDown
wkeKeyDown.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
wkeKeyDown.restype = c_bool

#BOOL wkeKeyPress(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
wkeKeyPress = mb.wkeKeyPress
wkeKeyPress.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
wkeKeyPress.restype = c_bool

#void wkeFocus(wkeWebView webView)
wkeFocus = mb.wkeFocus
wkeFocus.argtypes = [_LRESULT]


#void wkeUnfocus(wkeWebView webView)
wkeUnfocus = mb.wkeUnfocus
wkeUnfocus.argtypes = [_LRESULT]


#wkeRect wkeGetCaret(wkeWebView webView)
wkeGetCaret = mb.wkeGetCaret
wkeGetCaret.argtypes = [_LRESULT]
wkeGetCaret.restype = wkeRect

#void wkeAwaken(wkeWebView webView)
wkeAwaken = mb.wkeAwaken
wkeAwaken.argtypes = [_LRESULT]


#float wkeZoomFactor(wkeWebView webView)
wkeZoomFactor = mb.wkeZoomFactor
wkeZoomFactor.argtypes = [_LRESULT]
wkeZoomFactor.restype = c_float

#void wkeSetClientHandler(wkeWebView webView, const wkeClientHandler* handler)
wkeSetClientHandler = mb.wkeSetClientHandler
wkeSetClientHandler.argtypes = [_LRESULT,POINTER(wkeClientHandle)]


#const wkeClientHandler* wkeGetClientHandler(wkeWebView webView)
wkeGetClientHandler = mb.wkeGetClientHandler
wkeGetClientHandler.argtypes = [_LRESULT]
wkeGetClientHandler.restype = POINTER(wkeClientHandle)

#const utf8* wkeToString(const wkeString string)
wkeToString = mb.wkeToString
wkeToString.argtypes = [c_char_p]
wkeToString.restype = c_char_p

#const wchar_t* wkeToStringW(const wkeString string)
wkeToStringW = mb.wkeToStringW
wkeToStringW.argtypes = [c_char_p]
wkeToStringW.restype = c_wchar_p

#const utf8* jsToString(jsExecState es, jsValue v)
jsToString = mb.jsToString
jsToString.argtypes = [c_void_p,c_longlong]
jsToString.restype = c_char_p

#const wchar_t* jsToStringW(jsExecState es, jsValue v)
jsToStringW = mb.jsToStringW
jsToStringW.argtypes = [c_void_p,c_longlong]
jsToStringW.restype = c_wchar_p

#void wkeConfigure(const wkeSettings* settings)
wkeConfigure = mb.wkeConfigure
wkeConfigure.argtypes = [POINTER(wkeSettings)]


#BOOL wkeIsInitialize()
wkeIsInitialize = mb.wkeIsInitialize
wkeIsInitialize.argtypes = []
wkeIsInitialize.restype = c_bool

#void wkeSetViewSettings(wkeWebView webView, const wkeViewSettings* settings)
wkeSetViewSettings = mb.wkeSetViewSettings
wkeSetViewSettings.argtypes = [_LRESULT,POINTER(wkeViewSettings)]


#void wkeSetDebugConfig(wkeWebView webView, const char* debugString, const char* param)
wkeSetDebugConfig = mb.wkeSetDebugConfig
wkeSetDebugConfig.argtypes = [_LRESULT,c_char_p,c_char_p]


#void * wkeGetDebugConfig(wkeWebView webView, const char* debugString)
wkeGetDebugConfig = mb.wkeGetDebugConfig
wkeGetDebugConfig.argtypes = [_LRESULT,c_char_p]
wkeGetDebugConfig.restype = c_void_p

#void wkeFinalize()
wkeFinalize = mb.wkeFinalize
wkeFinalize.argtypes = []


#void wkeUpdate()
wkeUpdate = mb.wkeUpdate
wkeUpdate.argtypes = []


#unsigned int wkeGetVersion()
wkeGetVersion = mb.wkeGetVersion
wkeGetVersion.argtypes = []
wkeGetVersion.restype = c_uint

#const utf8* wkeGetVersionString()
wkeGetVersionString = mb.wkeGetVersionString
wkeGetVersionString.argtypes = []
wkeGetVersionString.restype = c_char_p

#wkeWebView wkeCreateWebView()
wkeCreateWebView = mb.wkeCreateWebView
wkeCreateWebView.argtypes = []
wkeCreateWebView.restype = _LRESULT

#void wkeDestroyWebView(wkeWebView webView)
wkeDestroyWebView = mb.wkeDestroyWebView
wkeDestroyWebView.argtypes = [_LRESULT]


#void wkeSetMemoryCacheEnable(wkeWebView webView, bool b)
wkeSetMemoryCacheEnable = mb.wkeSetMemoryCacheEnable
wkeSetMemoryCacheEnable.argtypes = [_LRESULT,c_bool]


#void wkeSetMouseEnabled(wkeWebView webView, bool b)
wkeSetMouseEnabled = mb.wkeSetMouseEnabled
wkeSetMouseEnabled.argtypes = [_LRESULT,c_bool]


#void wkeSetTouchEnabled(wkeWebView webView, bool b)
wkeSetTouchEnabled = mb.wkeSetTouchEnabled
wkeSetTouchEnabled.argtypes = [_LRESULT,c_bool]


#void wkeSetSystemTouchEnabled(wkeWebView webView, bool b)
wkeSetSystemTouchEnabled = mb.wkeSetSystemTouchEnabled
wkeSetSystemTouchEnabled.argtypes = [_LRESULT,c_bool]


#void wkeSetContextMenuEnabled(wkeWebView webView, bool b)
wkeSetContextMenuEnabled = mb.wkeSetContextMenuEnabled
wkeSetContextMenuEnabled.argtypes = [_LRESULT,c_bool]


#void wkeSetNavigationToNewWindowEnable(wkeWebView webView, bool b)
wkeSetNavigationToNewWindowEnable = mb.wkeSetNavigationToNewWindowEnable
wkeSetNavigationToNewWindowEnable.argtypes = [_LRESULT,c_bool]


#void wkeSetCspCheckEnable(wkeWebView webView, bool b)
wkeSetCspCheckEnable = mb.wkeSetCspCheckEnable
wkeSetCspCheckEnable.argtypes = [_LRESULT,c_bool]


#void wkeSetNpapiPluginsEnabled(wkeWebView webView, bool b)
wkeSetNpapiPluginsEnabled = mb.wkeSetNpapiPluginsEnabled
wkeSetNpapiPluginsEnabled.argtypes = [_LRESULT,c_bool]


#void wkeSetHeadlessEnabled(wkeWebView webView, bool b)//可以关闭渲染
wkeSetHeadlessEnabled = mb.wkeSetHeadlessEnabled
wkeSetHeadlessEnabled.argtypes = [_LRESULT,c_bool]


#void wkeSetDragEnable(wkeWebView webView, bool b)//可关闭拖拽文件加载网页
wkeSetDragEnable = mb.wkeSetDragEnable
wkeSetDragEnable.argtypes = [_LRESULT,c_bool]


#void wkeSetDragDropEnable(wkeWebView webView, bool b)//可关闭拖拽到其他进程
wkeSetDragDropEnable = mb.wkeSetDragDropEnable
wkeSetDragDropEnable.argtypes = [_LRESULT,c_bool]


#void wkeSetContextMenuItemShow(wkeWebView webView, wkeMenuItemId item, bool isShow)//设置某项menu是否显示
wkeSetContextMenuItemShow = mb.wkeSetContextMenuItemShow
wkeSetContextMenuItemShow.argtypes = [_LRESULT,c_int,c_bool]


#void wkeSetLanguage(wkeWebView webView, const char* language)
wkeSetLanguage = mb.wkeSetLanguage
wkeSetLanguage.argtypes = [_LRESULT,c_char_p]


#void wkeSetViewNetInterface(wkeWebView webView, const char* netInterface)
wkeSetViewNetInterface = mb.wkeSetViewNetInterface
wkeSetViewNetInterface.argtypes = [_LRESULT,c_char_p]


#void wkeSetProxy(const wkeProxy* proxy)
wkeSetProxy = mb.wkeSetProxy
wkeSetProxy.argtypes = [POINTER(wkeProxy)]


#void wkeSetViewProxy(wkeWebView webView, wkeProxy *proxy)
wkeSetViewProxy = mb.wkeSetViewProxy
wkeSetViewProxy.argtypes = [_LRESULT,wkeProxy]


#const char* wkeGetName(wkeWebView webView)
wkeGetName = mb.wkeGetName
wkeGetName.argtypes = [_LRESULT]
wkeGetName.restype = c_char_p

#void wkeSetName(wkeWebView webView, const char* name)
wkeSetName = mb.wkeSetName
wkeSetName.argtypes = [_LRESULT,c_char_p]


#void wkeSetHandle(wkeWebView webView, HWND wnd)
wkeSetHandle = mb.wkeSetHandle
wkeSetHandle.argtypes = [_LRESULT,_LRESULT]


#void wkeSetHandleOffset(wkeWebView webView, int x, int y)
wkeSetHandleOffset = mb.wkeSetHandleOffset
wkeSetHandleOffset.argtypes = [_LRESULT,c_int,c_int]


#BOOL wkeIsTransparent(wkeWebView webView)
wkeIsTransparent = mb.wkeIsTransparent
wkeIsTransparent.argtypes = [_LRESULT]
wkeIsTransparent.restype = c_bool

#void wkeSetTransparent(wkeWebView webView, bool transparent)
wkeSetTransparent = mb.wkeSetTransparent
wkeSetTransparent.argtypes = [_LRESULT,c_bool]


#void wkeSetUserAgent(wkeWebView webView, const utf8* userAgent)
wkeSetUserAgent = mb.wkeSetUserAgent
wkeSetUserAgent.argtypes = [_LRESULT,c_char_p]


#const char* wkeGetUserAgent(wkeWebView webView)
wkeGetUserAgent = mb.wkeGetUserAgent
wkeGetUserAgent.argtypes = [_LRESULT]
wkeGetUserAgent.restype = c_char_p

#void wkeSetUserAgentW(wkeWebView webView, const wchar_t* userAgent)
wkeSetUserAgentW = mb.wkeSetUserAgentW
wkeSetUserAgentW.argtypes = [_LRESULT,c_wchar_p]


#void wkeShowDevtools(wkeWebView webView, const wchar_t* path, wkeOnShowDevtoolsCallback callback, void* param)
#wkeOnShowDevtoolsCallback CFUNCTYPE(None,_LRESULT,c_void_p) 
#/*typedef void(WKE_CALL_TYPE*wkeOnShowDevtoolsCallback)(wkeWebView webView, void* param);*/
wkeShowDevtools = mb.wkeShowDevtools
wkeShowDevtools.argtypes = [_LRESULT,c_wchar_p,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p]


#void wkeLoadW(wkeWebView webView, const wchar_t* url)
wkeLoadW = mb.wkeLoadW
wkeLoadW.argtypes = [_LRESULT,c_wchar_p]


#void wkeLoadURL(wkeWebView webView, const utf8* url)
wkeLoadURL = mb.wkeLoadURL
wkeLoadURL.argtypes = [_LRESULT,c_char_p]


#void wkeLoadURLW(wkeWebView webView, const wchar_t* url)
wkeLoadURLW = mb.wkeLoadURLW
wkeLoadURLW.argtypes = [_LRESULT,c_wchar_p]


#void wkePostURL(wkeWebView wkeView, const utf8* url, const char* postData, int postLen)
wkePostURL = mb.wkePostURL
wkePostURL.argtypes = [_LRESULT,c_char_p,c_char_p,c_int]


#void wkePostURLW(wkeWebView wkeView, const wchar_t* url, const char* postData, int postLen)
wkePostURLW = mb.wkePostURLW
wkePostURLW.argtypes = [_LRESULT,c_wchar_p,c_char_p,c_int]


#void wkeLoadHTML(wkeWebView webView, const utf8* html)
wkeLoadHTML = mb.wkeLoadHTML
wkeLoadHTML.argtypes = [_LRESULT,c_char_p]


#void wkeLoadHtmlWithBaseUrl(wkeWebView webView, const utf8* html, const utf8* baseUrl)
wkeLoadHtmlWithBaseUrl = mb.wkeLoadHtmlWithBaseUrl
wkeLoadHtmlWithBaseUrl.argtypes = [_LRESULT,c_char_p,c_char_p]


#void wkeLoadHTMLW(wkeWebView webView, const wchar_t* html)
wkeLoadHTMLW = mb.wkeLoadHTMLW
wkeLoadHTMLW.argtypes = [_LRESULT,c_wchar_p]


#void wkeLoadFile(wkeWebView webView, const utf8* filename)
wkeLoadFile = mb.wkeLoadFile
wkeLoadFile.argtypes = [_LRESULT,c_char_p]


#void wkeLoadFileW(wkeWebView webView, const wchar_t* filename)
wkeLoadFileW = mb.wkeLoadFileW
wkeLoadFileW.argtypes = [_LRESULT,c_wchar_p]


#const utf8* wkeGetURL(wkeWebView webView)
wkeGetURL = mb.wkeGetURL
wkeGetURL.argtypes = [_LRESULT]
wkeGetURL.restype = c_char_p

#const utf8* wkeGetFrameUrl(wkeWebView webView, wkeWebFrameHandle frameId)
wkeGetFrameUrl = mb.wkeGetFrameUrl
wkeGetFrameUrl.argtypes = [_LRESULT,c_void_p]
wkeGetFrameUrl.restype = c_char_p

#BOOL wkeIsLoading(wkeWebView webView)
wkeIsLoading = mb.wkeIsLoading
wkeIsLoading.argtypes = [_LRESULT]
wkeIsLoading.restype = c_bool

#BOOL wkeIsLoadingSucceeded(wkeWebView webView)
wkeIsLoadingSucceeded = mb.wkeIsLoadingSucceeded
wkeIsLoadingSucceeded.argtypes = [_LRESULT]
wkeIsLoadingSucceeded.restype = c_bool

#BOOL wkeIsLoadingFailed(wkeWebView webView)
wkeIsLoadingFailed = mb.wkeIsLoadingFailed
wkeIsLoadingFailed.argtypes = [_LRESULT]
wkeIsLoadingFailed.restype = c_bool

#BOOL wkeIsLoadingCompleted(wkeWebView webView)
wkeIsLoadingCompleted = mb.wkeIsLoadingCompleted
wkeIsLoadingCompleted.argtypes = [_LRESULT]
wkeIsLoadingCompleted.restype = c_bool

#BOOL wkeIsDocumentReady(wkeWebView webView)
wkeIsDocumentReady = mb.wkeIsDocumentReady
wkeIsDocumentReady.argtypes = [_LRESULT]
wkeIsDocumentReady.restype = c_bool

#void wkeStopLoading(wkeWebView webView)
wkeStopLoading = mb.wkeStopLoading
wkeStopLoading.argtypes = [_LRESULT]


#void wkeReload(wkeWebView webView)
wkeReload = mb.wkeReload
wkeReload.argtypes = [_LRESULT]


#void wkeGoToOffset(wkeWebView webView, int offset)
wkeGoToOffset = mb.wkeGoToOffset
wkeGoToOffset.argtypes = [_LRESULT,c_int]


#void wkeGoToIndex(wkeWebView webView, int index)
wkeGoToIndex = mb.wkeGoToIndex
wkeGoToIndex.argtypes = [_LRESULT,c_int]


#int wkeGetWebviewId(wkeWebView webView)
wkeGetWebviewId = mb.wkeGetWebviewId
wkeGetWebviewId.argtypes = [_LRESULT]
wkeGetWebviewId.restype = c_int

#BOOL wkeIsWebviewAlive(int id)
wkeIsWebviewAlive = mb.wkeIsWebviewAlive
wkeIsWebviewAlive.argtypes = [c_int]
wkeIsWebviewAlive.restype = c_bool

#BOOL wkeIsWebviewValid(wkeWebView webView)
wkeIsWebviewValid = mb.wkeIsWebviewValid
wkeIsWebviewValid.argtypes = [_LRESULT]
wkeIsWebviewValid.restype = c_bool

#const utf8* wkeGetDocumentCompleteURL(wkeWebView webView, wkeWebFrameHandle frameId, const utf8* partialURL)
wkeGetDocumentCompleteURL = mb.wkeGetDocumentCompleteURL
wkeGetDocumentCompleteURL.argtypes = [_LRESULT,c_void_p,c_char_p]
wkeGetDocumentCompleteURL.restype = c_char_p

#wkeMemBuf* wkeCreateMemBuf(wkeWebView webView, void* buf, size_t length)
wkeCreateMemBuf = mb.wkeCreateMemBuf
wkeCreateMemBuf.argtypes = [_LRESULT,c_void_p,_LRESULT]
wkeCreateMemBuf.restype = POINTER(wkeMemBuf)

#void wkeFreeMemBuf(wkeMemBuf* buf)
wkeFreeMemBuf = mb.wkeFreeMemBuf
wkeFreeMemBuf.argtypes = [POINTER(wkeMemBuf)]


#const utf8* wkeGetTitle(wkeWebView webView)
wkeGetTitle = mb.wkeGetTitle
wkeGetTitle.argtypes = [_LRESULT]
wkeGetTitle.restype = c_char_p

#const wchar_t* wkeGetTitleW(wkeWebView webView)
wkeGetTitleW = mb.wkeGetTitleW
wkeGetTitleW.argtypes = [_LRESULT]
wkeGetTitleW.restype = c_wchar_p

#void wkeResize(wkeWebView webView, int w, int h)
wkeResize = mb.wkeResize
wkeResize.argtypes = [_LRESULT,c_int,c_int]


#int wkeGetWidth(wkeWebView webView)
wkeGetWidth = mb.wkeGetWidth
wkeGetWidth.argtypes = [_LRESULT]
wkeGetWidth.restype = c_int

#int wkeGetHeight(wkeWebView webView)
wkeGetHeight = mb.wkeGetHeight
wkeGetHeight.argtypes = [_LRESULT]
wkeGetHeight.restype = c_int

#int wkeGetContentWidth(wkeWebView webView)
wkeGetContentWidth = mb.wkeGetContentWidth
wkeGetContentWidth.argtypes = [_LRESULT]
wkeGetContentWidth.restype = c_int

#int wkeGetContentHeight(wkeWebView webView)
wkeGetContentHeight = mb.wkeGetContentHeight
wkeGetContentHeight.argtypes = [_LRESULT]
wkeGetContentHeight.restype = c_int

#void wkeSetDirty(wkeWebView webView, bool dirty)
wkeSetDirty = mb.wkeSetDirty
wkeSetDirty.argtypes = [_LRESULT,c_bool]


#BOOL wkeIsDirty(wkeWebView webView)
wkeIsDirty = mb.wkeIsDirty
wkeIsDirty.argtypes = [_LRESULT]
wkeIsDirty.restype = c_bool

#void wkeAddDirtyArea(wkeWebView webView, int x, int y, int w, int h)
wkeAddDirtyArea = mb.wkeAddDirtyArea
wkeAddDirtyArea.argtypes = [_LRESULT,c_int,c_int,c_int,c_int]


#void wkeLayoutIfNeeded(wkeWebView webView)
wkeLayoutIfNeeded = mb.wkeLayoutIfNeeded
wkeLayoutIfNeeded.argtypes = [_LRESULT]


#void wkePaint2(wkeWebView webView, void* bits, int bufWid, int bufHei, int xDst, int yDst, int w, int h, int xSrc, int ySrc, bool bCopyAlpha)
wkePaint2 = mb.wkePaint2
wkePaint2.argtypes = [_LRESULT,c_void_p,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_bool]


#void wkePaint(wkeWebView webView, void* bits, int pitch)
wkePaint = mb.wkePaint
wkePaint.argtypes = [_LRESULT,c_void_p,c_int]


#void wkeRepaintIfNeeded(wkeWebView webView)
wkeRepaintIfNeeded = mb.wkeRepaintIfNeeded
wkeRepaintIfNeeded.argtypes = [_LRESULT]


#HDC wkeGetViewDC(wkeWebView webView)
wkeGetViewDC = mb.wkeGetViewDC
wkeGetViewDC.argtypes = [_LRESULT]
wkeGetViewDC.restype = _LRESULT

#void wkeUnlockViewDC(wkeWebView webView)
wkeUnlockViewDC = mb.wkeUnlockViewDC
wkeUnlockViewDC.argtypes = [_LRESULT]


#HWND wkeGetHostHWND(wkeWebView webView)
wkeGetHostHWND = mb.wkeGetHostHWND
wkeGetHostHWND.argtypes = [_LRESULT]
wkeGetHostHWND.restype = _LRESULT

#BOOL wkeCanGoBack(wkeWebView webView)
wkeCanGoBack = mb.wkeCanGoBack
wkeCanGoBack.argtypes = [_LRESULT]
wkeCanGoBack.restype = c_bool

#BOOL wkeGoBack(wkeWebView webView)
wkeGoBack = mb.wkeGoBack
wkeGoBack.argtypes = [_LRESULT]
wkeGoBack.restype = c_bool

#BOOL wkeCanGoForward(wkeWebView webView)
wkeCanGoForward = mb.wkeCanGoForward
wkeCanGoForward.argtypes = [_LRESULT]
wkeCanGoForward.restype = c_bool

#BOOL wkeGoForward(wkeWebView webView)
wkeGoForward = mb.wkeGoForward
wkeGoForward.argtypes = [_LRESULT]
wkeGoForward.restype = c_bool

#BOOL wkeNavigateAtIndex(wkeWebView webView, int index)
wkeNavigateAtIndex = mb.wkeNavigateAtIndex
wkeNavigateAtIndex.argtypes = [_LRESULT,c_int]
wkeNavigateAtIndex.restype = c_bool

#int wkeGetNavigateIndex(wkeWebView webView)
wkeGetNavigateIndex = mb.wkeGetNavigateIndex
wkeGetNavigateIndex.argtypes = [_LRESULT]
wkeGetNavigateIndex.restype = c_int

#void wkeEditorSelectAll(wkeWebView webView)
wkeEditorSelectAll = mb.wkeEditorSelectAll
wkeEditorSelectAll.argtypes = [_LRESULT]


#void wkeEditorUnSelect(wkeWebView webView)
wkeEditorUnSelect = mb.wkeEditorUnSelect
wkeEditorUnSelect.argtypes = [_LRESULT]


#void wkeEditorCopy(wkeWebView webView)
wkeEditorCopy = mb.wkeEditorCopy
wkeEditorCopy.argtypes = [_LRESULT]


#void wkeEditorCut(wkeWebView webView)
wkeEditorCut = mb.wkeEditorCut
wkeEditorCut.argtypes = [_LRESULT]


#void wkeEditorPaste(wkeWebView webView)
wkeEditorPaste = mb.wkeEditorPaste
wkeEditorPaste.argtypes = [_LRESULT]


#void wkeEditorDelete(wkeWebView webView)
wkeEditorDelete = mb.wkeEditorDelete
wkeEditorDelete.argtypes = [_LRESULT]


#void wkeEditorUndo(wkeWebView webView)
wkeEditorUndo = mb.wkeEditorUndo
wkeEditorUndo.argtypes = [_LRESULT]


#void wkeEditorRedo(wkeWebView webView)
wkeEditorRedo = mb.wkeEditorRedo
wkeEditorRedo.argtypes = [_LRESULT]


#const wchar_t* wkeGetCookieW(wkeWebView webView)
wkeGetCookieW = mb.wkeGetCookieW
wkeGetCookieW.argtypes = [_LRESULT]
wkeGetCookieW.restype = c_wchar_p

#const utf8* wkeGetCookie(wkeWebView webView)
wkeGetCookie = mb.wkeGetCookie
wkeGetCookie.argtypes = [_LRESULT]
wkeGetCookie.restype = c_char_p

#void wkeSetCookie(wkeWebView webView, const utf8* url, const utf8* cookie)//cookie格式必须是类似:cna=4UvTFE12fEECAXFKf4SFW5eo; expires=Tue;23-Jan-2029 13:17:21 GMT; path=/; domain=.youku.com
wkeSetCookie = mb.wkeSetCookie
wkeSetCookie.argtypes = [_LRESULT,c_char_p,c_char_p]


#void wkeVisitAllCookie(wkeWebView webView, void* params, wkeCookieVisitor visitor)
#wkeCookieVisitor CFUNCTYPE(c_bool,c_void_p,c_char_p,c_char_p,c_char_p,c_char_p,c_int,c_int,POINTER(c_int)) 
#/*typedef bool(WKE_CALL_TYPE * wkeCookieVisitor)(void* params,const char* name,const char* value,const char* domain,const char* path, int secure,int httpOnly, int* expires );*/
wkeVisitAllCookie = mb.wkeVisitAllCookie
wkeVisitAllCookie.argtypes = [_LRESULT,c_void_p,CFUNCTYPE(c_bool,c_void_p,c_char_p,c_char_p,c_char_p,c_char_p,c_int,c_int,POINTER(c_int))]


#void wkePerformCookieCommand(wkeWebView webView, wkeCookieCommand command)
wkePerformCookieCommand = mb.wkePerformCookieCommand
wkePerformCookieCommand.argtypes = [_LRESULT,c_int]


#void wkeSetCookieEnabled(wkeWebView webView, bool enable)
wkeSetCookieEnabled = mb.wkeSetCookieEnabled
wkeSetCookieEnabled.argtypes = [_LRESULT,c_bool]


#BOOL wkeIsCookieEnabled(wkeWebView webView)
wkeIsCookieEnabled = mb.wkeIsCookieEnabled
wkeIsCookieEnabled.argtypes = [_LRESULT]
wkeIsCookieEnabled.restype = c_bool

#void wkeSetCookieJarPath(wkeWebView webView, const WCHAR* path)
wkeSetCookieJarPath = mb.wkeSetCookieJarPath
wkeSetCookieJarPath.argtypes = [_LRESULT,c_wchar_p]


#void wkeSetCookieJarFullPath(wkeWebView webView, const WCHAR* path)
wkeSetCookieJarFullPath = mb.wkeSetCookieJarFullPath
wkeSetCookieJarFullPath.argtypes = [_LRESULT,c_wchar_p]


#void wkeClearCookie(wkeWebView webView)
wkeClearCookie = mb.wkeClearCookie
wkeClearCookie.argtypes = [_LRESULT]


#void wkeSetLocalStorageFullPath(wkeWebView webView, const WCHAR* path)
wkeSetLocalStorageFullPath = mb.wkeSetLocalStorageFullPath
wkeSetLocalStorageFullPath.argtypes = [_LRESULT,c_wchar_p]


#void wkeAddPluginDirectory(wkeWebView webView, const WCHAR* path)
wkeAddPluginDirectory = mb.wkeAddPluginDirectory
wkeAddPluginDirectory.argtypes = [_LRESULT,c_wchar_p]


#void wkeSetMediaVolume(wkeWebView webView, float volume)
wkeSetMediaVolume = mb.wkeSetMediaVolume
wkeSetMediaVolume.argtypes = [_LRESULT,c_float]


#float wkeGetMediaVolume(wkeWebView webView)
wkeGetMediaVolume = mb.wkeGetMediaVolume
wkeGetMediaVolume.argtypes = [_LRESULT]
wkeGetMediaVolume.restype = c_float

#BOOL wkeFireMouseEvent(wkeWebView webView, unsigned int message, int x, int y, unsigned int flags)
wkeFireMouseEvent = mb.wkeFireMouseEvent
wkeFireMouseEvent.argtypes = [_LRESULT,c_uint,c_int,c_int,c_uint]
wkeFireMouseEvent.restype = c_bool

#BOOL wkeFireContextMenuEvent(wkeWebView webView, int x, int y, unsigned int flags)
wkeFireContextMenuEvent = mb.wkeFireContextMenuEvent
wkeFireContextMenuEvent.argtypes = [_LRESULT,c_int,c_int,c_uint]
wkeFireContextMenuEvent.restype = c_bool

#BOOL wkeFireMouseWheelEvent(wkeWebView webView, int x, int y, int delta, unsigned int flags)
wkeFireMouseWheelEvent = mb.wkeFireMouseWheelEvent
wkeFireMouseWheelEvent.argtypes = [_LRESULT,c_int,c_int,c_int,c_uint]
wkeFireMouseWheelEvent.restype = c_bool

#BOOL wkeFireKeyUpEvent(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
wkeFireKeyUpEvent = mb.wkeFireKeyUpEvent
wkeFireKeyUpEvent.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
wkeFireKeyUpEvent.restype = c_bool

#BOOL wkeFireKeyDownEvent(wkeWebView webView, unsigned int virtualKeyCode, unsigned int flags, bool systemKey)
wkeFireKeyDownEvent = mb.wkeFireKeyDownEvent
wkeFireKeyDownEvent.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
wkeFireKeyDownEvent.restype = c_bool

#BOOL wkeFireKeyPressEvent(wkeWebView webView, unsigned int charCode, unsigned int flags, bool systemKey)
wkeFireKeyPressEvent = mb.wkeFireKeyPressEvent
wkeFireKeyPressEvent.argtypes = [_LRESULT,c_uint,c_uint,c_bool]
wkeFireKeyPressEvent.restype = c_bool

#BOOL wkeFireWindowsMessage(wkeWebView webView, HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam, LRESULT* result)
wkeFireWindowsMessage = mb.wkeFireWindowsMessage
wkeFireWindowsMessage.argtypes = [_LRESULT,_LRESULT,c_uint,_LRESULT,_LRESULT,c_void_p]
wkeFireWindowsMessage.restype = c_bool

#void wkeSetFocus(wkeWebView webView)
wkeSetFocus = mb.wkeSetFocus
wkeSetFocus.argtypes = [_LRESULT]


#void wkeKillFocus(wkeWebView webView)
wkeKillFocus = mb.wkeKillFocus
wkeKillFocus.argtypes = [_LRESULT]


#wkeRect wkeGetCaretRect(wkeWebView webView)
wkeGetCaretRect = mb.wkeGetCaretRect
wkeGetCaretRect.argtypes = [_LRESULT]
wkeGetCaretRect.restype = wkeRect

#wkeRect* wkeGetCaretRect2(wkeWebView webView)//给一些不方便获取返回结构体的语言调用
wkeGetCaretRect2 = mb.wkeGetCaretRect2
wkeGetCaretRect2.argtypes = [_LRESULT]
wkeGetCaretRect2.restype = POINTER(wkeRect)

#jsValue wkeRunJS(wkeWebView webView, const utf8* script)
wkeRunJS = mb.wkeRunJS
wkeRunJS.argtypes = [_LRESULT,c_char_p]
wkeRunJS.restype = c_longlong

#jsValue wkeRunJSW(wkeWebView webView, const wchar_t* script)
wkeRunJSW = mb.wkeRunJSW
wkeRunJSW.argtypes = [_LRESULT,c_wchar_p]
wkeRunJSW.restype = c_longlong

#jsExecState wkeGlobalExec(wkeWebView webView)
wkeGlobalExec = mb.wkeGlobalExec
wkeGlobalExec.argtypes = [_LRESULT]
wkeGlobalExec.restype = c_void_p

#jsExecState wkeGetGlobalExecByFrame(wkeWebView webView, wkeWebFrameHandle frameId)
wkeGetGlobalExecByFrame = mb.wkeGetGlobalExecByFrame
wkeGetGlobalExecByFrame.argtypes = [_LRESULT,c_void_p]
wkeGetGlobalExecByFrame.restype = c_void_p

#void wkeSleep(wkeWebView webView)
wkeSleep = mb.wkeSleep
wkeSleep.argtypes = [_LRESULT]


#void wkeWake(wkeWebView webView)
wkeWake = mb.wkeWake
wkeWake.argtypes = [_LRESULT]


#BOOL wkeIsAwake(wkeWebView webView)
wkeIsAwake = mb.wkeIsAwake
wkeIsAwake.argtypes = [_LRESULT]
wkeIsAwake.restype = c_bool

#void wkeSetZoomFactor(wkeWebView webView, float factor)
wkeSetZoomFactor = mb.wkeSetZoomFactor
wkeSetZoomFactor.argtypes = [_LRESULT,c_float]


#float wkeGetZoomFactor(wkeWebView webView)
wkeGetZoomFactor = mb.wkeGetZoomFactor
wkeGetZoomFactor.argtypes = [_LRESULT]
wkeGetZoomFactor.restype = c_float

#void wkeEnableHighDPISupport()
wkeEnableHighDPISupport = mb.wkeEnableHighDPISupport
wkeEnableHighDPISupport.argtypes = []


#void wkeSetEditable(wkeWebView webView, bool editable)
wkeSetEditable = mb.wkeSetEditable
wkeSetEditable.argtypes = [_LRESULT,c_bool]


#const utf8* wkeGetString(const wkeString string)
wkeGetString = mb.wkeGetString
wkeGetString.argtypes = [c_char_p]
wkeGetString.restype = c_char_p

#const wchar_t* wkeGetStringW(const wkeString string)
wkeGetStringW = mb.wkeGetStringW
wkeGetStringW.argtypes = [c_char_p]
wkeGetStringW.restype = c_wchar_p

#void wkeSetString(wkeString string, const utf8* str, size_t len)
wkeSetString = mb.wkeSetString
wkeSetString.argtypes = [c_char_p,c_char_p,_LRESULT]


#void wkeSetStringWithoutNullTermination(wkeString string, const utf8* str, size_t len)
wkeSetStringWithoutNullTermination = mb.wkeSetStringWithoutNullTermination
wkeSetStringWithoutNullTermination.argtypes = [c_char_p,c_char_p,_LRESULT]


#void wkeSetStringW(wkeString string, const wchar_t* str, size_t len)
wkeSetStringW = mb.wkeSetStringW
wkeSetStringW.argtypes = [c_char_p,c_wchar_p,_LRESULT]


#wkeString wkeCreateString(const utf8* str, size_t len)
wkeCreateString = mb.wkeCreateString
wkeCreateString.argtypes = [c_char_p,_LRESULT]
wkeCreateString.restype = c_char_p

#wkeString wkeCreateStringW(const wchar_t* str, size_t len)
wkeCreateStringW = mb.wkeCreateStringW
wkeCreateStringW.argtypes = [c_wchar_p,_LRESULT]
wkeCreateStringW.restype = c_char_p

#wkeString wkeCreateStringWithoutNullTermination(const utf8* str, size_t len)
wkeCreateStringWithoutNullTermination = mb.wkeCreateStringWithoutNullTermination
wkeCreateStringWithoutNullTermination.argtypes = [c_char_p,_LRESULT]
wkeCreateStringWithoutNullTermination.restype = c_char_p

#size_t wkeGetStringLen(wkeString str)
wkeGetStringLen = mb.wkeGetStringLen
wkeGetStringLen.argtypes = [c_char_p]
wkeGetStringLen.restype = _LRESULT

#void wkeDeleteString(wkeString str)
wkeDeleteString = mb.wkeDeleteString
wkeDeleteString.argtypes = [c_char_p]


#wkeWebView wkeGetWebViewForCurrentContext()
wkeGetWebViewForCurrentContext = mb.wkeGetWebViewForCurrentContext
wkeGetWebViewForCurrentContext.argtypes = []
wkeGetWebViewForCurrentContext.restype = _LRESULT

#void wkeSetUserKeyValue(wkeWebView webView, const char* key, void* value)
wkeSetUserKeyValue = mb.wkeSetUserKeyValue
wkeSetUserKeyValue.argtypes = [_LRESULT,c_char_p,c_void_p]


#void* wkeGetUserKeyValue(wkeWebView webView, const char* key)
wkeGetUserKeyValue = mb.wkeGetUserKeyValue
wkeGetUserKeyValue.argtypes = [_LRESULT,c_char_p]
wkeGetUserKeyValue.restype = c_void_p

#int wkeGetCursorInfoType(wkeWebView webView)
wkeGetCursorInfoType = mb.wkeGetCursorInfoType
wkeGetCursorInfoType.argtypes = [_LRESULT]
wkeGetCursorInfoType.restype = c_int

#void wkeSetCursorInfoType(wkeWebView webView, int type)
wkeSetCursorInfoType = mb.wkeSetCursorInfoType
wkeSetCursorInfoType.argtypes = [_LRESULT,c_int]


#void wkeSetDragFiles(wkeWebView webView, const POINT* clintPos, const POINT* screenPos, wkeString* files, int filesCount)
wkeSetDragFiles = mb.wkeSetDragFiles
wkeSetDragFiles.argtypes = [_LRESULT,POINTER(wkePoint),POINTER(wkePoint),POINTER(c_char_p),c_int]


#void wkeSetDeviceParameter(wkeWebView webView, const char* device, const char* paramStr, int paramInt, float paramFloat)
wkeSetDeviceParameter = mb.wkeSetDeviceParameter
wkeSetDeviceParameter.argtypes = [_LRESULT,c_char_p,c_char_p,c_int,c_float]


#wkeTempCallbackInfo* wkeGetTempCallbackInfo(wkeWebView webView)
wkeGetTempCallbackInfo = mb.wkeGetTempCallbackInfo
wkeGetTempCallbackInfo.argtypes = [_LRESULT]
wkeGetTempCallbackInfo.restype = POINTER(wkeTempCallbackInfo)

#void wkeOnCaretChanged(wkeWebView webView, wkeCaretChangedCallback callback, void* callbackParam)
#wkeCaretChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeRect)) 
#/*typedef void(WKE_CALL_TYPE*wkeCaretChangedCallback)(wkeWebView webView, void* param, const wkeRect* r);*/
wkeOnCaretChanged = mb.wkeOnCaretChanged
wkeOnCaretChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeRect)),c_void_p]


#void wkeOnMouseOverUrlChanged(wkeWebView webView, wkeTitleChangedCallback callback, void* callbackParam)
#wkeTitleChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p) 
#/*typedef void(WKE_CALL_TYPE*wkeTitleChangedCallback)(wkeWebView webView, void* param, const wkeString title);*/
wkeOnMouseOverUrlChanged = mb.wkeOnMouseOverUrlChanged
wkeOnMouseOverUrlChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p]


#void wkeOnTitleChanged(wkeWebView webView, wkeTitleChangedCallback callback, void* callbackParam)
#wkeTitleChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p) 
#/*typedef void(WKE_CALL_TYPE*wkeTitleChangedCallback)(wkeWebView webView, void* param, const wkeString title);*/
wkeOnTitleChanged = mb.wkeOnTitleChanged
wkeOnTitleChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p]


#void wkeOnURLChanged(wkeWebView webView, wkeURLChangedCallback callback, void* callbackParam)
#wkeURLChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p) 
#/*typedef void(WKE_CALL_TYPE*wkeURLChangedCallback)(wkeWebView webView, void* param, const wkeString url);*/
wkeOnURLChanged = mb.wkeOnURLChanged
wkeOnURLChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p]


#void wkeOnURLChanged2(wkeWebView webView, wkeURLChangedCallback2 callback, void* callbackParam)
#wkeURLChangedCallback2 CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_char_p) 
#/*typedef void(WKE_CALL_TYPE*wkeURLChangedCallback2)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, const wkeString url);*/
wkeOnURLChanged2 = mb.wkeOnURLChanged2
wkeOnURLChanged2.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_char_p),c_void_p]


#void wkeOnPaintUpdated(wkeWebView webView, wkePaintUpdatedCallback callback, void* callbackParam)
#wkePaintUpdatedCallback CFUNCTYPE(None,_LRESULT,c_void_p,_LRESULT,c_int,c_int,c_int,c_int) 
#/*typedef void(WKE_CALL_TYPE*wkePaintUpdatedCallback)(wkeWebView webView, void* param, const HDC hdc, int x, int y, int cx, int cy);*/
wkeOnPaintUpdated = mb.wkeOnPaintUpdated
wkeOnPaintUpdated.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,_LRESULT,c_int,c_int,c_int,c_int),c_void_p]


#void wkeOnPaintBitUpdated(wkeWebView webView, wkePaintBitUpdatedCallback callback, void* callbackParam)
#wkePaintBitUpdatedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeRect),c_int,c_int) 
#/*typedef void(WKE_CALL_TYPE*wkePaintBitUpdatedCallback)(wkeWebView webView, void* param, const void* buffer, const wkeRect* r, int width, int height);*/
wkeOnPaintBitUpdated = mb.wkeOnPaintBitUpdated
wkeOnPaintBitUpdated.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeRect),c_int,c_int),c_void_p]


#void wkeOnAlertBox(wkeWebView webView, wkeAlertBoxCallback callback, void* callbackParam)
#wkeAlertBoxCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p) 
#/*typedef void(WKE_CALL_TYPE*wkeAlertBoxCallback)(wkeWebView webView, void* param, const wkeString msg);*/
wkeOnAlertBox = mb.wkeOnAlertBox
wkeOnAlertBox.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p),c_void_p]


#void wkeOnConfirmBox(wkeWebView webView, wkeConfirmBoxCallback callback, void* callbackParam)
#wkeConfirmBoxCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p) 
#/*typedef bool(WKE_CALL_TYPE*wkeConfirmBoxCallback)(wkeWebView webView, void* param, const wkeString msg);*/
wkeOnConfirmBox = mb.wkeOnConfirmBox
wkeOnConfirmBox.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p),c_void_p]


#void wkeOnPromptBox(wkeWebView webView, wkePromptBoxCallback callback, void* callbackParam)
#wkePromptBoxCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_char_p,c_void_p) 
#/*typedef bool(WKE_CALL_TYPE*wkePromptBoxCallback)(wkeWebView webView, void* param, const wkeString msg, const wkeString defaultResult, wkeString result);*/
wkeOnPromptBox = mb.wkeOnPromptBox
wkeOnPromptBox.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_char_p,c_void_p),c_void_p]


#void wkeOnNavigation(wkeWebView webView, wkeNavigationCallback callback, void* param)
#wkeNavigationCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_char_p) 
#/*typedef bool(WKE_CALL_TYPE*wkeNavigationCallback)(wkeWebView webView, void* param, wkeNavigationType navigationType, wkeString url);*/
wkeOnNavigation = mb.wkeOnNavigation
wkeOnNavigation.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_char_p),c_void_p]


#void wkeOnCreateView(wkeWebView webView, wkeCreateViewCallback callback, void* param)
#wkeCreateViewCallback CFUNCTYPE(_LRESULT,_LRESULT,c_void_p,c_int,c_char_p,POINTER(wkeWindowFeatures)) 
#/*typedef wkeWebView(WKE_CALL_TYPE*wkeCreateViewCallback)(wkeWebView webView, void* param, wkeNavigationType navigationType, const wkeString url, const wkeWindowFeatures* windowFeatures);*/
wkeOnCreateView = mb.wkeOnCreateView
wkeOnCreateView.argtypes = [_LRESULT,CFUNCTYPE(_LRESULT,_LRESULT,c_void_p,c_int,c_char_p,POINTER(wkeWindowFeatures)),c_void_p]


#void wkeOnDocumentReady(wkeWebView webView, wkeDocumentReadyCallback callback, void* param)
#wkeDocumentReadyCallback CFUNCTYPE(None,_LRESULT,c_void_p) 
#/*typedef void(WKE_CALL_TYPE*wkeDocumentReadyCallback)(wkeWebView webView, void* param);*/
wkeOnDocumentReady = mb.wkeOnDocumentReady
wkeOnDocumentReady.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p]


#void wkeOnDocumentReady2(wkeWebView webView, wkeDocumentReady2Callback callback, void* param)
#wkeDocumentReady2Callback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p) 
#/*typedef void(WKE_CALL_TYPE*wkeDocumentReady2Callback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId);*/
wkeOnDocumentReady2 = mb.wkeOnDocumentReady2
wkeOnDocumentReady2.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p),c_void_p]


#void wkeOnLoadingFinish(wkeWebView webView, wkeLoadingFinishCallback callback, void* param)
#wkeLoadingFinishCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_int,c_char_p) 
#/*typedef void(WKE_CALL_TYPE*wkeLoadingFinishCallback)(wkeWebView webView, void* param, const wkeString url, wkeLoadingResult result, const wkeString failedReason);*/
wkeOnLoadingFinish = mb.wkeOnLoadingFinish
wkeOnLoadingFinish.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_int,c_char_p),c_void_p]


#void wkeOnDownload(wkeWebView webView, wkeDownloadCallback callback, void* param)
#wkeDownloadCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p) 
#/*typedef bool(WKE_CALL_TYPE*wkeDownloadCallback)(wkeWebView webView, void* param, const char* url);*/
wkeOnDownload = mb.wkeOnDownload
wkeOnDownload.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p),c_void_p]


#void wkeOnDownload2(wkeWebView webView, wkeDownload2Callback callback, void* param)
#wkeDownload2Callback CFUNCTYPE(wkeNetJobDataBind,_LRESULT,c_void_p,c_size_t,c_char_p,c_char_p,c_char_p,c_void_p,POINTER(wkeNetJobDataBind)) 
#/*typedef wkeDownloadOpt(WKE_CALL_TYPE*wkeDownload2Callback)(wkeWebView webView, void* param,size_t expectedContentLength,const char* url, const char* mime, const char* disposition, wkeNetJob job, wkeNetJobDataBind* dataBind);*/
wkeOnDownload2 = mb.wkeOnDownload2
wkeOnDownload2.argtypes = [_LRESULT,CFUNCTYPE(wkeNetJobDataBind,_LRESULT,c_void_p,c_size_t,c_char_p,c_char_p,c_char_p,c_void_p,POINTER(wkeNetJobDataBind)),c_void_p]


#void wkeOnConsole(wkeWebView webView, wkeConsoleCallback callback, void* param)
#wkeConsoleCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_uint,c_char_p,c_char_p,c_int,c_char_p) 
#/*typedef void(WKE_CALL_TYPE*wkeConsoleCallback)(wkeWebView webView, void* param, wkeConsoleLevel level, const wkeString message, const wkeString sourceName, unsigned sourceLine, const wkeString stackTrace);*/
wkeOnConsole = mb.wkeOnConsole
wkeOnConsole.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_uint,c_char_p,c_char_p,c_int,c_char_p),c_void_p]


#void wkeSetUIThreadCallback(wkeWebView webView, wkeCallUiThread callback, void* param)
#wkeCallUiThread CFUNCTYPE(None,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p) 
#/*typedef void(WKE_CALL_TYPE*wkeCallUiThread)(wkeWebView webView, wkeOnCallUiThread func, void* param);*/
wkeSetUIThreadCallback = mb.wkeSetUIThreadCallback
wkeSetUIThreadCallback.argtypes = [_LRESULT,CFUNCTYPE(None,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p),c_void_p]


#void wkeOnLoadUrlBegin(wkeWebView webView, wkeLoadUrlBeginCallback callback, void* callbackParam)
#wkeLoadUrlBeginCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p) 
#/*typedef bool(WKE_CALL_TYPE*wkeLoadUrlBeginCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/
wkeOnLoadUrlBegin = mb.wkeOnLoadUrlBegin
wkeOnLoadUrlBegin.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]


#void wkeOnLoadUrlEnd(wkeWebView webView, wkeLoadUrlEndCallback callback, void* callbackParam)
#wkeLoadUrlEndCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_int) 
#/*typedef void(WKE_CALL_TYPE*wkeLoadUrlEndCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job, void* buf, int len);*/
wkeOnLoadUrlEnd = mb.wkeOnLoadUrlEnd
wkeOnLoadUrlEnd.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_int),c_void_p]


#void wkeOnLoadUrlHeadersReceived(wkeWebView webView, wkeLoadUrlHeadersReceivedCallback callback, void* callbackParam)
#wkeLoadUrlHeadersReceivedCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p) 
#/*typedef void(WKE_CALL_TYPE*wkeLoadUrlHeadersReceivedCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/
wkeOnLoadUrlHeadersReceived = mb.wkeOnLoadUrlHeadersReceived
wkeOnLoadUrlHeadersReceived.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]


#void wkeOnLoadUrlFinish(wkeWebView webView, wkeLoadUrlFinishCallback callback, void* callbackParam)
#wkeLoadUrlFinishCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_int) 
#/*typedef void(WKE_CALL_TYPE*wkeLoadUrlFinishCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job, int len);*/
wkeOnLoadUrlFinish = mb.wkeOnLoadUrlFinish
wkeOnLoadUrlFinish.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_int),c_void_p]


#void wkeOnLoadUrlFail(wkeWebView webView, wkeLoadUrlFailCallback callback, void* callbackParam)
#wkeLoadUrlFailCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p) 
#/*typedef void(WKE_CALL_TYPE*wkeLoadUrlFailCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/
wkeOnLoadUrlFail = mb.wkeOnLoadUrlFail
wkeOnLoadUrlFail.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]


#void wkeOnDidCreateScriptContext(wkeWebView webView, wkeDidCreateScriptContextCallback callback, void* callbackParam)
#wkeDidCreateScriptContextCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int,c_int) 
#/*typedef void(WKE_CALL_TYPE*wkeDidCreateScriptContextCallback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, void* context, int extensionGroup, int worldId);*/
wkeOnDidCreateScriptContext = mb.wkeOnDidCreateScriptContext
wkeOnDidCreateScriptContext.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int,c_int),c_void_p]


#void wkeOnWillReleaseScriptContext(wkeWebView webView, wkeWillReleaseScriptContextCallback callback, void* callbackParam)
#wkeWillReleaseScriptContextCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int) 
#/*typedef void(WKE_CALL_TYPE*wkeWillReleaseScriptContextCallback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, void* context, int worldId);*/
wkeOnWillReleaseScriptContext = mb.wkeOnWillReleaseScriptContext
wkeOnWillReleaseScriptContext.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_int),c_void_p]


#void wkeOnWindowClosing(wkeWebView webWindow, wkeWindowClosingCallback callback, void* param)
#wkeWindowClosingCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p) 
#/*typedef bool(WKE_CALL_TYPE*wkeWindowClosingCallback)(wkeWebView webWindow, void* param);*/
wkeOnWindowClosing = mb.wkeOnWindowClosing
wkeOnWindowClosing.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p),c_void_p]


#void wkeOnWindowDestroy(wkeWebView webWindow, wkeWindowDestroyCallback callback, void* param)
#wkeWindowDestroyCallback CFUNCTYPE(None,_LRESULT,c_void_p) 
#/*typedef void(WKE_CALL_TYPE*wkeWindowDestroyCallback)(wkeWebView webWindow, void* param);*/
wkeOnWindowDestroy = mb.wkeOnWindowDestroy
wkeOnWindowDestroy.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p]


#void wkeOnDraggableRegionsChanged(wkeWebView webView, wkeDraggableRegionsChangedCallback callback, void* param)
#wkeDraggableRegionsChangedCallback CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeDraggableRegion),c_int) 
#/*typedef void(WKE_CALL_TYPE*wkeDraggableRegionsChangedCallback)(wkeWebView webView, void* param, const wkeDraggableRegion* rects, int rectCount);*/
wkeOnDraggableRegionsChanged = mb.wkeOnDraggableRegionsChanged
wkeOnDraggableRegionsChanged.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,POINTER(wkeDraggableRegion),c_int),c_void_p]


#void wkeOnWillMediaLoad(wkeWebView webView, wkeWillMediaLoadCallback callback, void* param)
#wkeWillMediaLoadCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMediaLoadInfo)) 
#/*typedef void(WKE_CALL_TYPE*wkeWillMediaLoadCallback)(wkeWebView webView, void* param, const char* url, wkeMediaLoadInfo* info);*/
wkeOnWillMediaLoad = mb.wkeOnWillMediaLoad
wkeOnWillMediaLoad.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMediaLoadInfo)),c_void_p]


#void wkeOnStartDragging(wkeWebView webView, wkeStartDraggingCallback callback, void* param)
#wkeStartDraggingCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeWebDragData),c_uint,c_void_p,POINTER(wkePoint)) 
#/*typedef void(WKE_CALL_TYPE*wkeStartDraggingCallback)(wkeWebView webView,void* param, wkeWebFrameHandle frame,const wkeWebDragData* data,wkeWebDragOperationsMask mask, const void* image, const wkePoint* dragImageOffset);*/
wkeOnStartDragging = mb.wkeOnStartDragging
wkeOnStartDragging.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeWebDragData),c_uint,c_void_p,POINTER(wkePoint)),c_void_p]


#void wkeOnPrint(wkeWebView webView, wkeOnPrintCallback callback, void* param)
#wkeOnPrintCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p) 
#/*typedef void(WKE_CALL_TYPE*wkeOnPrintCallback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, void* printParams);*/
wkeOnPrint = mb.wkeOnPrint
wkeOnPrint.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p),c_void_p]


#void wkeScreenshot(wkeWebView webView, const wkeScreenshotSettings* settings, wkeOnScreenshot callback, void* param)
#wkeOnScreenshot CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_size_t) 
#/*typedef void(WKE_CALL_TYPE*wkeOnScreenshot)(wkeWebView webView, void* param, const char* data, size_t size);typedef void(WKE_CALL_TYPE*wkeUiThreadRunCallback)(HWND hWnd, void* param);*/
wkeScreenshot = mb.wkeScreenshot
wkeScreenshot.argtypes = [_LRESULT,POINTER(wkeScreenshotSettings),CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_size_t),c_void_p]


#void wkeOnOtherLoad(wkeWebView webView, wkeOnOtherLoadCallback callback, void* param)
#wkeOnOtherLoadCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_int,POINTER(wkeTempCallbackInfo)) 
#/*typedef void(WKE_CALL_TYPE*wkeOnOtherLoadCallback)(wkeWebView webView, void* param, wkeOtherLoadType type, wkeTempCallbackInfo* info);*/
wkeOnOtherLoad = mb.wkeOnOtherLoad
wkeOnOtherLoad.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_int,POINTER(wkeTempCallbackInfo)),c_void_p]


#void wkeOnContextMenuItemClick(wkeWebView webView, wkeOnContextMenuItemClickCallback callback, void* param)
#wkeOnContextMenuItemClickCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_int,c_void_p,c_void_p) 
#/*typedef bool(WKE_CALL_TYPE* wkeOnContextMenuItemClickCallback)(wkeWebView webView, void* param, wkeOnContextMenuItemClickType type, wkeOnContextMenuItemClickStep step, wkeWebFrameHandle frameId,void* info);*/
wkeOnContextMenuItemClick = mb.wkeOnContextMenuItemClick
wkeOnContextMenuItemClick.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_int,c_void_p,c_void_p),c_void_p]


#BOOL wkeIsProcessingUserGesture(wkeWebView webView)
wkeIsProcessingUserGesture = mb.wkeIsProcessingUserGesture
wkeIsProcessingUserGesture.argtypes = [_LRESULT]
wkeIsProcessingUserGesture.restype = c_bool

#void wkeNetSetMIMEType(wkeNetJob jobPtr, const char* type)//设置response的mime
wkeNetSetMIMEType = mb.wkeNetSetMIMEType
wkeNetSetMIMEType.argtypes = [c_void_p,c_char_p]


#const char* wkeNetGetMIMEType(wkeNetJob jobPtr, wkeString mime)//获取response的mime
wkeNetGetMIMEType = mb.wkeNetGetMIMEType
wkeNetGetMIMEType.argtypes = [c_void_p,c_char_p]
wkeNetGetMIMEType.restype = c_char_p

#const char* wkeNetGetReferrer(wkeNetJob jobPtr)//获取request的referrer
wkeNetGetReferrer = mb.wkeNetGetReferrer
wkeNetGetReferrer.argtypes = [c_void_p]
wkeNetGetReferrer.restype = c_char_p

#void wkeNetSetHTTPHeaderField(wkeNetJob jobPtr, const wchar_t* key, const wchar_t* value, bool response)
wkeNetSetHTTPHeaderField = mb.wkeNetSetHTTPHeaderField
wkeNetSetHTTPHeaderField.argtypes = [c_void_p,c_wchar_p,c_wchar_p,c_bool]


#const char* wkeNetGetHTTPHeaderField(wkeNetJob jobPtr, const char* key)
wkeNetGetHTTPHeaderField = mb.wkeNetGetHTTPHeaderField
wkeNetGetHTTPHeaderField.argtypes = [c_void_p,c_char_p]
wkeNetGetHTTPHeaderField.restype = c_char_p

#const char* wkeNetGetHTTPHeaderFieldFromResponse(wkeNetJob jobPtr, const char* key)
wkeNetGetHTTPHeaderFieldFromResponse = mb.wkeNetGetHTTPHeaderFieldFromResponse
wkeNetGetHTTPHeaderFieldFromResponse.argtypes = [c_void_p,c_char_p]
wkeNetGetHTTPHeaderFieldFromResponse.restype = c_char_p


#void wkeNetSetData(wkeNetJob jobPtr, void* buf, int len)//此调用严重影响性能
wkeNetSetData = mb.wkeNetSetData
wkeNetSetData.argtypes = [c_void_p,c_void_p,c_int]


#void wkeNetHookRequest(wkeNetJob jobPtr)
wkeNetHookRequest = mb.wkeNetHookRequest
wkeNetHookRequest.argtypes = [c_void_p]


#void wkeNetOnResponse(wkeWebView webView, wkeNetResponseCallback callback, void* param)
#wkeNetResponseCallback CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p) 
#/*typedef bool(WKE_CALL_TYPE*wkeNetResponseCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/
wkeNetOnResponse = mb.wkeNetOnResponse
wkeNetOnResponse.argtypes = [_LRESULT,CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p),c_void_p]


#wkeRequestType wkeNetGetRequestMethod(wkeNetJob jobPtr)
wkeNetGetRequestMethod = mb.wkeNetGetRequestMethod
wkeNetGetRequestMethod.argtypes = [c_void_p]
wkeNetGetRequestMethod.restype = c_int

#int wkeNetGetFavicon(wkeWebView webView, wkeOnNetGetFaviconCallback callback, void* param)
#wkeOnNetGetFaviconCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMemBuf)) 
#/*typedef void(WKE_CALL_TYPE*wkeOnNetGetFaviconCallback)(wkeWebView webView, void* param, const utf8* url, wkeMemBuf* buf);*/
wkeNetGetFavicon = mb.wkeNetGetFavicon
wkeNetGetFavicon.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMemBuf)),c_void_p]
wkeNetGetFavicon.restype = c_int

#void wkeNetContinueJob(wkeNetJob jobPtr)
wkeNetContinueJob = mb.wkeNetContinueJob
wkeNetContinueJob.argtypes = [c_void_p]


#const char* wkeNetGetUrlByJob(wkeNetJob jobPtr)
wkeNetGetUrlByJob = mb.wkeNetGetUrlByJob
wkeNetGetUrlByJob.argtypes = [c_void_p]
wkeNetGetUrlByJob.restype = c_char_p

#const wkeSlist* wkeNetGetRawHttpHead(wkeNetJob jobPtr)
wkeNetGetRawHttpHead = mb.wkeNetGetRawHttpHead
wkeNetGetRawHttpHead.argtypes = [c_void_p]
wkeNetGetRawHttpHead.restype = POINTER(wkeSlist)

#const wkeSlist* wkeNetGetRawResponseHead(wkeNetJob jobPtr)
wkeNetGetRawResponseHead = mb.wkeNetGetRawResponseHead
wkeNetGetRawResponseHead.argtypes = [c_void_p]
wkeNetGetRawResponseHead.restype = POINTER(wkeSlist)

#void wkeNetCancelRequest(wkeNetJob jobPtr)
wkeNetCancelRequest = mb.wkeNetCancelRequest
wkeNetCancelRequest.argtypes = [c_void_p]


#BOOL wkeNetHoldJobToAsynCommit(wkeNetJob jobPtr)
wkeNetHoldJobToAsynCommit = mb.wkeNetHoldJobToAsynCommit
wkeNetHoldJobToAsynCommit.argtypes = [c_void_p]
wkeNetHoldJobToAsynCommit.restype = c_bool

#void wkeNetChangeRequestUrl(wkeNetJob jobPtr, const char* url)
wkeNetChangeRequestUrl = mb.wkeNetChangeRequestUrl
wkeNetChangeRequestUrl.argtypes = [c_void_p,c_char_p]


#wkeWebUrlRequestPtr wkeNetCreateWebUrlRequest(const utf8* url, const utf8* method, const utf8* mime)
wkeNetCreateWebUrlRequest = mb.wkeNetCreateWebUrlRequest
wkeNetCreateWebUrlRequest.argtypes = [c_char_p,c_char_p,c_char_p]
wkeNetCreateWebUrlRequest.restype = c_void_p

#wkeWebUrlRequestPtr wkeNetCreateWebUrlRequest2(const blinkWebURLRequestPtr request)
wkeNetCreateWebUrlRequest2 = mb.wkeNetCreateWebUrlRequest2
wkeNetCreateWebUrlRequest2.argtypes = [c_void_p]
wkeNetCreateWebUrlRequest2.restype = c_void_p

#blinkWebURLRequestPtr wkeNetCopyWebUrlRequest(wkeNetJob jobPtr, bool needExtraData)
wkeNetCopyWebUrlRequest = mb.wkeNetCopyWebUrlRequest
wkeNetCopyWebUrlRequest.argtypes = [c_void_p,c_bool]
wkeNetCopyWebUrlRequest.restype = c_void_p

#void wkeNetDeleteBlinkWebURLRequestPtr(blinkWebURLRequestPtr request)
wkeNetDeleteBlinkWebURLRequestPtr = mb.wkeNetDeleteBlinkWebURLRequestPtr
wkeNetDeleteBlinkWebURLRequestPtr.argtypes = [c_void_p]


#void wkeNetAddHTTPHeaderFieldToUrlRequest(wkeWebUrlRequestPtr request, const utf8* name, const utf8* value)
wkeNetAddHTTPHeaderFieldToUrlRequest = mb.wkeNetAddHTTPHeaderFieldToUrlRequest
wkeNetAddHTTPHeaderFieldToUrlRequest.argtypes = [c_void_p,c_char_p,c_char_p]


#int wkeNetStartUrlRequest(wkeWebView webView, wkeWebUrlRequestPtr request, void* param, const wkeUrlRequestCallbacks* callbacks)
wkeNetStartUrlRequest = mb.wkeNetStartUrlRequest
wkeNetStartUrlRequest.argtypes = [_LRESULT,c_void_p,c_void_p,POINTER(wkeUrlRequestCallbacks)]
wkeNetStartUrlRequest.restype = c_int

#int wkeNetGetHttpStatusCode(wkeWebUrlResponsePtr response)
wkeNetGetHttpStatusCode = mb.wkeNetGetHttpStatusCode
wkeNetGetHttpStatusCode.argtypes = [c_void_p]
wkeNetGetHttpStatusCode.restype = c_int

#__int64 wkeNetGetExpectedContentLength(wkeWebUrlResponsePtr response)
wkeNetGetExpectedContentLength = mb.wkeNetGetExpectedContentLength
wkeNetGetExpectedContentLength.argtypes = [c_void_p]
wkeNetGetExpectedContentLength.restype = c_longlong

#const utf8* wkeNetGetResponseUrl(wkeWebUrlResponsePtr response)
wkeNetGetResponseUrl = mb.wkeNetGetResponseUrl
wkeNetGetResponseUrl.argtypes = [c_void_p]
wkeNetGetResponseUrl.restype = c_char_p

#void wkeNetCancelWebUrlRequest(int requestId)
wkeNetCancelWebUrlRequest = mb.wkeNetCancelWebUrlRequest
wkeNetCancelWebUrlRequest.argtypes = [c_int]


#wkePostBodyElements* wkeNetGetPostBody(wkeNetJob jobPtr)
wkeNetGetPostBody = mb.wkeNetGetPostBody
wkeNetGetPostBody.argtypes = [c_void_p]
wkeNetGetPostBody.restype = POINTER(wkePostBodyElements)

#wkePostBodyElements* wkeNetCreatePostBodyElements(wkeWebView webView, size_t length)
wkeNetCreatePostBodyElements = mb.wkeNetCreatePostBodyElements
wkeNetCreatePostBodyElements.argtypes = [_LRESULT,_LRESULT]
wkeNetCreatePostBodyElements.restype = POINTER(wkePostBodyElements)

#void wkeNetFreePostBodyElements(wkePostBodyElements* elements)
wkeNetFreePostBodyElements = mb.wkeNetFreePostBodyElements
wkeNetFreePostBodyElements.argtypes = [POINTER(wkePostBodyElements)]


#wkePostBodyElement* wkeNetCreatePostBodyElement(wkeWebView webView)
wkeNetCreatePostBodyElement = mb.wkeNetCreatePostBodyElement
wkeNetCreatePostBodyElement.argtypes = [_LRESULT]
wkeNetCreatePostBodyElement.restype = POINTER(wkePostBodyElement)

#void wkeNetFreePostBodyElement(wkePostBodyElement* element)
wkeNetFreePostBodyElement = mb.wkeNetFreePostBodyElement
wkeNetFreePostBodyElement.argtypes = [POINTER(wkePostBodyElement)]


#BOOL wkeIsMainFrame(wkeWebView webView, wkeWebFrameHandle frameId)
wkeIsMainFrame = mb.wkeIsMainFrame
wkeIsMainFrame.argtypes = [_LRESULT,c_void_p]
wkeIsMainFrame.restype = c_bool

#BOOL wkeIsWebRemoteFrame(wkeWebView webView, wkeWebFrameHandle frameId)
wkeIsWebRemoteFrame = mb.wkeIsWebRemoteFrame
wkeIsWebRemoteFrame.argtypes = [_LRESULT,c_void_p]
wkeIsWebRemoteFrame.restype = c_bool

#wkeWebFrameHandle wkeWebFrameGetMainFrame(wkeWebView webView)
wkeWebFrameGetMainFrame = mb.wkeWebFrameGetMainFrame
wkeWebFrameGetMainFrame.argtypes = [_LRESULT]
wkeWebFrameGetMainFrame.restype = c_void_p

#jsValue wkeRunJsByFrame(wkeWebView webView, wkeWebFrameHandle frameId, const utf8* script, bool isInClosure)
wkeRunJsByFrame = mb.wkeRunJsByFrame
wkeRunJsByFrame.argtypes = [_LRESULT,c_void_p,c_char_p,c_bool]
wkeRunJsByFrame.restype = c_longlong

#void wkeInsertCSSByFrame(wkeWebView webView, wkeWebFrameHandle frameId, const utf8* cssText)
wkeInsertCSSByFrame = mb.wkeInsertCSSByFrame
wkeInsertCSSByFrame.argtypes = [_LRESULT,c_void_p,c_char_p]


#void wkeWebFrameGetMainWorldScriptContext(wkeWebView webView, wkeWebFrameHandle webFrameId, v8ContextPtr contextOut)
wkeWebFrameGetMainWorldScriptContext = mb.wkeWebFrameGetMainWorldScriptContext
wkeWebFrameGetMainWorldScriptContext.argtypes = [_LRESULT,c_void_p,c_void_p]


#v8Isolate wkeGetBlinkMainThreadIsolate()
wkeGetBlinkMainThreadIsolate = mb.wkeGetBlinkMainThreadIsolate
wkeGetBlinkMainThreadIsolate.argtypes = []
wkeGetBlinkMainThreadIsolate.restype = c_void_p

#wkeWebView wkeCreateWebWindow(wkeWindowType type, HWND parent, int x, int y, int width, int height)
wkeCreateWebWindow = mb.wkeCreateWebWindow
wkeCreateWebWindow.argtypes = [c_int,_LRESULT,c_int,c_int,c_int,c_int]
wkeCreateWebWindow.restype = _LRESULT

#wkeWebView wkeCreateWebCustomWindow(const wkeWindowCreateInfo* info)
wkeCreateWebCustomWindow = mb.wkeCreateWebCustomWindow
wkeCreateWebCustomWindow.argtypes = [POINTER(wkeWindowCreateInfo)]
wkeCreateWebCustomWindow.restype = _LRESULT

#void wkeDestroyWebWindow(wkeWebView webWindow)
wkeDestroyWebWindow = mb.wkeDestroyWebWindow
wkeDestroyWebWindow.argtypes = [_LRESULT]


#HWND wkeGetWindowHandle(wkeWebView webWindow)
wkeGetWindowHandle = mb.wkeGetWindowHandle
wkeGetWindowHandle.argtypes = [_LRESULT]
wkeGetWindowHandle.restype = _LRESULT

#void wkeShowWindow(wkeWebView webWindow, bool show)
wkeShowWindow = mb.wkeShowWindow
wkeShowWindow.argtypes = [_LRESULT,c_bool]


#void wkeEnableWindow(wkeWebView webWindow, bool enable)
wkeEnableWindow = mb.wkeEnableWindow
wkeEnableWindow.argtypes = [_LRESULT,c_bool]


#void wkeMoveWindow(wkeWebView webWindow, int x, int y, int width, int height)
wkeMoveWindow = mb.wkeMoveWindow
wkeMoveWindow.argtypes = [_LRESULT,c_int,c_int,c_int,c_int]


#void wkeMoveToCenter(wkeWebView webWindow)
wkeMoveToCenter = mb.wkeMoveToCenter
wkeMoveToCenter.argtypes = [_LRESULT]


#void wkeResizeWindow(wkeWebView webWindow, int width, int height)
wkeResizeWindow = mb.wkeResizeWindow
wkeResizeWindow.argtypes = [_LRESULT,c_int,c_int]


#wkeWebDragOperation wkeDragTargetDragEnter(wkeWebView webView, const wkeWebDragData* webDragData, const POINT* clientPoint, const POINT* screenPoint, wkeWebDragOperationsMask operationsAllowed, int modifiers)
wkeDragTargetDragEnter = mb.wkeDragTargetDragEnter
wkeDragTargetDragEnter.argtypes = [_LRESULT,POINTER(wkeWebDragData),POINTER(wkePoint),POINTER(wkePoint),c_int,c_int]
wkeDragTargetDragEnter.restype = c_int

#wkeWebDragOperation wkeDragTargetDragOver(wkeWebView webView, const POINT* clientPoint, const POINT* screenPoint, wkeWebDragOperationsMask operationsAllowed, int modifiers)
wkeDragTargetDragOver = mb.wkeDragTargetDragOver
wkeDragTargetDragOver.argtypes = [_LRESULT,POINTER(wkePoint),POINTER(wkePoint),c_int,c_int]
wkeDragTargetDragOver.restype = c_int

#void wkeDragTargetDragLeave(wkeWebView webView)
wkeDragTargetDragLeave = mb.wkeDragTargetDragLeave
wkeDragTargetDragLeave.argtypes = [_LRESULT]


#void wkeDragTargetDrop(wkeWebView webView, const POINT* clientPoint, const POINT* screenPoint, int modifiers)
wkeDragTargetDrop = mb.wkeDragTargetDrop
wkeDragTargetDrop.argtypes = [_LRESULT,POINTER(wkePoint),POINTER(wkePoint),c_int]


#void wkeDragTargetEnd(wkeWebView webView, const POINT* clientPoint, const POINT* screenPoint, wkeWebDragOperation operation)
wkeDragTargetEnd = mb.wkeDragTargetEnd
wkeDragTargetEnd.argtypes = [_LRESULT,POINTER(wkePoint),POINTER(wkePoint),c_int]


#void wkeUtilSetUiCallback(wkeUiThreadPostTaskCallback callback)
#wkeUiThreadPostTaskCallback CFUNCTYPE(c_int,_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p) 
#/*typedef int(WKE_CALL_TYPE*wkeUiThreadPostTaskCallback)(HWND hWnd, wkeUiThreadRunCallback callback, void* param);*/
wkeUtilSetUiCallback = mb.wkeUtilSetUiCallback
wkeUtilSetUiCallback.argtypes = [CFUNCTYPE(c_int,_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p),c_void_p)]


#const utf8* wkeUtilSerializeToMHTML(wkeWebView webView)
wkeUtilSerializeToMHTML = mb.wkeUtilSerializeToMHTML
wkeUtilSerializeToMHTML.argtypes = [_LRESULT]
wkeUtilSerializeToMHTML.restype = c_char_p

#const wkePdfDatas* wkeUtilPrintToPdf(wkeWebView webView, wkeWebFrameHandle frameId, const wkePrintSettings* settings)
wkeUtilPrintToPdf = mb.wkeUtilPrintToPdf
wkeUtilPrintToPdf.argtypes = [_LRESULT,c_void_p,POINTER(wkePrintSettings)]
wkeUtilPrintToPdf.restype = POINTER(wkePdfDatas)

#const wkeMemBuf* wkePrintToBitmap(wkeWebView webView, wkeWebFrameHandle frameId, const wkeScreenshotSettings* settings)
wkePrintToBitmap = mb.wkePrintToBitmap
wkePrintToBitmap.argtypes = [_LRESULT,c_void_p,POINTER(wkeScreenshotSettings)]
wkePrintToBitmap.restype = POINTER(wkeMemBuf)

#void wkeUtilRelasePrintPdfDatas(const wkePdfDatas* datas)
wkeUtilRelasePrintPdfDatas = mb.wkeUtilRelasePrintPdfDatas
wkeUtilRelasePrintPdfDatas.argtypes = [POINTER(wkePdfDatas)]


#void wkeSetWindowTitle(wkeWebView webWindow, const utf8* title)
wkeSetWindowTitle = mb.wkeSetWindowTitle
wkeSetWindowTitle.argtypes = [_LRESULT,c_char_p]


#void wkeSetWindowTitleW(wkeWebView webWindow, const wchar_t* title)
wkeSetWindowTitleW = mb.wkeSetWindowTitleW
wkeSetWindowTitleW.argtypes = [_LRESULT,c_wchar_p]


#void wkeNodeOnCreateProcess(wkeWebView webView, wkeNodeOnCreateProcessCallback callback, void* param)
#wkeNodeOnCreateProcessCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_wchar_p,c_wchar_p,POINTER(STARTUPINFOW)) 
#/*typedef void(__stdcall *wkeNodeOnCreateProcessCallback)(wkeWebView webView, void* param, const WCHAR* applicationPath, const WCHAR* arguments, STARTUPINFOW* startup);*/
wkeNodeOnCreateProcess = mb.wkeNodeOnCreateProcess
wkeNodeOnCreateProcess.argtypes = [_LRESULT,CFUNCTYPE(None,_LRESULT,c_void_p,c_wchar_p,c_wchar_p,POINTER(STARTUPINFOW)),c_void_p]


#void wkeOnPluginFind(wkeWebView webView, const char* mime, wkeOnPluginFindCallback callback, void* param)
#wkeOnPluginFindCallback CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_void_p) 
#/*typedef void(WKE_CALL_TYPE*wkeOnPluginFindCallback)(wkeWebView webView, void* param, const utf8* mime, void* initializeFunc, void* getEntryPointsFunc, void* shutdownFunc);*/
wkeOnPluginFind = mb.wkeOnPluginFind
wkeOnPluginFind.argtypes = [_LRESULT,c_char_p,CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_void_p),c_void_p]


#void wkeAddNpapiPlugin(wkeWebView webView, void* initializeFunc, void* getEntryPointsFunc, void* shutdownFunc)
wkeAddNpapiPlugin = mb.wkeAddNpapiPlugin
wkeAddNpapiPlugin.argtypes = [_LRESULT,c_void_p,c_void_p,c_void_p]


#void wkePluginListBuilderAddPlugin(void* builder, const utf8* name, const utf8* description, const utf8* fileName)
wkePluginListBuilderAddPlugin = mb.wkePluginListBuilderAddPlugin
wkePluginListBuilderAddPlugin.argtypes = [c_void_p,c_char_p,c_char_p,c_char_p]


#void wkePluginListBuilderAddMediaTypeToLastPlugin(void* builder, const utf8* name, const utf8* description)
wkePluginListBuilderAddMediaTypeToLastPlugin = mb.wkePluginListBuilderAddMediaTypeToLastPlugin
wkePluginListBuilderAddMediaTypeToLastPlugin.argtypes = [c_void_p,c_char_p,c_char_p]


#void wkePluginListBuilderAddFileExtensionToLastMediaType(void* builder, const utf8* fileExtension)
wkePluginListBuilderAddFileExtensionToLastMediaType = mb.wkePluginListBuilderAddFileExtensionToLastMediaType
wkePluginListBuilderAddFileExtensionToLastMediaType.argtypes = [c_void_p,c_char_p]


#wkeWebView wkeGetWebViewByNData(void* ndata)
wkeGetWebViewByNData = mb.wkeGetWebViewByNData
wkeGetWebViewByNData.argtypes = [c_void_p]
wkeGetWebViewByNData.restype = _LRESULT

#BOOL wkeRegisterEmbedderCustomElement(wkeWebView webView, wkeWebFrameHandle frameId, const char* name, void* options, void* outResult)
wkeRegisterEmbedderCustomElement = mb.wkeRegisterEmbedderCustomElement
wkeRegisterEmbedderCustomElement.argtypes = [_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p]
wkeRegisterEmbedderCustomElement.restype = c_bool

#void wkeSetMediaPlayerFactory(wkeWebView webView, wkeMediaPlayerFactory factory, wkeOnIsMediaPlayerSupportsMIMEType callback)
#wkeMediaPlayerFactory CFUNCTYPE(c_void_p,_LRESULT,c_void_p,c_void_p,c_void_p) 
#/*typedef wkeMediaPlayer(WKE_CALL_TYPE* wkeMediaPlayerFactory)(wkeWebView webView, wkeMediaPlayerClient client, void* npBrowserFuncs, void* npPluginFuncs); wkeMediaPlayerClient client unknow */
#wkeOnIsMediaPlayerSupportsMIMEType CFUNCTYPE(c_bool,c_char_p) 
#/*typedef bool(WKE_CALL_TYPE* wkeOnIsMediaPlayerSupportsMIMEType)(const utf8* mime);*/
wkeSetMediaPlayerFactory = mb.wkeSetMediaPlayerFactory
wkeSetMediaPlayerFactory.argtypes = [_LRESULT,CFUNCTYPE(c_void_p,_LRESULT,c_void_p,c_void_p,c_void_p),CFUNCTYPE(c_bool,c_char_p)]


#const utf8* wkeGetContentAsMarkup(wkeWebView webView, wkeWebFrameHandle frame, size_t* size)
wkeGetContentAsMarkup = mb.wkeGetContentAsMarkup
wkeGetContentAsMarkup.argtypes = [_LRESULT,c_void_p,POINTER(c_size_t)]
wkeGetContentAsMarkup.restype = c_char_p

#const utf8* wkeUtilDecodeURLEscape(const utf8* url)
wkeUtilDecodeURLEscape = mb.wkeUtilDecodeURLEscape
wkeUtilDecodeURLEscape.argtypes = [c_char_p]
wkeUtilDecodeURLEscape.restype = c_char_p

#const utf8* wkeUtilEncodeURLEscape(const utf8* url)
wkeUtilEncodeURLEscape = mb.wkeUtilEncodeURLEscape
wkeUtilEncodeURLEscape.argtypes = [c_char_p]
wkeUtilEncodeURLEscape.restype = c_char_p

#const utf8* wkeUtilBase64Encode(const utf8* str)
wkeUtilBase64Encode = mb.wkeUtilBase64Encode
wkeUtilBase64Encode.argtypes = [c_char_p]
wkeUtilBase64Encode.restype = c_char_p

#const utf8* wkeUtilBase64Decode(const utf8* str)
wkeUtilBase64Decode = mb.wkeUtilBase64Decode
wkeUtilBase64Decode.argtypes = [c_char_p]
wkeUtilBase64Decode.restype = c_char_p

#const wkeMemBuf* wkeUtilCreateV8Snapshot(const utf8* str)
wkeUtilCreateV8Snapshot = mb.wkeUtilCreateV8Snapshot
wkeUtilCreateV8Snapshot.argtypes = [c_char_p]
wkeUtilCreateV8Snapshot.restype = POINTER(wkeMemBuf)

#void wkeRunMessageLoop()
wkeRunMessageLoop = mb.wkeRunMessageLoop
wkeRunMessageLoop.argtypes = []


#void wkeSaveMemoryCache(wkeWebView webView)
wkeSaveMemoryCache = mb.wkeSaveMemoryCache
wkeSaveMemoryCache.argtypes = [_LRESULT]


#void jsBindFunction(const char* name, jsNativeFunction fn, unsigned int argCount)
#jsNativeFunction CFUNCTYPE(c_longlong,c_void_p) 
#/*typedef jsValue(JS_CALL* jsNativeFunction) (jsExecState es);*/
jsBindFunction = mb.jsBindFunction
jsBindFunction.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p),c_uint]


#void jsBindGetter(const char* name, jsNativeFunction fn)
#jsNativeFunction CFUNCTYPE(c_longlong,c_void_p) 
#/*typedef jsValue(JS_CALL* jsNativeFunction) (jsExecState es);*/
jsBindGetter = mb.jsBindGetter
jsBindGetter.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p)]


#void jsBindSetter(const char* name, jsNativeFunction fn)
#jsNativeFunction CFUNCTYPE(c_longlong,c_void_p) 
#/*typedef jsValue(JS_CALL* jsNativeFunction) (jsExecState es);*/
jsBindSetter = mb.jsBindSetter
jsBindSetter.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p)]


#void wkeJsBindFunction(const char* name, wkeJsNativeFunction fn, void* param, unsigned int argCount)
#wkeJsNativeFunction CFUNCTYPE(c_longlong,c_void_p,c_void_p) 
#/*typedef jsValue(WKE_CALL_TYPE* wkeJsNativeFunction) (jsExecState es, void* param);*/
wkeJsBindFunction = mb.wkeJsBindFunction
wkeJsBindFunction.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p,c_void_p),c_void_p,c_uint]


#void wkeJsBindGetter(const char* name, wkeJsNativeFunction fn, void* param)
#wkeJsNativeFunction CFUNCTYPE(c_longlong,c_void_p,c_void_p) 
#/*typedef jsValue(WKE_CALL_TYPE* wkeJsNativeFunction) (jsExecState es, void* param);*/
wkeJsBindGetter = mb.wkeJsBindGetter
wkeJsBindGetter.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p,c_void_p),c_void_p]


#void wkeJsBindSetter(const char* name, wkeJsNativeFunction fn, void* param)
#wkeJsNativeFunction CFUNCTYPE(c_longlong,c_void_p,c_void_p) 
#/*typedef jsValue(WKE_CALL_TYPE* wkeJsNativeFunction) (jsExecState es, void* param);*/
wkeJsBindSetter = mb.wkeJsBindSetter
wkeJsBindSetter.argtypes = [c_char_p,CFUNCTYPE(c_longlong,c_void_p,c_void_p),c_void_p]


#int jsArgCount(jsExecState es)
jsArgCount = mb.jsArgCount
jsArgCount.argtypes = [c_void_p]
jsArgCount.restype = c_int

#jsType jsArgType(jsExecState es, int argIdx)
jsArgType = mb.jsArgType
jsArgType.argtypes = [c_void_p,c_int]
jsArgType.restype = c_int

#jsValue jsArg(jsExecState es, int argIdx)
jsArg = mb.jsArg
jsArg.argtypes = [c_void_p,c_int]
jsArg.restype = c_longlong

#jsType jsTypeOf(jsValue v)
jsTypeOf = mb.jsTypeOf
jsTypeOf.argtypes = [c_longlong]
jsTypeOf.restype = c_int

#BOOL jsIsNumber(jsValue v)
jsIsNumber = mb.jsIsNumber
jsIsNumber.argtypes = [c_longlong]
jsIsNumber.restype = c_bool

#BOOL jsIsString(jsValue v)
jsIsString = mb.jsIsString
jsIsString.argtypes = [c_longlong]
jsIsString.restype = c_bool

#BOOL jsIsBoolean(jsValue v)
jsIsBoolean = mb.jsIsBoolean
jsIsBoolean.argtypes = [c_longlong]
jsIsBoolean.restype = c_bool

#BOOL jsIsObject(jsValue v)
jsIsObject = mb.jsIsObject
jsIsObject.argtypes = [c_longlong]
jsIsObject.restype = c_bool

#BOOL jsIsFunction(jsValue v)
jsIsFunction = mb.jsIsFunction
jsIsFunction.argtypes = [c_longlong]
jsIsFunction.restype = c_bool

#BOOL jsIsUndefined(jsValue v)
jsIsUndefined = mb.jsIsUndefined
jsIsUndefined.argtypes = [c_longlong]
jsIsUndefined.restype = c_bool

#BOOL jsIsNull(jsValue v)
jsIsNull = mb.jsIsNull
jsIsNull.argtypes = [c_longlong]
jsIsNull.restype = c_bool

#BOOL jsIsArray(jsValue v)
jsIsArray = mb.jsIsArray
jsIsArray.argtypes = [c_longlong]
jsIsArray.restype = c_bool

#BOOL jsIsTrue(jsValue v)
jsIsTrue = mb.jsIsTrue
jsIsTrue.argtypes = [c_longlong]
jsIsTrue.restype = c_bool

#BOOL jsIsFalse(jsValue v)
jsIsFalse = mb.jsIsFalse
jsIsFalse.argtypes = [c_longlong]
jsIsFalse.restype = c_bool

#int jsToInt(jsExecState es, jsValue v)
jsToInt = mb.jsToInt
jsToInt.argtypes = [c_void_p,c_longlong]
jsToInt.restype = c_int

#float jsToFloat(jsExecState es, jsValue v)
jsToFloat = mb.jsToFloat
jsToFloat.argtypes = [c_void_p,c_longlong]
jsToFloat.restype = c_float

#double jsToDouble(jsExecState es, jsValue v)
jsToDouble = mb.jsToDouble
jsToDouble.argtypes = [c_void_p,c_longlong]
jsToDouble.restype = c_double

#const char* jsToDoubleString(jsExecState es, jsValue v)
jsToDoubleString = mb.jsToDoubleString
jsToDoubleString.argtypes = [c_void_p,c_longlong]
jsToDoubleString.restype = c_char_p

#BOOL jsToBoolean(jsExecState es, jsValue v)
jsToBoolean = mb.jsToBoolean
jsToBoolean.argtypes = [c_void_p,c_longlong]
jsToBoolean.restype = c_bool

#jsValue jsArrayBuffer(jsExecState es, const char* buffer, size_t size)
jsArrayBuffer = mb.jsArrayBuffer
jsArrayBuffer.argtypes = [c_void_p,c_char_p,_LRESULT]
jsArrayBuffer.restype = c_longlong

#wkeMemBuf* jsGetArrayBuffer(jsExecState es, jsValue value)
jsGetArrayBuffer = mb.jsGetArrayBuffer
jsGetArrayBuffer.argtypes = [c_void_p,c_longlong]
jsGetArrayBuffer.restype = POINTER(wkeMemBuf)

#const utf8* jsToTempString(jsExecState es, jsValue v)
jsToTempString = mb.jsToTempString
jsToTempString.argtypes = [c_void_p,c_longlong]
jsToTempString.restype = c_char_p

#const wchar_t* jsToTempStringW(jsExecState es, jsValue v)
jsToTempStringW = mb.jsToTempStringW
jsToTempStringW.argtypes = [c_void_p,c_longlong]
jsToTempStringW.restype = c_wchar_p

#void* jsToV8Value(jsExecState es, jsValue v)//return v8::Persistent<v8::Value>*
jsToV8Value = mb.jsToV8Value
jsToV8Value.argtypes = [c_void_p,c_longlong]
jsToV8Value.restype = c_void_p

#jsValue jsInt(int n)
jsInt = mb.jsInt
jsInt.argtypes = [c_int]
jsInt.restype = c_longlong

#jsValue jsFloat(float f)
jsFloat = mb.jsFloat
jsFloat.argtypes = [c_float]
jsFloat.restype = c_longlong

#jsValue jsDouble(double d)
jsDouble = mb.jsDouble
jsDouble.argtypes = [c_double]
jsDouble.restype = c_longlong

#jsValue jsDoubleString(const char* str)
jsDoubleString = mb.jsDoubleString
jsDoubleString.argtypes = [c_char_p]
jsDoubleString.restype = c_longlong

#jsValue jsBoolean(bool b)
jsBoolean = mb.jsBoolean
jsBoolean.argtypes = [c_bool]
jsBoolean.restype = c_longlong

#jsValue jsUndefined()
jsUndefined = mb.jsUndefined
jsUndefined.argtypes = []
jsUndefined.restype = c_longlong

#jsValue jsNull()
jsNull = mb.jsNull
jsNull.argtypes = []
jsNull.restype = c_longlong

#jsValue jsTrue()
jsTrue = mb.jsTrue
jsTrue.argtypes = []
jsTrue.restype = c_longlong

#jsValue jsFalse()
jsFalse = mb.jsFalse
jsFalse.argtypes = []
jsFalse.restype = c_longlong

#jsValue jsString(jsExecState es, const utf8* str)
jsString = mb.jsString
jsString.argtypes = [c_void_p,c_char_p]
jsString.restype = c_longlong

#jsValue jsStringW(jsExecState es, const wchar_t* str)
jsStringW = mb.jsStringW
jsStringW.argtypes = [c_void_p,c_wchar_p]
jsStringW.restype = c_longlong

#jsValue jsEmptyObject(jsExecState es)
jsEmptyObject = mb.jsEmptyObject
jsEmptyObject.argtypes = [c_void_p]
jsEmptyObject.restype = c_longlong

#jsValue jsEmptyArray(jsExecState es)
jsEmptyArray = mb.jsEmptyArray
jsEmptyArray.argtypes = [c_void_p]
jsEmptyArray.restype = c_longlong

#jsValue jsObject(jsExecState es, jsData* obj)
jsObject = mb.jsObject
jsObject.argtypes = [c_void_p,POINTER(wkeJsData)]
jsObject.restype = c_longlong

#jsValue jsFunction(jsExecState es, jsData* obj)
jsFunction = mb.jsFunction
jsFunction.argtypes = [c_void_p,POINTER(wkeJsData)]
jsFunction.restype = c_longlong

#jsData* jsGetData(jsExecState es, jsValue object)
jsGetData = mb.jsGetData
jsGetData.argtypes = [c_void_p,c_longlong]
jsGetData.restype = POINTER(wkeJsData)

#jsValue jsGet(jsExecState es, jsValue object, const char* prop)
jsGet = mb.jsGet
jsGet.argtypes = [c_void_p,c_longlong,c_char_p]
jsGet.restype = c_longlong

#void jsSet(jsExecState es, jsValue object, const char* prop, jsValue v)
jsSet = mb.jsSet
jsSet.argtypes = [c_void_p,c_longlong,c_char_p,c_longlong]


#jsValue jsGetAt(jsExecState es, jsValue object, int index)
jsGetAt = mb.jsGetAt
jsGetAt.argtypes = [c_void_p,c_longlong,c_int]
jsGetAt.restype = c_longlong

#void jsSetAt(jsExecState es, jsValue object, int index, jsValue v)
jsSetAt = mb.jsSetAt
jsSetAt.argtypes = [c_void_p,c_longlong,c_int,c_longlong]


#jsKeys* jsGetKeys(jsExecState es, jsValue object)
jsGetKeys = mb.jsGetKeys
jsGetKeys.argtypes = [c_void_p,c_longlong]
jsGetKeys.restype = POINTER(wkeJsKeys)

#BOOL jsIsJsValueValid(jsExecState es, jsValue object)
jsIsJsValueValid = mb.jsIsJsValueValid
jsIsJsValueValid.argtypes = [c_void_p,c_longlong]
jsIsJsValueValid.restype = c_bool

#BOOL jsIsValidExecState(jsExecState es)
jsIsValidExecState = mb.jsIsValidExecState
jsIsValidExecState.argtypes = [c_void_p]
jsIsValidExecState.restype = c_bool

#void jsDeleteObjectProp(jsExecState es, jsValue object, const char* prop)
jsDeleteObjectProp = mb.jsDeleteObjectProp
jsDeleteObjectProp.argtypes = [c_void_p,c_longlong,c_char_p]


#int jsGetLength(jsExecState es, jsValue object)
jsGetLength = mb.jsGetLength
jsGetLength.argtypes = [c_void_p,c_longlong]
jsGetLength.restype = c_int

#void jsSetLength(jsExecState es, jsValue object, int length)
jsSetLength = mb.jsSetLength
jsSetLength.argtypes = [c_void_p,c_longlong,c_int]


#jsValue jsGlobalObject(jsExecState es)
jsGlobalObject = mb.jsGlobalObject
jsGlobalObject.argtypes = [c_void_p]
jsGlobalObject.restype = c_longlong

#wkeWebView jsGetWebView(jsExecState es)
jsGetWebView = mb.jsGetWebView
jsGetWebView.argtypes = [c_void_p]
jsGetWebView.restype = _LRESULT

#jsValue jsEval(jsExecState es, const utf8* str)
jsEval = mb.jsEval
jsEval.argtypes = [c_void_p,c_char_p]
jsEval.restype = c_longlong

#jsValue jsEvalW(jsExecState es, const wchar_t* str)
jsEvalW = mb.jsEvalW
jsEvalW.argtypes = [c_void_p,c_wchar_p]
jsEvalW.restype = c_longlong

#jsValue jsEvalExW(jsExecState es, const wchar_t* str, bool isInClosure)
jsEvalExW = mb.jsEvalExW
jsEvalExW.argtypes = [c_void_p,c_wchar_p,c_bool]
jsEvalExW.restype = c_longlong

#jsValue jsCall(jsExecState es, jsValue func, jsValue thisObject, jsValue* args, int argCount)
jsCall = mb.jsCall
jsCall.argtypes = [c_void_p,c_longlong,c_longlong,POINTER(c_longlong),c_int]
jsCall.restype = c_longlong

#jsValue jsCallGlobal(jsExecState es, jsValue func, jsValue* args, int argCount)
jsCallGlobal = mb.jsCallGlobal
jsCallGlobal.argtypes = [c_void_p,c_longlong,POINTER(c_longlong),c_int]
jsCallGlobal.restype = c_longlong

#jsValue jsGetGlobal(jsExecState es, const char* prop)
jsGetGlobal = mb.jsGetGlobal
jsGetGlobal.argtypes = [c_void_p,c_char_p]
jsGetGlobal.restype = c_longlong

#void jsSetGlobal(jsExecState es, const char* prop, jsValue v)
jsSetGlobal = mb.jsSetGlobal
jsSetGlobal.argtypes = [c_void_p,c_char_p,c_longlong]


#void jsGC()
jsGC = mb.jsGC
jsGC.argtypes = []


#BOOL jsAddRef(jsExecState es, jsValue val)
jsAddRef = mb.jsAddRef
jsAddRef.argtypes = [c_void_p,c_longlong]
jsAddRef.restype = c_bool

#BOOL jsReleaseRef(jsExecState es, jsValue val)
jsReleaseRef = mb.jsReleaseRef
jsReleaseRef.argtypes = [c_void_p,c_longlong]
jsReleaseRef.restype = c_bool

#jsExceptionInfo* jsGetLastErrorIfException(jsExecState es)
jsGetLastErrorIfException = mb.jsGetLastErrorIfException
jsGetLastErrorIfException.argtypes = [c_void_p]
jsGetLastErrorIfException.restype = POINTER(wkeJsExceptionInfo)

#jsValue jsThrowException(jsExecState es, const utf8* exception)
jsThrowException = mb.jsThrowException
jsThrowException.argtypes = [c_void_p,c_char_p]
jsThrowException.restype = c_longlong

#const utf8* jsGetCallstack(jsExecState es)
jsGetCallstack = mb.jsGetCallstack
jsGetCallstack.argtypes = [c_void_p]
jsGetCallstack.restype = c_char_p









