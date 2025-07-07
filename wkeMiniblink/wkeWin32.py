# -*- coding:utf-8 -*-

import os,sys,platform,time
import json
from threading import  Lock,Event,Thread
from struct import pack

import ctypes


from ctypes import (cast,c_char_p,py_object,sizeof,byref,string_at,create_string_buffer,POINTER)
from ctypes import (c_uint32,c_int32,c_ulong)
from ctypes import (
    c_void_p,
    c_float,
    windll,
    byref,
    CFUNCTYPE
)


from ctypes.wintypes import (RGB,MSG,
    DWORD,
    HWND,
    UINT,
    LPLONG
)


import win32gui
import win32api
from win32con import *
import win32ui
import win32con
import zlib

from . import _LRESULT,WkeCallbackError
from .wke import Wke,WebView
from .wkeStruct import *

RelPath = lambda file : os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
PCOPYDATASTRUCT = POINTER(COPYDATASTRUCT)


user32 = ctypes.WinDLL('user32', use_last_error=True)





bit=architecture()[0]

if bit == '64bit':
    SetWindowLong = user32.SetWindowLongPtrA
    GetWindowLong = user32.GetWindowLongPtrA
    #user32.SetWindowLongA.argtypes=[HWND,c_int,py_object]
    #user32.GetWindowLongA.argtypes=[HWND,c_int]
else:
    SetWindowLong = user32.SetWindowLongA
    GetWindowLong = user32.GetWindowLongA
    #user32.SetWindowLongA.argtypes=[HWND,c_int,py_object]
    #user32.GetWindowLongA.argtypes=[HWND,c_int]

SetWindowLong.argtypes = [HWND, c_int,py_object]
GetWindowLong.argtypes = [HWND, c_int]
SetWindowLong.restype = _LRESULT
GetWindowLong.restype = _LRESULT


def wkeSetWindowLongHook(hwnd,ex,index = WkeConst.GWL_USERDATA):
    """在窗口的私有数据上挂靠一个python对象 

    Args:   
        hwnd(int):窗体句柄
        ex(obj):  挂靠的python对象 
        index(int,optional): 挂载位置，默认WkeConst.GWL_USERDATA
    Return:
    """
    #创建 Python 对象的 C 指针,PyObject *
    cPtrOfPyobj = py_object(ex)

    result = SetWindowLong(hwnd, index,cPtrOfPyobj)
    return result

def wkeGetWindowLongHook(hwnd,index = WkeConst.GWL_USERDATA):
    """在窗口的私有数据上获取一个python对象

    Args:   
        hwnd(int):窗体句柄
        
        index(int,optional): 挂载位置，默认WkeConst.GWL_USERDATA
    Returns:
        object:     挂靠的python对象 
    """
    ex = GetWindowLong(hwnd,index)
    if ex == 0:
        return None
    #PyObject * -> Ctypes Object
    cPtrOfPyobj = cast(ex,py_object)
    obj = cPtrOfPyobj.value
    return obj

def wkeGetWindowLong(hwnd,index = WkeConst.GWL_USERDATA):
    """在窗口的私有数据上获取数值


    """
    ex = GetWindowLong(hwnd,index)
    return ex

def wkeSetWindowLong(hwnd,index,ex):
    """在窗口的私有数据上获取数值


    """
    result = SetWindowLong(hwnd, index,ex)
    return result

def wkeSetIcon(hwnd,filename):
    """为一个真实窗口绑定一个wkeWebWindow

    Args:
        hwnd (int):         窗口句柄
        filename (str):     图标文件位置
    Returns:
        bool: Ture图标文件正常,设置成功,否则False
       
    """
    if  not os.path.exists(filename):
        return False
    if not filename.endswith('.ico'):
        return False

    icon = win32gui.LoadImage(
        None, RelPath(filename), WkeConst.IMAGE_ICON,
        48, 48, WkeConst.LR_LOADFROMFILE)
    win32api.SendMessage(hwnd, WkeConst.WM_SETICON,WkeConst.ICON_BIG, icon)
    return True

