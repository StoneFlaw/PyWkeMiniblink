# -*- coding:utf-8 -*-
import os
import sys
import time
from pathlib import Path
from pprint import pformat

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))



import ctypes
import win32gui
from win32con import *
from ctypes import windll


from wkeMiniblink.wke import Wke,WebView,WebWindow
from wkeMiniblink.wkeEvent import WkeEvent
from wkeMiniblink.wkeWin32 import *


def runJsCode(**kwargs):
  

    es=kwargs['es']
    webview =kwargs['param']
    hwnd = webview.hwnd
    arg_count=Wke.jsArgCount(es)
    val_ls=Wke.getJsArgs(es,arg_count)
    #print("args:",val_ls)
    code = ""
    for v in val_ls:
        code = code + str(v)
    ret = webview.runJsCode(code)
    return ret

def testJs():
    #没什么用,js和py的互相返回值没验证,用不了
    webview = WebWindow()
    webview.create(0,0,0,400,300)

    hwnd = webview.getWindowHandle()
    
    wkeSetIcon(hwnd,f'{father_folder}/logo.ico')

    Wke.extend(runJsCode,'runJsCode', param=webview)

    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True
    webview.onWindowClosing(OnCloseEvent,param='App Quit')
    
    webview.loadFile(f'{father_folder}/res/testdata/testRunJs.html')
    
    webview.moveToCenter()
    webview.showWindow(True)
    Wke.runMessageLoop()
    return 






def main():
    
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)  
    testJs()  

if __name__=='__main__':
    main()

