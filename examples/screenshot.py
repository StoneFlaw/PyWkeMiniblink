# -*- coding:utf-8 -*-
import os,sys,platform,time
from pathlib import Path
import win32gui
from pprint import pformat

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))


from wkeMiniblink.wke import Wke,WebView,WebWindow
from wkeMiniblink.wkeEvent import WkeEvent
from wkeMiniblink.wkeWin32 import *

def snapshot(**kwargs):
    global j_webview

    es=kwargs['es']
    webview =kwargs['param']
    hwnd = webview.hwnd
    arg_count=Wke.jsArgCount(es)
    val_ls=Wke.getJsArgs(es,arg_count)

    sc = webview.snap

    wkeMessageBox(f"func:snapshot\n args:{pformat(val_ls)}","Python",hwnd)

    sc.capture()
    sc.saveAsPng(f"{father_folder}/build/screenshot.png")
 
    return 0

def main():
    
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)
    webview = WebWindow()
    webview.create(0,0,0,640,480)
    snap = WkeSnapShot()
    snap.bind(webview.getWindowHandle())
    setattr(webview,"snap",snap)

    Wke.extend(snapshot,'snapshot', param=webview)

    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True
    

    webview.onWindowClosing(OnCloseEvent,param='App Quit')
    
    webview.loadFile(f'{father_folder}/res/testdata/testSnapShot.html')
    webview.moveToCenter()
    webview.showWindow(True)

    wkePumpMessages()
    #Wke.runMessageLoop()
    #win32gui.PumpMessages()

if __name__=='__main__':
    main()