def wkeMessageBox(msg,title="",parent=None):
    ret = win32gui.MessageBox(parent, msg, title, win32con.MB_OK)
    return ret

def wkeCreateWindow(title="",x=0,y=0,w=640,h=480,className='Miniblink'):
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

def wkeCreateTransparentWindow(title="",x=0,y=0,w=640,h=480,className='Miniblink'):
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




def wkeReplaceHWndProc(hwnd,newHwndProc):
    """替换窗口消息处理过程

    Args:   
        hwnd(int):窗体句柄
        newHwndProc(function):  新的窗口处理过程
    Returns:
        int: 旧窗体处理过程  
    """

    oldHwndProc = win32api.GetWindowLong(hwnd, WkeConst.GWL_WNDPROC)
    #win32gui.GetWindowLong的x64 返回值只有低32位0
    if newHwndProc:
        #user32.SetWindowLongW.argtypes=[HWND,c_int,py_object]
        #user32.SetWindowLongW(hwnd,WkeConst.GWL_WNDPROC, newHwndProc)
        
        #only win32gui.SetWindowLong works
        win32gui.SetWindowLong(hwnd, WkeConst.GWL_WNDPROC, newHwndProc)
    return oldHwndProc



    


def wkeTransparentPaint(webview,hwnd,hdc, x, y, cx, cy):
    """webview透明绘制 


    """
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
    

def wkeEventOnPaint(context,hdc,x,y,cx,cy):
    """webview绘制事件的绑定


    """

    #hdc=kwargs['hdc']
    #x=kwargs['x']
    #y=kwargs['y']
    #cx=kwargs['cx']
    #cy=kwargs['cy']
    hwnd=context["param"]
    webview = context["webview"]
    if (windll.user32.GetWindowLongW(hwnd,WkeConst.GWL_EXSTYLE) & WkeConst.WS_EX_LAYERED)== WkeConst.WS_EX_LAYERED:
        wkeTransparentPaint(webview,hwnd, hdc, x, y, cx, cy)
    else:
        rc=Rect(0,0,x+cx,y+cy)
        windll.user32.InvalidateRect(hwnd, byref(rc), True)
    return

def wkePumpMessages(block=False):
    """循环提取分发当前线程的所有窗口消息
    
    Args:
        block(bool) : True使用GetMessageA阻塞式/False使用PeekMessageA非阻塞式并配合休眠
    """
    msg = MSG()
    if block == True:
        while True:
            res = windll.user32.GetMessageA(byref(msg), None, 0, 0)
            if  res != 0:
                windll.user32.TranslateMessage(byref(msg))
                windll.user32.DispatchMessageA(byref(msg))
            elif res == 0:
                windll.user32.TranslateMessage(byref(msg))
                windll.user32.DispatchMessageA(byref(msg))
                break
            else:
                raise RuntimeError(f"GetMessage {res}")
    else:
        while True:
            res = windll.user32.PeekMessageA(byref(msg), None,0, 0, 1)
            if  res != 0:
                windll.user32.TranslateMessage(byref(msg))
                windll.user32.DispatchMessageA(byref(msg))
                if msg.message in[WM_QUIT]: 
                    break
            else:
                time.sleep(0.05)
    return

