# -*- coding:utf-8 -*-
import os,sys,platform,time
from pathlib import Path
import win32gui

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))
sys.path.append(father_folder)

from wkeMiniblink.wke import Wke,WebView,WebWindow
from wkeMiniblink.wkeEvent import WkeEvent
from wkeMiniblink.wkeWin32 import *

def main():
    Wke.init()
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    webview = WebWindow()
    webview.create(0,0,0,800,600)
    snap = WkeSnapShot()
    snap.bind(webview.getWindowHandle())
    setattr(webview,"snap",snap)

    
    def OnCloseEvent(context,*args,**kwargs):
        sc = context["webview"].snap
        sc.capture()
        sc.saveAsPng("screenshot.png")
        win32gui.PostQuitMessage(0)
        return True
    

    webview.onWindowClosing(OnCloseEvent,param='App Quit')
    
    webview.loadFile(f'{father_folder}/res/testdata/testjs.html')
    webview.showWindow(True)
    wkePumpMessages()
    #Wke.runMessageLoop()
    #win32gui.PumpMessages()

if __name__=='__main__':
    main()