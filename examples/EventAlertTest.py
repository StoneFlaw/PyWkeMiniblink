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
    
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)
    webview = WebWindow()
    webview.create(0,0,0,400,300)

    def OnAlertEvent(context,*args,**kwargs):
        param = context["param"]
        print(f"{str(param)} \nargs:{pformat(args)}\nkwargs:{pformat(kwargs)}\n=======================\n")

        msg = kwargs["msg"]
        windowTitle = ""
        result  = win32gui.MessageBox(0, msg, windowTitle, win32con.MB_OK)

        return  result

    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True

    webview.onAlertBox(OnAlertEvent,'Alert')
    webview.onWindowClosing(OnCloseEvent,param='App Quit')
    #webview.onDocumentReady2(OnTheEvent,'Document is Ready')

    #webview.loadURL('https://www.w3school.com.cn/tiy/t.asp?f=jsck_alert_2')
    webview.loadFile(f'{father_folder}/res/testdata/alert.html')
    webview.moveToCenter()
    webview.showWindow(True)
    #wkePumpMessages()
    Wke.runMessageLoop()
    #win32gui.PumpMessages()

if __name__=='__main__':
    main()