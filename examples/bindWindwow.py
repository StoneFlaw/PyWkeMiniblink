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


from wkeMiniblink.miniblink import *
from wkeMiniblink.wke import *
from wkeMiniblink.wkeEvent import *
from wkeMiniblink.wkeWin32 import *

from wkeMiniblink.wkeWin32ProcMsg import wkeMsgProcResize,wkeMsgProcQuit

init_path=os.getcwd()
icon_path=f'{father_folder}/logo.ico'

user32=windll.user32

def test():

    webview = WebviewWindow()
    x,y,w,h = 0,0,640,480

    hwnd = createWindow('自创建Win窗口',x,y,w,h)
    setIcon(hwnd,icon_path)
    webview.bind(hwnd,x,y,w,h)   
    
    a = HwndProcAdapter()

  
 
    a.registerMsgProc(WM_SIZE,wkeMsgProcResize)
    a.registerMsgProc(WM_DESTROY,wkeMsgProcQuit)
    a.attach(hwnd,webview)

    #'https://www.w3school.com.cn/jsref/index.asp'
    #http://192.168.1.130/nav/
    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
 
    webview.showWindow(True)
    win32gui.ShowWindow(hwnd,SW_SHOWNORMAL)
    win32gui.PumpMessages()
    return



if __name__=='__main__':

    Wke.init()
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version())

    test()


 
