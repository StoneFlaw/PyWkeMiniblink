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
from wkeMiniblink.wkeWin32ProcMsg import *

from wkeMiniblink.wkeWin32ProcMsg import wkeMsgProcResize,wkeMsgProcQuit




user32=windll.user32

def main():
    
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)
    webview = WebWindow()
    x,y,w,h = 0,0,640,480

    hwnd = wkeCreateWindow('自创建Win窗口',x,y,w,h)
    
    wkeSetIcon(hwnd,f'{father_folder}/logo.ico')
    webview.build(hwnd,x,y,w,h)
 
    webview.loadURL(f'baidu.com')


    a = HwndMsgAdapter()

    a.registerMsgProc(WM_SIZE,wkeMsgProcResize)
    a.registerMsgProc(WM_DESTROY,wkeMsgProcQuit)
    a.attach(hwnd,webview)


    
    webview.showWindow(True)
    win32gui.ShowWindow(hwnd,SW_SHOWNORMAL)
    
    #'https://www.w3school.com.cn/jsref/index.asp'
    #http://192.168.1.130/nav/

    
    win32gui.PumpMessages()
    return



if __name__=='__main__':



    main()


 

