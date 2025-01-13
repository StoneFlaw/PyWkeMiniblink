# -*- coding:utf-8 -*-




import os
import json


from ctypes import (cast,c_char_p,py_object,sizeof,byref,string_at,create_string_buffer,POINTER)
from ctypes import (
    c_void_p,
    windll,
    byref,
    CFUNCTYPE,
    WINFUNCTYPE
)
from ctypes.wintypes import (RGB,
    DWORD,
    HWND,
    UINT
)


import win32gui
import win32api
from win32con import *


from . import _LRESULT,WkeCallbackError
from .wke import Wke,Webview
from .wkeStruct import *

RelPath = lambda file : os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
PCOPYDATASTRUCT = POINTER(COPYDATASTRUCT)

SetWindowLong = windll.user32.SetWindowLongA
GetWindowLong = windll.user32.GetWindowLongA





def setIcon(hwnd,filename):
    """为一个真实窗口绑定一个wkeWebViewWindow

    Args:
        hwnd (int):         窗口句柄
        filename (str):     图标文件位置
    Returns:
        bool: Ture图标文件正常,设置成功,否则False
       
    """
    if not filename.endswith('.ico'):
        return False

    icon = win32gui.LoadImage(
        None, RelPath(filename), WkeConst.IMAGE_ICON,
        48, 48, WkeConst.LR_LOADFROMFILE)
    win32api.SendMessage(hwnd, WkeConst.WM_SETICON,WkeConst.ICON_BIG, icon)
    return True

def createWindow(title="",x=0,y=0,w=640,h=480,className='Miniblink'):
    """创建窗口

    Args:   
        title(str):  挂靠的python对象 
        x(int): 窗口左上点x坐标
        y(int): 窗口左上点y坐标
        w(int): 窗口宽度
        h(int): 窗口高度
        className(str):窗体句柄
    """
    wc = win32gui.WNDCLASS()
    wc.hbrBackground = COLOR_BTNFACE + 1
    wc.hCursor = win32gui.LoadCursor(0,IDI_APPLICATION)
    wc.lpszClassName = className
    wc.style =  CS_GLOBALCLASS|CS_VREDRAW | CS_HREDRAW
    reg = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindowEx(0, reg,title,WS_OVERLAPPEDWINDOW,x,y,w,h, 0, 0, 0, None)
    return hwnd

def createTransparentWindow(title="",x=0,y=0,w=640,h=480,className='Miniblink'):
    """创建透明窗口

    Args:   
        title(str):  挂靠的python对象 
        x(int): 窗口左上点x坐标
        y(int): 窗口左上点y坐标
        w(int): 窗口宽度
        h(int): 窗口高度
        className(str):窗体句柄
    """
    wc = win32gui.WNDCLASS()
    wc.hbrBackground = COLOR_BTNFACE + 1
    wc.hCursor = win32gui.LoadCursor(0,IDI_APPLICATION)
    wc.lpszClassName = className
    wc.style =  CS_GLOBALCLASS|CS_VREDRAW | CS_HREDRAW

    reg = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindowEx(0,reg,title,WS_CLIPCHILDREN|WS_CLIPSIBLINGS|WS_POPUP|WS_MINIMIZEBOX,x,y,w,h,0,0,0,None)
    return hwnd


def setWindowLongHook(hwnd,ex,index = WkeConst.GWL_USERDATA):
    """在窗口的私有数据上挂靠一个python对象 

    Args:   
        hwnd(int):窗体句柄
        ex(obj):  挂靠的python对象 
        index(int,optional): 挂载位置，默认WkeConst.GWL_USERDATA
    """
    #创建 Python 对象的 C 指针,PyObject *
    cPtrOfPyobj = py_object(ex)
    SetWindowLong(hwnd,index,cPtrOfPyobj)
    return

def getWindowLongHook(hwnd,index = WkeConst.GWL_USERDATA):
    """在窗口的私有数据上获取一个python对象

    Args:   
        hwnd(int):窗体句柄
        
        index(int,optional): 挂载位置，默认WkeConst.GWL_USERDATA
    Returns:
        object:     挂靠的python对象 
    """
    ex = GetWindowLong(hwnd,index)
    #PyObject * -> Ctypes Object
    cPtrOfPyobj = cast(ex,py_object)
    if ex == 0:
        return None
    obj = cPtrOfPyobj.value
    return obj


def replaceHWndProc(hwnd,newHwndProc):
    """替换窗口消息处理过程

    Args:   
        hwnd(int):窗体句柄
        newHwndProc(callable):  新的窗口处理过程
    Returns:
        int: 旧窗体处理过程  
    """
    oldHwndProc = win32gui.GetWindowLong(hwnd, WkeConst.GWL_WNDPROC)
    if newHwndProc:
       win32gui.SetWindowLong(hwnd, WkeConst.GWL_WNDPROC, newHwndProc)
    return oldHwndProc


    


