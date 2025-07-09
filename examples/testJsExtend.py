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





def jsCallpy(**kwargs):
    global j_webview

    es=kwargs['es']
    webview =kwargs['param']
    hwnd = webview.hwnd
    arg_count=Wke.jsArgCount(es)
    val_ls=Wke.getJsArgs(es,arg_count)

    #print("args:",val_ls)

    wkeMessageBox(f"func:jsCallpy\n args:{pformat(val_ls)}","Python",hwnd)

    webview.runJsCode('alert("Send to Javascript : alert('+str(val_ls)+')")')        

    return 0

def extendJS(**kwargs):
    global j_webview

    es=kwargs['es']
    webview =kwargs['param']
    hwnd = webview.hwnd
    arg_count=Wke.jsArgCount(es)
    val_ls=Wke.getJsArgs(es,arg_count)
    #print("args:",val_ls)
    wkeMessageBox(f"func:extendJS\n args:{pformat(val_ls)}","Python",hwnd)

    if val_ls[0]=='confirm':

        ret = webview.runJsCode('confirm("是否开启一个新窗口?")')
        if ret:
            j_webview = WebWindow()
            j_webview.create(0,0,0,400,300)
            j_webview.loadURL('https://www.hao123.com/')
            j_webview.showWindow()

    return 0

  

def testJsExtend():

    webview = WebWindow()
    webview.create(0,0,0,400,300)

    hwnd = webview.getWindowHandle()
    
    wkeSetIcon(hwnd,f'{father_folder}/logo.ico')


    Wke.extend(jsCallpy,'jsCallpy', param=webview)
    Wke.extend(extendJS,'extendJS', param=webview)

    webview.loadFile(f'{father_folder}/res/testdata/testJsExtend.html')


    webview.showWindow(True)
    Wke.runMessageLoop()
    return 






def main():
    
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)
    testJsExtend()  

if __name__=='__main__':
    main()

