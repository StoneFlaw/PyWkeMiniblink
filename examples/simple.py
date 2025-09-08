# -*- coding:utf-8 -*-
import os,sys,platform,time
from pathlib import Path
import win32gui

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))


from wkeMiniblink.wke import Wke,WebView,WebWindow
from wkeMiniblink.wkeEvent import WkeEvent
from wkeMiniblink.wkeWin32 import *

def main():
  
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)
    webview = WebWindow()
    webview.create(0,0,0,800,600)
    webview.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    wkeSetIcon(webview.hwnd,f'{father_folder}/logo.ico')

    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True
    webview.onWindowClosing(OnCloseEvent,param='App Quit')
    
    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
    webview.showWindow(True)
    wkePumpMessages()
    #Wke.runMessageLoop()
    #win32gui.PumpMessages()

if __name__=='__main__':
    main()