def wkeTransparentPaint(webview,hwnd,hdc, x, y, cx, cy):
    rectDest=Rect()
    windll.user32.GetClientRect(hwnd,byref(rectDest))
    windll.user32.OffsetRect(byref(rectDest),-rectDest.Left,-rectDest.Top)

    width = rectDest.Right - rectDest.Left
    height = rectDest.Bottom - rectDest.Top
    hBitmap = windll.gdi32.GetCurrentObject(hdc, WkeConst.OBJ_BITMAP)

    bmp=bitMap()
    bmp.bmType=0
    cbBuffer=windll.gdi32.GetObjectA(hBitmap, 24,0)
    windll.gdi32.GetObjectA(hBitmap, cbBuffer,byref(bmp))
    sizeDest=mSize()
    sizeDest.cx =bmp.bmWidth
    sizeDest.cy =bmp.bmHeight

    hdcScreen = webview.getViewDC()# windll.user32.GetDC(_LRESULT(hwnd))
    blendFunc32bpp=blendFunction()
    blendFunc32bpp.BlendOp = 0   
    blendFunc32bpp.BlendFlags = 0
    blendFunc32bpp.SourceConstantAlpha = 255
    blendFunc32bpp.AlphaFormat = 1  
    pointSource=mPos()
    callOk = windll.user32.UpdateLayeredWindow(hwnd, hdcScreen, 0, byref(sizeDest), hdc, byref(pointSource), RGB(255,255,255), byref(blendFunc32bpp), WkeConst.ULW_ALPHA)

    windll.user32.ReleaseDC(hwnd, hdcScreen)
    return
    

def wkeEventOnPaint(webview,param,hdc,x,y,cx,cy):
    #hdc=kwargs['hdc']
    #x=kwargs['x']
    #y=kwargs['y']
    #cx=kwargs['cx']
    #cy=kwargs['cy']

    if param==None:
        return
    hwnd=param
    if (windll.user32.GetWindowLongW(hwnd,WkeConst.GWL_EXSTYLE) & WkeConst.WS_EX_LAYERED)== WkeConst.WS_EX_LAYERED:
        wkeTransparentPaint(webview,hwnd, hdc, x, y, cx, cy)
    else:
        rc=Rect(0,0,x+cx,y+cy)
        windll.user32.InvalidateRect(hwnd, byref(rc), True)
    return


class Timer:
    def __init__(self):
        self.timer_func_dict={}

    def setTimer(self,hwnd,nid,dwTime,is_timer_one=True):
        self.is_timer_one=is_timer_one
        return windll.user32.SetTimer (hwnd,nid, dwTime, self._timerCallBack)
    
    @WkeMethod(WINFUNCTYPE(c_void_p,HWND,c_void_p,UINT,DWORD))
    def _timerCallBack(self,hwnd,msg,nid,dwTime):
        if hasattr(self,'timerCallBack'):
            if self.is_timer_one:
                self.timerCallBack(hwnd=hwnd,msg=msg,nid=nid,dwTime=dwTime)
                windll.user32.KillTimer(hwnd,nid)
                return 0
            return self.timerCallBack(hwnd=hwnd,msg=msg,nid=nid,dwTime=dwTime)
        



class HwndProcAdapter():
    def __init__(self,hwnd=0,webview=None):
        self.webview=webview
        self.hwnd=hwnd
        self.msgProcEntries = {}  
        self.oldHwndProc = None
        self.oldGWL_USERDATA = 0
        self.attached = False
        return
    
    def registerMsgProc(self,msg,func):
        if isinstance(msg,list):
            for m in msg:
                self.msgProcEntries[m]=func
        else:
            self.msgProcEntries[msg]=func
        return

  

    def attach(self,hwnd=0,webview=None):
        if hwnd is not None:
            self.hwnd = hwnd
        if webview is not None:
            self.webview = webview

        self.oldGWL_USERDATA = getWindowLongHook(hwnd)
        setWindowLongHook(hwnd,self.webview)

        self.attached = True
        self.oldHwndProc = replaceHWndProc(hwnd,self._onWndProcCallback)

        
        return
    
    def detach(self):
        if self.attached == True:
            cb = CFUNCTYPE(_LRESULT, _LRESULT,_LRESULT,_LRESULT)
            self.oldHwndProc = replaceHWndProc(self.hwnd,cast(self.oldHwndProc,cb))
            setWindowLongHook(self.hwnd,self.oldGWL_USERDATA)
            self.attached = False
        return     
        
    def _onWndProcCallback(self, hwnd, msg, wParam, lParam):
        if msg in self.msgProcEntries:
            argcount=self.msgProcEntries[msg].__code__.co_argcount
            ret=None

            if argcount==5:
                arg_vals=self.msgProcEntries[msg].__code__.co_varnames
                if arg_vals[0] in ['self','webview']:
                    ret=self.msgProcEntries[msg](self.webview,hwnd,msg,wParam, lParam)
                else:
                    raise WkeCallbackError(f"Not support arg {arg_vals[0]}")

            elif argcount==4:
                ret=self.msgProcEntries[msg](hwnd,msg,wParam, lParam)

            elif argcount==3:
                ret=self.msgProcEntries[msg](hwnd,wParam, lParam)

            elif argcount==2:
                ret=self.msgProcEntries[msg](wParam, lParam)

            elif argcount==1:
                ret=self.msgProcEntries[msg](hwnd)
            else:
                raise WkeCallbackError(f"Not support {argcount} args")

            if ret!=None:
                return ret
           
        if msg == WkeConst.WM_DESTROY: 
            self.detach()
            
        return win32gui.CallWindowProc(self.oldHwndProc, hwnd, msg, wParam, lParam)