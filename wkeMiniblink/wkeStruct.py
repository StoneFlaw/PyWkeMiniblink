# -*- coding:utf-8 -*-
import enum

from ctypes import (
    c_int,
    c_ushort,
    c_long,
    c_longlong,
    c_char,
    c_char_p,
    c_wchar_p,
    c_bool,
    c_void_p,
    c_size_t,
    Structure,
    POINTER
    )

from ctypes.wintypes import (
    LPARAM,
    DWORD,
    LONG,
    WORD,
    BYTE
)

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
    
class wkeProxy(Structure):

    _fields_ = [('type', c_int),('hostname', c_char *100),('port', c_ushort ),('username', c_char *50),('password',c_char *50)]
class wkeRect(Structure):

    _fields_=[('x',c_int),('y',c_int),('w',c_int),('h',c_int)]
class wkeMemBuf(Structure):

    _fields_=[('size',c_int),('data',c_char_p),('length',c_size_t)]
class wkeString(Structure):
    ...
class wkePostBodyElement(Structure):

    _fields_=[('size',c_int),('type',c_int),('data',POINTER(wkeMemBuf)),('filePath',wkeString),('fileStart',c_longlong),('fileLength',c_longlong)]
    ...
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

    
from . import _LRESULT
class PAINTSTRUCT(Structure):
    _fields_=[('hdc',_LRESULT),('fErase',c_int),('rcPaint',Rect),('fRestore',c_int),('fIncUpdate',c_int),('rgbReserved',c_char *32)]


class WKETempCallbackInfo(Structure):
    _fields_=[('size',_LRESULT),('frame',c_int),('willSendRequestInfo',c_void_p),('url',c_char_p),('postBody',c_void_p),('job',c_void_p)]


    
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
