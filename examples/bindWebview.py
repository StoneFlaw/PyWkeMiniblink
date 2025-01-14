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
from wkeMiniblink.wkeWin32ProcMsg import *


init_path=os.getcwd()
icon_path=f'{father_folder}/logo.ico'


user32=windll.user32





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

def test():


    x,y,w,h = 0,0,640,480

    hwnd = createTransparentWindow('自创建Win窗口',x,y,w,h)
    
    setIcon(hwnd,icon_path)
    webview = WebviewWithProcHwnd(isTransparent=True,isZoom=False)
    webview.bind(hwnd,x,y,w,h)   
    
    #'https://www.w3school.com.cn/jsref/index.asp'

    #webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
    webview.loadFile(f'{father_folder}/res/testdata/testjs.html')

    Wke.extend(jsWindowExtend,'jsWindowExtend', param=webview)
    #webview.showWindow(True)
    win32gui.ShowWindow(hwnd,SW_SHOWNORMAL)
    win32gui.PumpMessages()
    return



if __name__=='__main__':

    Wke.init()
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version())

    test()


 