class WkeTimer:
    """定时器
        Win32定时器的接口对象,可以指定定时器的对应窗口/ID/周期/响应函数

        Example:
            
            .. code:: python

                #定时器消息回调函数
                def timeCallback(*args,**kwargs):
                global count
                count = count+1
                if count>=9:
                    owner = kwargs["owner"]
                    owner.stop()
                    win32gui.PostQuitMessage(0)
                return

                t = WkeTimer()    
                t.init(timeCallback,None,0,3000)
                t.start()
                Wke.runMessageLoop()       

    """
    def __init__(self,func=None,hwnd=0,nIDEvent=0,msElapse=0):
        """
            对应的C API
            UINT_PTR SetTimer(
                HWND hWnd,          # 窗口句柄
                UINT_PTR nIDEvent,  # 定时器ID
                UINT msElapse,       # 时间间隔，单位为毫秒
                TIMERPROC lpTimerFunc  # 回调函数指针
            );

            如果函数成功，且hWnd参数为0，则返回新建立的时钟编号，可以将这个时钟编号传递给KillTimer来销毁时钟。
            如果函数成功，且hWnd参数为非0，则返回一个非零的整数，可以将这个非零的整数传递给KillTimer来销毁时钟。
            如果函数失败，返回值为零。若想获得更多的错误信息，可以调用GetLastError函数。

            lpTimerFunc是WM_TIMER的处理函数,可以NULL，这样变成定时的WM_TIMER消息。
            
        """
        self._kid = 0
      
        self.init(func,hwnd,nIDEvent,msElapse)
        return

    def __del__(self):
        if self._kid:
            self.stop()
        return
    
    def init(self,func=None,hwnd=0,nIDEvent=0,msElapse=0):
        """ 初始化定时器

        Args:
            func(function): 定时器响应函数指针
            hwnd(int):      定时器所在窗口句柄
            nIDEvent(int):  定时器ID
            msElapse(int):  时间间隔，单位为毫秒

        定时器响应函数格式:         def timerCallback(hwnd, msg, id, time) 返回值None

        """
        if self._kid != 0 :
            raise SyntaxError("Timer was not killed before init!")
        self.hwnd = hwnd
        self.nIDEvent = nIDEvent
        self.msElapse = msElapse
        self.func = func
        self._kid = 0
        self.context={"hwnd":hwnd,"id":self.nIDEvent,"period":self.msElapse}
        return

    @WkeMethod(CFUNCTYPE(c_void_p,HWND,c_void_p,UINT,DWORD))
    def timeCallback(self,hwnd, msg, id, time):
        return self.func(hwnd, msg, id, time,owner=self)
    
    @property
    def period(self):
        return self.msElapse
    
    def start(self):
        """ 启动定时器

        Returns:
            int:     返回非0启动成功，返回0启动失败
        """    
        if self.func == None or not callable(self.func):
            "只是定时触发WM_TIMER"
            func = None
        else:
            func = self.timeCallback
        
        #注意如果HWND为NULL的时候，第二个nIDEvent参数无效
        if self.hwnd == None:
            self.nIDEvent = 0
            #注意如果HWND为NULL的时候，第二个nIDEvent参数无效，即不能再timer的响应函数中通过ID判断不同的定时器
            ret =  windll.user32.SetTimer(self.hwnd,self.nIDEvent, self.msElapse,func)
            if ret!=0:
                self.started = True
                #关闭时要用返回的计时器编号
                self._kid = ret
                return True
        else:
            ret =  windll.user32.SetTimer(self.hwnd,self.nIDEvent, self.msElapse,func)
            if ret!=0:                    
                self._kid = ret
                return True
    
        return False
    
    def stop(self):
        """ 停止定时器
        """
        if self._kid != 0 :
            windll.user32.KillTimer(self.hwnd,self._kid )
            self._kid = 0
            return True
        return False



