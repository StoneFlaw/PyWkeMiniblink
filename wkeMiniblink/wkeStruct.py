# -*- coding:utf-8 -*-
import enum
from platform import architecture

from ctypes import (
    c_int,
    c_uint,
    c_ushort,
    c_long,
    c_longlong,
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
    CFUNCTYPE
    )

from ctypes.wintypes import (
    LPARAM,
    DWORD,
    LONG,
    WORD,
    BYTE
)
from ctypes import wintypes



_LRESULT=c_int
bit=architecture()[0]

miniblink_core_dll = '\\miniblink.dll'
if bit == '64bit':
    _LRESULT=c_longlong
else:
    _LRESULT=c_int

class wkeMouseFlags(enum.IntEnum):
    WKE_LBUTTON = 0x01
    WKE_RBUTTON = 0x02
    WKE_SHIFT = 0x04
    WKE_CONTROL = 0x08
    WKE_MBUTTON = 0x10


class wkeKeyFlags(enum.IntEnum):
    WKE_EXTENDED = 0x0100,
    WKE_REPEAT = 0x4000,

class wkeMouseMsg(enum.IntEnum):
    WKE_MSG_MOUSEMOVE = 0x0200
    WKE_MSG_LBUTTONDOWN = 0x0201
    WKE_MSG_LBUTTONUP = 0x0202
    WKE_MSG_LBUTTONDBLCLK = 0x0203
    WKE_MSG_RBUTTONDOWN = 0x0204
    WKE_MSG_RBUTTONUP = 0x0205
    WKE_MSG_RBUTTONDBLCLK = 0x0206
    WKE_MSG_MBUTTONDOWN = 0x0207
    WKE_MSG_MBUTTONUP = 0x0208
    WKE_MSG_MBUTTONDBLCLK = 0x0209
    WKE_MSG_MOUSEWHEEL = 0x020A

class wkeProxyType (enum.IntEnum):
    WKE_PROXY_NONE=0
    WKE_PROXY_HTTP=1
    WKE_PROXY_SOCKS4=2
    WKE_PROXY_SOCKS4A=3
    WKE_PROXY_SOCKS5=4
    WKE_PROXY_SOCKS5HOSTNAME=5

class wkeNavigationType (enum.IntEnum):
    WKE_NAVIGATION_TYPE_LINKCLICK=0
    WKE_NAVIGATION_TYPE_FORMSUBMITTE=1
    WKE_NAVIGATION_TYPE_BACKFORWARD=2
    WKE_NAVIGATION_TYPE_RELOAD=3
    WKE_NAVIGATION_TYPE_FORMRESUBMITT=4
    WKE_NAVIGATION_TYPE_OTHER=5


class WkeConst():
    GWL_EXSTYLE = -20
    GWL_USERDATA = -21
    GWL_WNDPROC = -4
    WS_EX_LAYERED = 0x80000
    WM_PAINT = 15
    WM_ERASEBKGND = 20
    WM_SIZE = 5
    WM_KEYDOWN = 256
    WM_KEYUP = 257
    WM_CHAR = 258
    WM_LBUTTONDOWN = 513
    WM_LBUTTONUP = 514
    WM_MBUTTONDOWN = 519
    WM_RBUTTONDOWN = 516
    WM_LBUTTONDBLCLK = 515
    WM_MBUTTONDBLCLK = 521
    WM_RBUTTONDBLCLK = 518
    WM_MBUTTONUP = 520
    WM_RBUTTONUP = 517
    WM_MOUSEMOVE = 512
    WM_CONTEXTMENU = 123
    WM_MOUSEWHEEL = 522
    WM_SETFOCUS = 7
    WM_KILLFOCUS = 8
    WM_IME_STARTCOMPOSITION = 269
    WM_NCHITTEST = 132
    WM_GETMINMAXINFO = 36
    WM_DESTROY = 2
    WM_SETCURSOR = 32
    MK_CONTROL = 8
    MK_SHIFT = 4
    MK_LBUTTON = 1
    MK_MBUTTON = 16
    MK_RBUTTON = 2
    KF_REPEAT = 16384
    KF_EXTENDED = 256
    SRCCOPY = 13369376
    CAPTUREBLT = 1073741824
    CFS_POINT = 2
    CFS_FORCE_POSITION = 32
    OBJ_BITMAP = 7
    AC_SRC_OVER = 0
    AC_SRC_ALPHA = 1
    ULW_ALPHA = 2
    WM_INPUTLANGCHANGE = 81
    WM_NCDESTROY = 130
    IMAGE_ICON=1
    LR_LOADFROMFILE=16
    WM_SETICON=128
    ICON_SMALL=0
    ICON_BIG=1
    IMAGE_ICON = 1
    LR_CREATEDIBSECTION = 0x00002000
    SRCCOPY = 13369376
    IDC_SIZENS=32645
    IDC_SIZEWE=32644
    IDC_SIZENWSE=32642
    IDC_SIZENESW=32643
    
