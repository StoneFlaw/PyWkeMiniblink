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



from wkeMiniblink.wke import *
from wkeMiniblink.wkeEvent import *
from wkeMiniblink.wkeWin32 import *

import win32gui
from win32con import *
from ctypes import windll


init_path=os.getcwd()
icon_path=f'{father_folder}/logo.ico'



user32=windll.user32

def WndProc(hwnd,msg,wParam,lParam):
    if msg == WM_PAINT:
        rect=Rect()
        user32.GetClientRect(hwnd,byref(rect))
        #webview.resize(rect.Right - rect.Left,rect.Bottom - rect.Top)
    if msg == WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0
    return win32gui.DefWindowProc(hwnd,msg,wParam,lParam)
    
def get_hwnd(x=0,y=0,w=860,h=760):
    wc = win32gui.WNDCLASS()
    wc.hbrBackground = COLOR_BTNFACE + 1
    wc.hCursor = win32gui.LoadCursor(0,IDI_APPLICATION)
    wc.lpszClassName = "MBPython"
    wc.style =  CS_GLOBALCLASS|CS_VREDRAW | CS_HREDRAW
    wc.lpfnWndProc = WndProc
    reg = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindowEx(0, reg,'自创建Win窗口',WS_OVERLAPPEDWINDOW,300,100,860,760, 0, 0, 0, None)
    return hwnd,x,y,w,h


def testOnEventAll():

    Wke.init()
    webview = WebviewWindow()
    webview.create(0,0,0,0,800,600)
    def OnEvent(w,param,*args,**kwargs):
        print(f"{str(param)} \nargs:{pformat(args)}\nkwargs:{pformat(kwargs)}\n=======================\n")
        return 0
    

    def OnCloseEvent(w,param,*args,**kwargs):
        print(f"{str(param)} \nargs:{pformat(args)}\nkwargs:{pformat(kwargs)}\n=======================\n")
        win32gui.PostQuitMessage(0)
        return True


    event = Wke.event

    event.onWindowClosing(webview,OnEvent,'Title Changed')
    event.onURLChanged2(webview,OnEvent,'URL Changed')
    event.onDocumentReady2(webview,OnEvent,'Document is Ready')
    event.onMouseOverUrlChanged(webview,OnEvent,'Mouse over URL')
    event.onWindowClosing(webview,OnCloseEvent,'Closing Window')
    event.onAlertBox(webview,OnEvent,'AlertBox')
    event.onConfirmBox(webview,OnEvent,'ConfirmBox')
    event.onPromptBox(webview,OnEvent,'PromptBox')
    event.onConsole(webview,OnEvent,'Console')
    event.onDownload(webview,OnEvent,'Download')

    #event.onNetResponse(webview,OnEvent,'NetResponse')
    event.onLoadUrlEnd(webview,OnEvent,'LoadUrlEnd')



    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
    webview.showWindow(True)
    Wke.runMessageLoop()



if __name__=='__main__':
    
    testOnEventAll()   