class WkeSnapShot():
    """网页视图截图

        Win32定时器的接口对象,可以指定定时器的对应窗口/ID/周期/响应函数

        Example:
            
            .. code:: python

                webview = WebWindow()
                webview.create(0,0,0,800,600)
                snap = WkeSnapShot()
                snap.bind(webview.getWindowHandle())
                setattr(webview,"snap",snap)

                snap.capture()
                snap.save("screenshot.bmp")

                Wke.runMessageLoop()       

    """
    def __init__(self):
        '''
        D3D 的窗口需要再前台才能,最小化不行
        DirectX12的窗口不行
        '''
        self.hwnd = None  #默认当前窗口
        self.WindowDC = None
        self.DC = None
        self.bmpDC = None
        self.bmp = None
  

        self.bmpinfo = None

        self.clientWidth = -1
        self.clientHeight = -1
        #客户区相对于窗口的偏移
        self.clientTop = 0    
        self.clientLeft = 0    

        return

    def __del__(self):
        self.release()
        return
    @property
    def size(self):
        return self.clientWidth,self.clientHeight 

    @property
    def bytesPixel(self):
        return self.bmBytesPixel

    @property
    def width(self):
        return self.clientWidth

    @property
    def height(self):
        return self.clientHeight 
    
    @property
    def bits(self):
        return self.bmp.GetBitmapBits(True)

    @property
    def bitsInfo(self):
        return self.bmp.GetInfo()  
      
    def bind(self,hwnd):
        """绑定指定的窗口

        如果窗口Resize了,需要重新绑定

        Args:
            hwnd(int): 要截图的窗口句柄
        Returns:
            int: 返回原窗口句柄绑定成功。返回-1绑定失败
        """  
        ret = -1
        self.WindowDC = win32gui.GetWindowDC(hwnd)
        if self.WindowDC != 0:
            ret = hwnd
            self.hwnd = hwnd
            self.DC = win32ui.CreateDCFromHandle(self.WindowDC)
            # mfcDC创建可兼容的DC
            self.bmpDC = self.DC.CreateCompatibleDC()

            #窗口全局
            winRect = Rect()
            windll.user32.GetWindowRect(self.hwnd,byref(winRect))
            #print("%d,%d,%d,%d"%(winRect.Left,winRect.Top,winRect.Right,winRect.Bottom))

            #窗口客户区
            clientRect = Rect()
            #此时为客户区内坐标
            windll.user32.GetClientRect(self.hwnd,byref(clientRect))
            #print("%d,%d,%d,%d"%(clientRect.Left,clientRect.Top,clientRect.Right,clientRect.Bottom))

            self.clientWidth=clientRect.Right - clientRect.Left 
            self.clientHeight=clientRect.Bottom- clientRect.Top 

            #转换到全局屏幕坐标
            p = mPos()
            p.x = 0
            p.y = 0
            windll.user32.ClientToScreen(self.hwnd,byref(p))
            #print("%d,%d"%(p.x,p.y))

            self.clientLeft = p.x - winRect.Left
            self.clientTop = p.y  - winRect.Top  


            # 创建bigmap准备保存图片
            self.bmp = win32ui.CreateBitmap()
            self.bmp.CreateCompatibleBitmap(self.DC, self.clientWidth, self.clientHeight)
            self.bmpinfo = self.bmp.GetInfo()

            self.clientWidth = self.bmpinfo['bmWidth']
            self.clientHeight =  self.bmpinfo['bmHeight']
            self.bmBytesPixel = self.bmpinfo['bmBitsPixel']//8

        return    ret




    def release(self):
        """释放截图对象的资源
        """    
        if self.bmpDC:
            self.bmpDC.DeleteDC()
            self.bmpDC = None
        if self.DC:    
            self.DC.DeleteDC()
            self.DC = None
        if self.WindowDC:
            win32gui.ReleaseDC(self.hwnd,self.WindowDC)
            self.WindowDC = None

        if self.bmp:
            win32gui.DeleteObject(self.bmp.GetHandle())
            self.bmp = None
       
        self.bmpinfo = None
        self.clientWidth = -1
        self.clientHeight = -1
        self.clientTop = 0    
        self.clientLeft = 0    

        return

    def capture(self):
        """截图

        Return:
            bytes: 当前截图的二进制流
        """
        if self.hwnd == None:
            return None

        self.bmpDC.SelectObject(self.bmp)
 
        '''
        PW_CLIENTONLY=1
        PW_RENDERFULLCONTENT=2
        WM_PRINT     =                   0x0317
        WM_PRINTCLIENT    =              0x0318

        ret = windll.user32.PrintWindow(hwnd, self.DC.GetSafeHdc(),WM_PRINTCLIENT )
        print(ret)
        '''
        self.bmpDC.BitBlt((0 ,0), (self.clientWidth, self.clientHeight), self.DC, ( self.clientLeft,self.clientTop ), win32con.SRCCOPY)

        #bmpinfo = self.bmp.GetInfo()
        #bmpBits = self.bmp.GetBitmapBits(True)

        return 
 
    def saveAsBmp(self,name):
        """截图数据存入bmp文件

        使用capture截图后的二进制数据存入name指定的文件,bmp格式

        Args:
            name(str): 使用capture截图后的二进制数据

        """  
        if self.hwnd == None:
            return None
        self.bmp.SaveBitmapFile(self.bmpDC,name)    
        return


    def saveAsPng(self,name):
        """截图数据存入png文件

        使用capture截图后的二进制数据存入name指定的文件,png格式

        Args:
            name(str): 使用capture截图后的二进制数据

        """  
        def bgra2rgb(raw,width, height):        
            """BMP格式中的BGRA翻转成RGB""" 
            rgb = bytearray(height * width * 3)
            rgb[0::3] = raw[2::4]   #r
            rgb[1::3] = raw[1::4]   #g
            rgb[2::3] = raw[0::4]   #b
            return bytes(rgb)
        
        def toPng(data, width, height, level=6, filename=None):
            """RGB压缩到文件""" 
            line = width * 3
            png_filter = pack(">B", 0)
            scanlines = b"".join(
                [png_filter + data[y * line : y * line + line] for y in range(height)]
            )

            magic = pack(">8B", 137, 80, 78, 71, 13, 10, 26, 10)
        
            ihdr = [b"", b"IHDR", b"", b""]
            ihdr[2] = pack(">2I5B", width, height, 8, 2, 0, 0, 0)
            ihdr[3] = pack(">I", zlib.crc32(b"".join(ihdr[1:3])) & 0xFFFFFFFF)
            ihdr[0] = pack(">I", len(ihdr[2]))

        
            idat = [b"", b"IDAT", zlib.compress(scanlines, level), b""]
            idat[3] = pack(">I", zlib.crc32(b"".join(idat[1:3])) & 0xFFFFFFFF)
            idat[0] = pack(">I", len(idat[2]))

            
            iend = [b"", b"IEND", b"", b""]
            iend[3] = pack(">I", zlib.crc32(iend[1]) & 0xFFFFFFFF)
            iend[0] = pack(">I", len(iend[2]))

            if not filename:
                #没指定文件名就返回二进制数据
                return magic + b"".join(ihdr + idat + iend)
            with open(filename, "wb") as f:
                f.write(magic+ b"".join(ihdr + idat + iend))
            return
        
        if self.hwnd == None:
            return None
        
        bits = self.bmp.GetBitmapBits(True)
        rgb = bgra2rgb(bits,self.clientWidth ,self.clientHeight )     
        toPng(rgb,self.clientWidth ,self.clientHeight,7,name )   
        return None