class STARTUPINFOW(Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", wintypes.LPBYTE),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]

class wkeProxy(Structure):

    _fields_ = [('type', c_int),('hostname', c_char *100),('port', c_ushort ),('username', c_char *50),('password',c_char *50)]
class wkePoint(Structure):

    _fields_=[('x',c_int),('y',c_int)]
class wkeRect(Structure):

    _fields_=[('x',c_int),('y',c_int),('w',c_int),('h',c_int)]
class wkeMemBuf(Structure):

    _fields_=[('size',c_int),('data',c_char_p),('length',c_size_t)]

class wkePostBodyElement(Structure):

    _fields_=[('size',c_int),('type',c_int),('data',POINTER(wkeMemBuf)),('filePath',c_char_p),('fileStart',c_longlong),('fileLength',c_longlong)]
    
class wkePostBodyElements(Structure):

    _fields_ =[('size',c_int),('element',POINTER(POINTER(wkePostBodyElement))),('elementSize',c_size_t),('isDirty',c_bool)]
    
class wkeScreenshotSettings(Structure):

    _fields_=[('structSize',c_int),('width',c_int),('height',c_int)]
class wkeWindowFeatures(Structure):

    _fields_=[('x',c_int),('y',c_int),('width',c_int),('height',c_int),('menuBarVisible',c_bool),('statusBarVisible',c_bool),('toolBarVisible',c_bool),('locationBarVisible',c_bool),('scrollbarsVisible',c_bool),('resizable',c_bool),('fullscreen',c_bool)]

class wkePrintSettings(Structure):

    _fields_=[('structSize',c_int),('dpi',c_int),('width',c_int),('height',c_int),('marginTop',c_int),('marginBottom',c_int),('marginLeft',c_int),('marginRight',c_int),('isPrintPageHeadAndFooter',c_bool),('isPrintBackgroud',c_bool),('isLandscape',c_bool)]

class wkePdfDatas(Structure):
    _fields_=[('count',c_int),('sizes',c_size_t),('datas',c_void_p)]


class wkeClientHandle(Structure):
    #typedef void(WKE_CALL_TYPE *ON_TITLE_CHANGED) (const struct _wkeClientHandler* clientHandler, const wkeString title);
    #typedef void(WKE_CALL_TYPE *ON_URL_CHANGED) (const struct _wkeClientHandler* clientHandler, const wkeString url);
    _fields_=[('onTitleChanged',CFUNCTYPE(None,c_void_p,c_char_p)),('onURLChanged',CFUNCTYPE(None,c_void_p,c_char_p))]    

class wkeSlist(Structure):
    '''
    char* data;
    struct _wkeSlist* next;
    '''
    _fields_=[('data',c_char_p),('next',POINTER(c_void_p))]  
    
class wkeSettings(Structure):
    '''
    wkeProxy proxy;
    unsigned int mask;
    const char* extension;
    '''
    _fields_=[('proxy',wkeProxy),('mask',c_uint),('extension',c_char_p)]

class wkeViewSettings(Structure):
    '''
    int size;
    unsigned int bgColor;
    '''
    _fields_=[('size',c_int),('bgColor',c_uint)]

class wkePrintSettings(Structure):
    '''struct _wkePrintSettings {
    int structSize;
    int dpi;
    int width; // in px
    int height;
    int marginTop;
    int marginBottom;
    int marginLeft;
    int marginRight;
    BOOL isPrintPageHeadAndFooter;
    BOOL isPrintBackgroud;
    BOOL isLandscape;
    BOOL isPrintToMultiPage;
} wkePrintSettings;
'''
    _fields_=[('structSize',c_int),('dpi',c_int),('width',c_int),('height',c_int),
              ('marginTop',c_int),('marginBottom',c_int),('marginLeft',c_int),('marginRight',c_int),
              ('isPrintPageHeadAndFooter',c_bool),('isPrintBackgroud',c_bool),('isLandscape',c_bool),('isPrintToMultiPage',c_bool)]

class wkePostBodyElement(Structure):
    '''
    typedef struct _wkePostBodyElement {
        int size;
        wkeHttBodyElementType type;
        wkeMemBuf* data;
        wkeString filePath;
        __int64 fileStart;
        __int64 fileLength; // -1 means to the end of the file.
    } wkePostBodyElement;
    '''
    _fields_=[('size',c_int),('type',c_int),('data',POINTER(wkeMemBuf)),('filePath',c_char_p),('fileStart',c_longlong),('fileLength',c_longlong)]

class wkePostBodyElements(Structure):
    '''
    typedef struct _wkePostBodyElements {
        int size;
        wkePostBodyElement** element;
        size_t elementSize;
        bool isDirty;
    } wkePostBodyElements;
    '''
    _fields_=[('size',c_int),('element',POINTER(POINTER(wkePostBodyElement))),('elementSize',c_int),('isDirty',c_bool)]

class wkeWindowCreateInfo(Structure):
    '''
    typedef struct _wkeWindowCreateInfo {
        int size;
        HWND parent;
        DWORD style; 
        DWORD styleEx; 
        int x; 
        int y; 
        int width; 
        int height;
        COLORREF color; /*typedef DWORD COLORREF;*/
    } wkeWindowCreateInfo;
'''
    _fields_=[('size',c_int),('parent',_LRESULT),('style',c_uint),('styleEx',c_uint),('x',c_int),('y',c_int),('width',c_int),('height',c_int),('color',c_uint)]

class wkeWebDragDataItem(Structure):
    '''
    '''   
    _fields_=[('storageType',c_int),
              ('stringType',POINTER(wkeMemBuf)),
              ('stringData',POINTER(wkeMemBuf)),
              ('filenameData',POINTER(wkeMemBuf)),
              ('displayNameData',POINTER(wkeMemBuf)),
              ('binaryData',POINTER(wkeMemBuf)),
              ('title',POINTER(wkeMemBuf)),
              ('fileSystemURL',POINTER(wkeMemBuf)),
              ('fileSystemFileSize',c_longlong),
              ('baseURL',POINTER(wkeMemBuf))]

class wkeWebDragData(Structure):
    '''
    typedef struct _wkeWebDragData {
        struct Item {
            enum wkeStorageType {
                // String data with an associated MIME type. Depending on the MIME type, there may be
                // optional metadata attributes as well.
                StorageTypeString,
                // Stores the name of one file being dragged into the renderer.
                StorageTypeFilename,
                // An image being dragged out of the renderer. Contains a buffer holding the image data
                // as well as the suggested name for saving the image to.
                StorageTypeBinaryData,
                // Stores the filesystem URL of one file being dragged into the renderer.
                StorageTypeFileSystemFile,
            } storageType;

            // Only valid when storageType == StorageTypeString.
            wkeMemBuf* stringType;
            wkeMemBuf* stringData;

            // Only valid when storageType == StorageTypeFilename.
            wkeMemBuf* filenameData;
            wkeMemBuf* displayNameData;

            // Only valid when storageType == StorageTypeBinaryData.
            wkeMemBuf* binaryData;

            // Title associated with a link when stringType == "text/uri-list".
            // Filename when storageType == StorageTypeBinaryData.
            wkeMemBuf* title;

            // Only valid when storageType == StorageTypeFileSystemFile.
            wkeMemBuf* fileSystemURL;
            __int64 fileSystemFileSize;

            // Only valid when stringType == "text/html".
            wkeMemBuf* baseURL;
        };

        struct Item* m_itemList;
        int m_itemListLength;

        int m_modifierKeyState; // State of Shift/Ctrl/Alt/Meta keys.
        wkeMemBuf* m_filesystemId;
    } wkeWebDragData;
    '''
    _fields_=[('Item',wkeWebDragDataItem),       
              ('m_itemList',POINTER(wkeWebDragDataItem)),
              ('m_itemListLength',c_int),            
              ('m_modifierKeyState',c_int),   
              ('m_filesystemId',POINTER(wkeMemBuf))
              ]
    
class wkeJsData(Structure):
    '''
    typedef struct tagjsData {
        char typeName[100];
        jsGetPropertyCallback propertyGet;
        jsSetPropertyCallback propertySet;
        jsFinalizeCallback finalize;
        jsCallAsFunctionCallback callAsFunction;
    } jsData;
    typedef jsValue(WKE_CALL_TYPE*jsGetPropertyCallback)(jsExecState es, jsValue object, const char* propertyName);
    typedef bool(WKE_CALL_TYPE*jsSetPropertyCallback)(jsExecState es, jsValue object, const char* propertyName, jsValue value);
    typedef void(WKE_CALL_TYPE*jsFinalizeCallback)(struct tagjsData* data);
    typedef jsValue(WKE_CALL_TYPE*jsCallAsFunctionCallback)(jsExecState es, jsValue object, jsValue* args, int argCount);
    jsValue -> c_longlong
    jsExecState -> c_void_p
    '''
    _fields_=[('typeName',c_char*100),
              ('propertyGet',CFUNCTYPE(c_longlong,c_void_p,c_longlong,c_char_p)),
              ('propertySet',CFUNCTYPE(c_bool,c_void_p,c_longlong,c_char_p,c_longlong)),
              ('jsFinalizeCallback',CFUNCTYPE(None,c_void_p)),
              ('jsCallAsFunctionCallback',CFUNCTYPE(c_longlong,c_void_p))
              ]

class wkeJsKeys(Structure):
    '''
    typedef struct _jsKeys {
    unsigned int length;
    const char** keys;
    }jsKeys
    '''
    _fields_=[('length',c_uint),('keys',POINTER(c_char_p))]    

class wkeJsExceptionInfo(Structure):
    '''
    typedef struct _jsExceptionInfo {
        const utf8* message; // Returns the exception message.
        const utf8* sourceLine; // Returns the line of source code that the exception occurred within.
        const utf8* scriptResourceName; // Returns the resource name for the script from where the function causing the error originates.
        int lineNumber; // Returns the 1-based number of the line where the error occurred or 0 if the line number is unknown.
        int startPosition; // Returns the index within the script of the first character where the error occurred.
        int endPosition; // Returns the index within the script of the last character where the error occurred.
        int startColumn; // Returns the index within the line of the first character where the error occurred.
        int endColumn; // Returns the index within the line of the last character where the error occurred.
        const utf8* callstackString;
    } jsExceptionInfo;
    '''
    _fields_=[('message',c_char_p),
              ('keyssourceLine',c_char_p),
              ('scriptResourceName',c_char_p),      
              ('lineNumber',c_int),
              ('startPosition',c_int),
              ('endPosition',c_int),
              ('startColumn',c_int),
              ('endColumn',c_int),        
              ('callstackString',c_char_p) 
              ]    

class wkeUrlRequestCallbacks(Structure):
    '''
    typedef void(WKE_CALL_TYPE* wkeOnUrlRequestWillRedirectCallback)(wkeWebView webView, void* param, wkeWebUrlRequestPtr oldRequest, wkeWebUrlRequestPtr request, wkeWebUrlResponsePtr redirectResponse);
    typedef void(WKE_CALL_TYPE* wkeOnUrlRequestDidReceiveResponseCallback)(wkeWebView webView, void* param, wkeWebUrlRequestPtr request, wkeWebUrlResponsePtr response);
    typedef void(WKE_CALL_TYPE* wkeOnUrlRequestDidReceiveDataCallback)(wkeWebView webView, void* param, wkeWebUrlRequestPtr request, const char* data, int dataLength);
    typedef void(WKE_CALL_TYPE* wkeOnUrlRequestDidFailCallback)(wkeWebView webView, void* param, wkeWebUrlRequestPtr request, const utf8* error);
    typedef void(WKE_CALL_TYPE* wkeOnUrlRequestDidFinishLoadingCallback)(wkeWebView webView, void* param, wkeWebUrlRequestPtr request, double finishTime);

    typedef struct _wkeUrlRequestCallbacks {
        wkeOnUrlRequestWillRedirectCallback willRedirectCallback;
        wkeOnUrlRequestDidReceiveResponseCallback didReceiveResponseCallback;
        wkeOnUrlRequestDidReceiveDataCallback didReceiveDataCallback;
        wkeOnUrlRequestDidFailCallback didFailCallback;
        wkeOnUrlRequestDidFinishLoadingCallback didFinishLoadingCallback;
    } wkeUrlRequestCallbacks;

    '''
    _fields_=[('willRedirectCallback',CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p,c_void_p)),
              ('didReceiveResponseCallback',CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_void_p)),
              ('didReceiveDataCallback',CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_char_p,c_int)),
              ('didFailCallback',CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_char_p)),
              ('didFinishLoadingCallback',CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_double))
              ]

