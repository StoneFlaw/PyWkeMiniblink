# -*- coding:utf-8 -*-
import os
import sys
import time
from pathlib import Path
from pprint import pformat

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))
sys.path.append(father_folder)


import ctypes
import win32gui
from win32con import *
from ctypes import windll


from wkeMiniblink.wke import Wke,WebView,WebWindow
from wkeMiniblink.wkeEvent import WkeEvent
from wkeMiniblink.wkeWin32 import *








user32=windll.user32

SetWindowLong= windll.user32.SetWindowLongA
GetWindowLong = windll.user32.GetWindowLongA

def WndProc(hwnd,msg,wParam,lParam):
    if msg == WM_PAINT:
        rect=Rect()
        user32.GetClientRect(hwnd,byref(rect))
      
        cPtrOfPyobj = GetWindowLong(hwnd,GWL_USERDATA)
        pyObj = ctypes.cast(cPtrOfPyobj,py_object)
        view =  pyObj.value
        view.resize(rect.Right - rect.Left,rect.Bottom - rect.Top)
    if msg == WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0
    return win32gui.DefWindowProc(hwnd,msg,wParam,lParam)
    
def get_hwnd(x=0,y=0,w=860,h=760,view=None):
    wc = win32gui.WNDCLASS()
    wc.hbrBackground = COLOR_BTNFACE + 1
    wc.hCursor = win32gui.LoadCursor(0,IDI_APPLICATION)
    wc.lpszClassName = "Miniblink"
    wc.style =  CS_GLOBALCLASS|CS_VREDRAW | CS_HREDRAW
    wc.lpfnWndProc = WndProc
    wc.cbWndExtra = 32
    reg = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindowEx(0, reg,'自创建Win窗口',WS_OVERLAPPEDWINDOW,x,y,w,h, 0, 0, 0, None)

    cPtrOfPyobj = ctypes.py_object(view)  
    SetWindowLong(hwnd,GWL_USERDATA,cPtrOfPyobj)

    return hwnd,x,y,w,h




def jsWindowExtend(**kwargs):
    es=kwargs['es']
    webview =kwargs['param']
    hwnd = webview.hwnd

    arg_count=Wke.jsArgCount(es)
    val_ls=Wke.getJsArgs(es,arg_count)
    if val_ls[0]=='move':
        user32.ReleaseCapture()
        user32.SendMessageW(hwnd,161, 2, 0)
    elif val_ls[0]=='close':
        win32gui.PostQuitMessage(0)
    elif val_ls[0]=='max':
        ismax=user32.IsZoomed(hwnd)
        if ismax==0:
            user32.ShowWindow(hwnd,3)
        elif ismax==1:
            user32.ShowWindow(hwnd,1)
    elif val_ls[0]=='min':
        user32.ShowWindow(hwnd,2)
    elif val_ls[0]=='menu':
        return Wke.setJsArgs(es,'click-menu')
    return 0

def jsCallpy(**kwargs):
    global j_webview

    es=kwargs['es']
    webview =kwargs['param']
    
    arg_count=Wke.jsArgCount(es)
    val_ls=Wke.getJsArgs(es,arg_count)

    print("args:",val_ls)

    hwnd = webview.hwnd
    webview.runJsCode('alert("jsCallpy'+str(val_ls)+'")')        

    return 0

def jsExtendConfirm(**kwargs):
    global j_webview

    es=kwargs['es']
    webview =kwargs['param']

    arg_count=Wke.jsArgCount(es)
    val_ls=Wke.getJsArgs(es,arg_count)
    print("args:",val_ls)

    hwnd = webview.hwnd
    if val_ls[0]=='confirm':

        webview.runJsCode('confirm("confirm")')

        j_webview = WebWindow()
        j_webview.create(0,0,0,400,300)
        j_webview.loadURL('https://www.hao123.com/')
        j_webview.showWindow()

    return 0

  
def testCreateWindwow():
    webview = WebWindow()

    webview.create(0,0,0,800,600)

    hwnd = webview.getWindowHandle()
    
    wkeSetIcon(hwnd,f'{father_folder}/logo.ico')

    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True
    Wke.event.onWindowClosing(webview,OnCloseEvent,'Closing Window')
    
    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
    webview.showWindow(True)
    Wke.runMessageLoop()
    return   

def testBindWindwow():
    webview = WebWindow()

    hwnd,x,y,w,h = get_hwnd(0,0,640,480,webview)
    
    wkeSetIcon(hwnd,f'{father_folder}/logo.ico')
    webview.build(hwnd,x,y,w,h)   

    #'https://www.w3school.com.cn/jsref/index.asp'
    #http://192.168.1.130/nav/
    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
 
    webview.showWindow(True)
    win32gui.ShowWindow(hwnd,SW_SHOWNORMAL)

    win32gui.PumpMessages()
    return





def testJsExtend():

    webview = WebWindow()
    webview.create(0,0,0,800,600)

    hwnd = webview.getWindowHandle()
    
    wkeSetIcon(hwnd,f'{father_folder}/logo.ico')

    Wke.extend(jsWindowExtend,'jsWindowExtend', param=webview)
    Wke.extend(jsCallpy,'jsCallpy', param=webview)
    Wke.extend(jsExtendConfirm,'extendConfirm', param=webview)

    webview.loadFile(f'{father_folder}/res/testdata/testjs.html')


    webview.showWindow(True)
    Wke.runMessageLoop()
    return 



def testOnEvent():

    webview = WebWindow()
    webview.create(0,0,0,800,600)
    hwnd = webview.getWindowHandle()
    
    wkeSetIcon(hwnd,f'{father_folder}/logo.ico')

    def OnEvent(context,*args,**kwargs):
        param = context["param"]
        #url = kwargs["url"]
        #w.runJsCode(f'alert("URL:{url}")')
        print(f"{str(param)} \nargs:{pformat(args)}\nkwargs:{pformat(kwargs)}\n=======================\n")
        return 0
    
    event = Wke.event
    event.onDocumentReady2(webview,OnEvent,'onDocument')
    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
    webview.showWindow(True)
    Wke.runMessageLoop()



def main():
    
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version())
 
    msg = '''==================
    1. testCreateWindow
    2. testBindWindow

    6. testJsExtend
    7. testEvent
    ==================
    '''
    print(msg)


    c = input()
    if c == '1':
        testCreateWindwow()
    elif c == '2':
        testBindWindwow()

    elif c == '6':
        testJsExtend()  
    elif c == '7':
        testOnEvent()   

if __name__=='__main__':
    main()

