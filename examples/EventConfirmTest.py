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

    def OnConfirmEvent(context,*args,**kwargs):
        param = context["param"]
        print(f"{str(param)} \nargs:{pformat(args)}\nkwargs:{pformat(kwargs)}\n=======================\n")

        msg = kwargs["msg"]
        windowTitle = ""
        response = win32api.MessageBox(
                None,
                msg,
                windowTitle,
                win32con.MB_YESNO | win32con.MB_ICONQUESTION
            )
            
        # 根据用户选择返回 True 或 False
        if response == win32con.IDYES:
            return True
        elif response == win32con.IDNO:
            return False



    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True


    webview.onConfirmBox(OnConfirmEvent,'Confirm')
    webview.onWindowClosing(OnCloseEvent,param='App Quit')
    #webview.onDocumentReady2(OnTheEvent,'Document is Ready')

    #webview.loadURL("https://www.w3school.com.cn/tiy/t.asp?f=jsck_confirm_3")   
    webview.loadFile(f'{father_folder}/res/testdata/confirm.html')
    
    webview.showWindow(True)
    #wkePumpMessages()
    Wke.runMessageLoop()
    #win32gui.PumpMessages()

if __name__=='__main__':
    main()