class Rect(Structure):

    _fields_=[('Left',c_int),('Top',c_int),('Right',c_int),('Bottom',c_int)]

class mPos(Structure):

    _fields_=[('x',c_int),('y',c_int)]



class mSize(Structure):
    ...
mSize._fields_=[('cx',c_int),('cy',c_int)]

class bitMap(Structure):

    _fields_=[('bmType',c_int),('bmWidth',c_int),('bmHeight',c_int),('bmWidthBytes',c_int),('bmPlanes',c_int),('bmBitsPixel',c_int),('bmBits',c_int)]

class blendFunction(Structure):

    _fields_=[('BlendOp',BYTE),('BlendFlags',BYTE),('SourceConstantAlpha',BYTE),('AlphaFormat',BYTE)]


class COMPOSITIONFORM(Structure):

    _fields_=[('dwStyle',c_int),('ptCurrentPos',mPos),('rcArea',Rect)]


class BITMAPINFOHEADER(Structure):
    """ 关于DIB的尺寸和颜色格式的信息 """
    _fields_ = [
        ("biSize", DWORD),
        ("biWidth", LONG),
        ("biHeight", LONG),
        ("biPlanes", WORD),#永远为1
        ("biBitCount", WORD),#1(双色)，4(16色)，8(256色)，24(真彩色)，32(真彩色)
        ("biCompression", DWORD),#0不压缩
        ("biSizeImage", DWORD),#表示位图数据的大小以字节为单位
        ("biXPelsPerMeter", LONG),
        ("biYPelsPerMeter", LONG),
        ("biClrUsed", DWORD),#位图实际使用的颜色表中的颜色数
        ("biClrImportant", DWORD)#位图显示过程中重要的颜色数
    ]
