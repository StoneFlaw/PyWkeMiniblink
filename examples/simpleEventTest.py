# -*- coding:utf-8 -*-
import os,sys,platform,time
from pprint import *
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

    def OnTheEvent(context,*args,**kwargs):
        param = context["param"]
        print(f"{str(param)} \nargs:{pformat(args)}\nkwargs:{pformat(kwargs)}\n=======================\n")
        return 0

    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True


    
    webview.onTitleChanged(OnTheEvent,'TITLE Changed')
    webview.onWindowClosing(OnCloseEvent,param='App Quit')
    #webview.onDocumentReady2(OnTheEvent,'Document is Ready')


    
    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
    webview.showWindow(True)
    #wkePumpMessages()
    Wke.runMessageLoop()
    #win32gui.PumpMessages()

if __name__=='__main__':
    main()