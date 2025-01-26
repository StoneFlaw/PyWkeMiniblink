# -*- coding:utf-8 -*-




import os
import json


from ctypes import (cast,c_char_p,py_object,sizeof,byref,string_at,create_string_buffer,POINTER)
from ctypes import (
    c_void_p,
    windll,
    byref,
    CFUNCTYPE
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
from .wke import Wke,WebView
from .wkeStruct import *

from .wkeWin32 import *




##############################################################################################
def wkeMsgProcPaint_Resize(webview,hwnd,msg,wParam,lParam):
    """WM_PAINT 
    
    只调整大小,webview内部自己重绘
    
    """
    rect=Rect()
    windll.user32.GetClientRect(hwnd,byref(rect))
    webview.resize(rect.Right - rect.Left,rect.Bottom - rect.Top)
    return 

def wkeMsgProcResize(webview,hwnd,msg,wParam,lParam):
    """WM_SIZE

    """
    width= lParam & 65535
    height= lParam >> 16
    webview.resize(width,height)
    return 
 
def wkeMsgProcQuit(webview,hwnd,msg,wParam,lParam):
    """WM_DESTROY

    """
    win32gui.PostQuitMessage(0)
    return 

def wkeMsgProcKeyDown(webview,hwnd,msg,wParam,lParam):
    """WM_KEYDOWN

    """
    virtualKeyCode=wParam
    flags=0
    if ((lParam >> 16) & WkeConst.KF_REPEAT)!=0:
        flags=flags | 0x4000
    if ((lParam >> 16)  & WkeConst.KF_EXTENDED)!=0:
        flags=flags | 0x0100
    if webview.fireKeyDownEvent(virtualKeyCode,flags)!=0:
        return 0
    return

def wkeMsgProcKeyUp(webview,hwnd,msg,wParam,lParam):
    """WM_KEYUP

    """
    virtualKeyCode=wParam
    flags=0
    if virtualKeyCode==116:
        webview.reload()
    if ((lParam >> 16) & WkeConst.KF_REPEAT)!=0:
        flags=flags | 0x4000
    if ((lParam >> 16) & WkeConst.KF_EXTENDED)!=0:
        flags=flags | 0x0100
    if webview.fireKeyUpEvent(virtualKeyCode,flags)!=0:
        return 0
    return

def wkeMsgProcChar(webview,hwnd,msg,wParam,lParam):
    """WM_CHAR

    """
    virtualKeyCode=wParam
    flags=0
    if ((lParam >> 16) & WkeConst.KF_REPEAT)!=0:
        flags=flags | 0x4000
    if webview.fireKeyPressEvent(virtualKeyCode,flags)!=0:
        return 0
    return

def wkeMsgProcEraseBackground(webview,hwnd,msg,wParam,lParam):
    """WM_ERASEBKGND

    """
    return 1

def wkeMsgProcInputLangChange(webview,hwnd,msg,wParam,lParam):
    """WM_INPUTLANGCHANGE

    """
    return windll.user32.DefWindowProcA(hwnd, msg, _LRESULT(wParam), _LRESULT(lParam))

def wkeMsgProcMouseClick(webview,hwnd,msg,wParam,lParam):
    """鼠标点击事件
       
       包括:WM_LBUTTONDOWN,WM_MBUTTONDOWN,WM_RBUTTONDOWN,WM_LBUTTONDBLCLK,WM_MBUTTONDBLCLK,WM_RBUTTONDBLCLK,WM_LBUTTONUP,WkeConst.WM_MBUTTONUP,WkeConst.WM_RBUTTONUP

    """
    x=lParam & 65535
    y=lParam >> 16
    flags=0
    if msg in [WkeConst.WM_LBUTTONDOWN,WkeConst.WM_MBUTTONDOWN,WkeConst.WM_RBUTTONDOWN]:
        if windll.user32.GetFocus()!=hwnd:
            windll.user32.SetFocus(hwnd)
        windll.user32.SetCapture(hwnd)
    elif msg in [WkeConst.WM_LBUTTONUP,WkeConst.WM_MBUTTONUP,WkeConst.WM_RBUTTONUP]:
        windll.user32.ReleaseCapture()

    if (wParam & WkeConst.MK_CONTROL)!=0:
        flags=flags | 8
    elif (wParam & WkeConst.MK_SHIFT)!=0:
        flags=flags | 4
    elif (wParam & WkeConst.MK_LBUTTON)!=0:
        flags=flags | 1
    elif (wParam & WkeConst.MK_MBUTTON)!=0:
        flags=flags | 16
    elif (wParam & WkeConst.MK_RBUTTON)!=0:
        flags=flags | 2
    webview.fireMouseEvent( msg, x, y, flags)
    return 0


def wkeMsgProcMouseMove(webview,hwnd,msg,wParam,lParam):
    """WM_MOUSEMOVE

    """
    x=lParam & 65535
    y=lParam >> 16
    flags=0
    if (wParam & WkeConst.MK_LBUTTON)!=0:
        flags=flags | 1
    if webview.fireMouseEvent( msg, x, y, flags)!=0:
        return 0
    return

def wkeMsgProcMouseWheel(webview,hwnd,msg,wParam,lParam):
    """WM_MOUSEWHEEL

    """    
    pt=mPos()
    pt.x=lParam & 65535
    pt.y=lParam >> 16
    windll.user32.ScreenToClient(hwnd,byref(pt))
    delta= wParam >> 16
    flags=0

    if (wParam & WkeConst.MK_CONTROL)!=0:
        flags=flags | 8
    if (wParam & WkeConst.MK_SHIFT)!=0:
        flags=flags | 4
    if (wParam & WkeConst.MK_LBUTTON)!=0:
        flags=flags | 1
    if (wParam & WkeConst.MK_MBUTTON)!=0:
        flags=flags | 16
    if (wParam & WkeConst.MK_RBUTTON)!=0:
        flags=flags | 2
    if webview.fireMouseWheelEvent(pt.x,pt.y,delta,flags)!=0:
        return 0
    return

def wkeMsgProcMouseContextMenu(webview,hwnd,msg,wParam,lParam):
    """WM_CONTEXTMENU

    """
       
    pt=mPos()
    pt.x=lParam & 65535
    pt.y=lParam >> 16
    if pt.x!=-1 and pt.y!=-1:
        windll.user32.ScreenToClient(hwnd,byref(pt))
    flags=0
    if (wParam & WkeConst.MK_CONTROL)!=0:
        flags=flags | 8
    if (wParam & WkeConst.MK_SHIFT)!=0:
        flags=flags | 4
    if (wParam & WkeConst.MK_LBUTTON)!=0:
        flags=flags | 1
    if (wParam & WkeConst.MK_MBUTTON)!=0:
        flags=flags | 16
    if (wParam & WkeConst.MK_RBUTTON)!=0:
        flags=flags | 2

    if webview.fireContextMenuEvent(pt.x,pt.y, flags)!=0:
        return 0
    return

def wkeMsgProcNchiTest(webview,hwnd,msg,wParam,lParam):
    """WM_NCHITTEST

    处理鼠标消息，以便系统确定屏幕坐标属于窗口哪个部分,透明窗口下默认上下左右边框宽度5
    """
    #if webview.IsZoomed() != True:
    #    return
    
    if windll.user32.IsZoomed(hwnd)!=0:
        return 1
    pt=mPos()
    pt.x=lParam & 65535
    pt.y=lParam >> 16
    windll.user32.ScreenToClient(hwnd,byref(pt))
    rc=Rect()
    windll.user32.GetClientRect(hwnd,byref(rc))
    iWidth = rc.Right - rc.Left
    iHeight = rc.Bottom - rc.Top
    if windll.user32.PtInRect(byref(Rect(5, 0, iWidth - 5, 5)),pt):
        retn=12#HTTOP
    elif windll.user32.PtInRect(byref(Rect(0, 5, 5, iHeight - 5)),pt):
        retn=10#HTLEFT
    elif windll.user32.PtInRect(byref(Rect(iWidth - 5, 5, iWidth, iHeight - 10)),pt):
        retn=11#HTRIGHT 
    elif windll.user32.PtInRect(byref(Rect(5, iHeight - 5, iWidth - 10, iHeight)),pt):
        retn=15#HTBOTTOM
    elif windll.user32.PtInRect(byref(Rect(0, 0, 5, 5)),pt):
        retn=13#HTTOPLEFT
    elif windll.user32.PtInRect(byref(Rect(0, iHeight - 5, 5, iHeight)),pt):
        retn=16#HTBOTTOMLEFT
    elif windll.user32.PtInRect(byref(Rect(iWidth - 5, 0, iWidth, 5)),pt):
        retn=14#HTTOPRIGHT
    elif windll.user32.PtInRect(byref(Rect(iWidth - 10, iHeight - 10, iWidth, iHeight)),pt):
        retn=17#HTBOTTOMRIGHT
    else:
        retn=1
    return retn

def wkeMsgProcSetCursor(webview,hwnd,msg,wParam,lParam):
    """WM_SETCURSOR

    """
    if webview.fireWindowsMessage(WkeConst.WM_SETCURSOR,wParam,lParam)!=0:
        return 0
    return

def wkeMsgProcSetFocus(webview,hwnd,msg,wParam,lParam):
    """WM_SETFOCUS

    """
    windll.user32.SetFocus(hwnd)
    return 0

def wkeMsgProcKillFocus(webview,hwnd,msg,wParam,lParam):
    """WM_WM_KILLFOCUS

    """
    webview.killFocus()
    return 0

def wkeMsgProcStartComposition(webview,hwnd,msg,wParam,lParam):
    """WM_IME_STARTCOMPOSITION

    """    
    caret=webview.getCaretRect()
    mposForm=COMPOSITIONFORM()
    mposForm.dwStyle = 2 | 32
    mposForm.ptCurrentPos.x = caret.x
    mposForm.ptCurrentPos.y = caret.y
    hIMC=windll.imm32.ImmGetContext(hwnd)
    windll.imm32.ImmSetCompositionWindow(hIMC,byref(mposForm))
    windll.imm32.ImmReleaseContext(hwnd,hIMC)
    return 0

def wkeMsgProcPaint(webview,hwnd,msg,wParam,lParam):

    #窗口有WS_EX_LAYERED扩展样式=透明窗口
    if WkeConst.WS_EX_LAYERED!=(WkeConst.WS_EX_LAYERED & windll.user32.GetWindowLongW(hwnd,WkeConst.GWL_EXSTYLE)):
        ps=PAINTSTRUCT()
        hdc=windll.user32.BeginPaint(hwnd,byref(ps))
        rcClip = ps.rcPaint
        rcClient=Rect()
        windll.user32.GetClientRect(hwnd,byref(rcClient))

        rcInvalid=rcClient
        if (rcClient.Right != rcClip.Left) and (rcClip.Bottom != rcClip.Top):
            windll.user32.IntersectRect(byref(rcInvalid),byref(rcClip),byref(rcClient))
            srcX = rcInvalid.Left - rcClient.Left
            srcY = rcInvalid.Top - rcClient.Top
            destX = rcInvalid.Left
            destY = rcInvalid.Top
            width = rcInvalid.Right - rcInvalid.Left
            height = rcInvalid.Bottom - rcInvalid.Top
            if width!=0 and height!=0:
                
                tmp_dc=webview.getViewDC()
                windll.gdi32.BitBlt(hdc,destX, destY, width, height,tmp_dc,srcX, srcY,WkeConst.SRCCOPY)
                webview.unlockViewDC()
            windll.user32.EndPaint(hwnd,byref(ps))
            #向hWnd窗体发出WM_PAINT的消息，强制客户区域重绘制
            windll.user32.InvalidateRect(hwnd, byref(rcInvalid), True)
            return 0
    else:
        """
        #TransparentPaint
        ps=PAINTSTRUCT()
        hdc=windll.user32.BeginPaint(hwnd,byref(ps))
        rcClip = ps.rcPaint
        rcClient=Rect()
        windll.user32.GetClientRect(hwnd,byref(rcClient))
        wkeTransparentPaint(webview,hwnd,hdc,rcClient.Left,rcClient.Top,rcClient.Right,rcClient.Bottom)
        windll.user32.EndPaint(hwnd,byref(ps))
        """
    return

class WebViewWithProcHwnd(WebView):
    def __init__(self,isTransparent=False,isZoom=True):
        super().__init__()
        self.hwndMsgAdapter = HwndMsgAdapter()
        self.isZoom=isZoom
        self.isTransparent = isTransparent
        return

    def bind(self,hwnd=0,x=0,y=0,width=640,height=480):
        if windll.user32.IsWindow(hwnd)==0:
            return 0

        super().bind(hwnd,x,y,width,height)

        if self.isTransparent:
            self.setTransparent(1)
            exStyle=windll.user32.GetWindowLongW(hwnd,WkeConst.GWL_EXSTYLE)
            windll.user32.SetWindowLongW(hwnd,WkeConst.GWL_EXSTYLE,exStyle | WkeConst.WS_EX_LAYERED)
        else:
            self.setTransparent(0)

        Wke.event.onPaintUpdated(self,wkeEventOnPaint,param=self.hwnd)

        self.hwndMsgAdapter.registerMsgProc(WM_SIZE,wkeMsgProcResize)
        self.hwndMsgAdapter.registerMsgProc(WM_PAINT,wkeMsgProcPaint)
        self.hwndMsgAdapter.registerMsgProc(WM_DESTROY,wkeMsgProcQuit)
        self.hwndMsgAdapter.registerMsgProc(WM_KEYDOWN,wkeMsgProcKeyDown)
        self.hwndMsgAdapter.registerMsgProc(WM_KEYUP,wkeMsgProcKeyUp)
        self.hwndMsgAdapter.registerMsgProc(WM_CHAR,wkeMsgProcChar)
        self.hwndMsgAdapter.registerMsgProc(WM_ERASEBKGND,wkeMsgProcEraseBackground)
        self.hwndMsgAdapter.registerMsgProc(WM_INPUTLANGCHANGE,wkeMsgProcInputLangChange)
        self.hwndMsgAdapter.registerMsgProc([WM_LBUTTONDOWN,WM_MBUTTONDOWN,WM_RBUTTONDOWN,WM_LBUTTONDBLCLK,WM_MBUTTONDBLCLK,WM_RBUTTONDBLCLK,WM_LBUTTONUP,WkeConst.WM_MBUTTONUP,WkeConst.WM_RBUTTONUP],wkeMsgProcMouseClick)
        self.hwndMsgAdapter.registerMsgProc(WM_MOUSEMOVE,wkeMsgProcMouseMove)
        self.hwndMsgAdapter.registerMsgProc(WM_MOUSEWHEEL,wkeMsgProcMouseWheel)
        self.hwndMsgAdapter.registerMsgProc(WM_CONTEXTMENU,wkeMsgProcMouseContextMenu)
        self.hwndMsgAdapter.registerMsgProc(WM_NCHITTEST,wkeMsgProcNchiTest)
        self.hwndMsgAdapter.registerMsgProc(WM_SETCURSOR,wkeMsgProcSetCursor)
        self.hwndMsgAdapter.registerMsgProc(WM_SETFOCUS,wkeMsgProcSetFocus)
        self.hwndMsgAdapter.registerMsgProc(WM_KILLFOCUS,wkeMsgProcKillFocus)
        self.hwndMsgAdapter.registerMsgProc(WM_IME_STARTCOMPOSITION,wkeMsgProcStartComposition)
        self.hwndMsgAdapter.attach(self.hwnd,self)

        return 
    