class BITMAPFILEHEADER(Structure):
    __file__=[
        ('bfType',c_int),#BMP类型：19778，也就是BM
        ('bfSize',c_int),#文件字节数：14 + BITMAPINFOHEADER.biSize + BITMAPINFOHEADER.biSizeImage
        ('bfReserved1',c_int),
        ('bfReserved2',c_int),
        ('bfOffBits',c_int)#位图的数据信息离文件头的偏移量:14 + BITMAPINFOHEADER.biSize
    ]
class BITMAPINFO(Structure):

    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", DWORD * 3)]

class COPYDATASTRUCT(Structure):
    _fields_ = [('dwData', LPARAM),('cbData', DWORD),('lpData', c_char_p)]

    

class PAINTSTRUCT(Structure):
    _fields_=[('hdc',_LRESULT),('fErase',c_int),('rcPaint',Rect),('fRestore',c_int),('fIncUpdate',c_int),('rgbReserved',c_char *32)]

class wkeWillSendRequestInfo(Structure):
    '''
    typedef struct _wkeWillSendRequestInfo {
        wkeString url;
        wkeString newUrl;
        wkeResourceType resourceType;
        int httpResponseCode;
        wkeString method;
        wkeString referrer;
        void* headers;
    } wkeWillSendRequestInfo;
    '''
    _fields_=[('url',c_char_p),('newUrl',c_char_p),('resourceType',c_int),('httpResponseCode',c_int),('method',c_char_p),('referrer',c_char_p),('headers',c_void_p)]