class HwndMsgAdapter():
    """窗口消息适配器

        HwndProcAdapter使用自身的消息处理流程替换指定父窗口的消息处理，接受外部注册的python函数处理指定的消息。
        
        替换后对于已经注册的消息,使用注册函数来响应,如果函数返回None,则继续调用父窗口的默认消息处理流程,若不为None则不调用;对于没注册的消息则使用父窗口的默认消息处理流程。

        注册的消息响应函数可以有1~5个参数,如下:

        ============      ======      ======      ======      ======
            Arg1           Arg2        Arg3        Arg4        Arg5
        ------------      ------      ------      ------      ------
        webview           hwnd        msg         wParam      lParam
        self              hwnd        msg         wParam      lParam
        hwnd              msg         wParam      lParam
        hwnd              wParam      lParam
        wParam            lParam
        self  
        hwnd    
        ============      ======      ======      ======      ======
        
        *HwndProcAdapter的消息处理流程调用注册的消息响应函数时:*
        
            * hwnd/msg/wParam/lParam 使用父窗口的处理流程的句柄/消息/参数带入
            * 5个参数时,第一个参数名为self或webview,self则对应HwndProcAdapter类实例带入,webview对应HwndProcAdapter类实例的webview属性带入
            * 1个参数时,同上,参数名为其他时,以消息窗口句柄hwnd带入

        Examples:
            .. code:: python      

                x,y,w,h = 0,0,640,480
                hwnd = wkeCreateWindow('Window',x,y,w,h)
                webview.build(hwnd,x,y,w,h)   
                
                a = HwndMsgAdapter()
                def wkeMsgProcQuit(webview,hwnd,msg,wParam,lParam):
                    win32gui.PostQuitMessage(0)
                    return 
                a.registerMsgProc(WM_SIZE,wkeMsgProcResize)
                a.registerMsgProc(WM_DESTROY,wkeMsgProcQuit)
                a.attach(hwnd,webview)
                webview.loadURL("http://192.168.1.1")
                ....

        NOTE:
            替换窗口消息流程后,消息循环工作前.如果使用其他API(webview.moveToCenter)触发了UI相关消息可能导致显示不正确
    """
    def __init__(self,hwnd=0,webview=None):
        self.webview=webview
        self.hwnd=hwnd
        self.msgProcEntries = {}  
        self.oldHwndProc = None
        self.oldGWL_USERDATA = 0
        self.attached = False
        return
    
    def registerMsgProc(self,msg,func):
        """为指定的消息注册指定的处理函数

        Keyword Args:
            msg(int):         注册的消息
            func(function):    为该消息注册的响应函数
        """
        if isinstance(msg,list):
            for m in msg:
                self.msgProcEntries[m]=func
        else:
            self.msgProcEntries[msg]=func
        return

  
    def attach(self,hwnd=0,webview=None):
        """加载替换父窗口的消息响应流程

        Keyword Args:
            hwnd(int):  父窗口句柄
            webview(WebView):   父窗口对应的WebView/WebWindow网页对象

        """
        if hwnd is not None:
            self.hwnd = hwnd
        if webview is not None:
            self.webview = webview

        self.oldGWL_USERDATA = wkeGetWindowLongHook(hwnd)
        if self.oldGWL_USERDATA  != self.webview:
            wkeSetWindowLongHook(hwnd,self.webview)
            newUSERDATA = wkeGetWindowLongHook(hwnd)
            if newUSERDATA != self.webview:
                raise RuntimeError("SetWindowLongHook Fail")

        self.attached = True
        self.oldHwndProc = wkeReplaceHWndProc(hwnd,self._onWndProcCallback)

        
        return
    
    def detach(self):
        """卸载替换父窗口的消息响应流程

        """
        if self.attached == True:
            cb = CFUNCTYPE(_LRESULT, _LRESULT,_LRESULT,_LRESULT)
            self.oldHwndProc = wkeReplaceHWndProc(self.hwnd,cast(self.oldHwndProc,cb))
            wkeSetWindowLongHook(self.hwnd,self.oldGWL_USERDATA)
            self.attached = False
        return     
        
    def _onWndProcCallback(self, hwnd, msg, wParam, lParam):
        if msg in self.msgProcEntries:
            argcount=self.msgProcEntries[msg].__code__.co_argcount
            ret=None

            if argcount==5:
                arg_vals=self.msgProcEntries[msg].__code__.co_varnames
                if arg_vals[0] in ['self']:
                    ret=self.msgProcEntries[msg](self,hwnd,msg,wParam, lParam)
                elif arg_vals[0] in ['webview']:
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
                arg_vals=self.msgProcEntries[msg].__code__.co_varnames
                if arg_vals[0] in ['self']:
                    ret=self.msgProcEntries[msg](self)
                else:
                    ret=self.msgProcEntries[msg](hwnd)

            else:
                raise WkeCallbackError(f"Not support {argcount} args")

            if ret!=None:
                return ret
           
        if msg == WkeConst.WM_DESTROY: 
            self.detach()
            
        return win32gui.CallWindowProc(self.oldHwndProc, hwnd, msg, wParam, lParam)