class wkeTempCallbackInfo(Structure):
    '''
    typedef struct _wkeTempCallbackInfo {
        int size;
        wkeWebFrameHandle frame;
        wkeWillSendRequestInfo* willSendRequestInfo;
        const char* url;
        wkePostBodyElements* postBody;
        wkeNetJob job;
    } wkeTempCallbackInfo;    
    '''
    _fields_=[('size',_LRESULT),('frame',c_void_p),('willSendRequestInfo',POINTER(wkeWillSendRequestInfo)),('url',c_char_p),('postBody',POINTER(wkePostBodyElements)),('job',c_void_p)]

class wkeNetJobDataBind(Structure):
    '''
    typedef void(WKE_CALL_TYPE*wkeNetJobDataRecvCallback)(void* ptr, wkeNetJob job, const char* data, int length);
    typedef void(WKE_CALL_TYPE*wkeNetJobDataFinishCallback)(void* ptr, wkeNetJob job, wkeLoadingResult result);

    typedef struct _wkeNetJobDataBind {
        void* param;
        wkeNetJobDataRecvCallback recvCallback;
        wkeNetJobDataFinishCallback finishCallback;
    } wkeNetJobDataBind;
    '''
    _fields_=[('param',c_void_p),('recvCallback',CFUNCTYPE(None,c_void_p,c_void_p,c_char_p,c_int)),('finishCallback',CFUNCTYPE(None,c_void_p,c_void_p,c_int))]

class wkeDraggableRegion(Structure):
    '''
        typedef struct {
        RECT bounds;
        bool draggable;
    } wkeDraggableRegion;
    '''
    _fields_=[('bounds',wkeRect),('draggable',c_bool)]
   
class wkeMediaLoadInfo(Structure):
    '''
    typedef struct _wkeMediaLoadInfo {
        int size;
        int width;
        int height;
        double duration;
    } wkeMediaLoadInfo;
    '''
    _fields_=[('size',c_int),('width',c_int),('height',c_int),('duration',c_double)]

def WkeMethod(prototype):
    class MethodDescriptor(object):
        __slots__ = ['func', 'boundFuncs']
        def __init__(self, func):
            self.func = func
            self.boundFuncs = {} 
        def __get__(self, obj, type=None):
            if obj!=None:
                try:
                    return self.boundFuncs[obj,type]
                except:
                    ret = self.boundFuncs[obj,type] = prototype(
                        self.func.__get__(obj, type))
                    return ret
    return MethodDescriptor
