# -*- coding:utf-8 -*-
import os,sys,platform,time
from pprint import *
from pathlib import Path
import win32gui



current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))


from wkeMiniblink.wke import Wke,WebView,WebWindow
from wkeMiniblink.wkeEvent import WkeEvent
from wkeMiniblink.wkeWin32 import *


import tkinter as tk
from tkinter import simpledialog

def input_box( prompt,defaultResult):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    windowTitle = ""
    user_input = simpledialog.askstring(windowTitle,prompt,initialvalue=defaultResult)
    root.destroy()  # Destroy the main window after input
    return user_input

def main():
    
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)
    webview = WebWindow()
    webview.create(0,0,0,400,300)

    def OnPromtEvent(context,*args,**kwargs):
        param = context["param"]
        print(f"{str(param)} \nargs:{pformat(args)}\nkwargs:{pformat(kwargs)}\n=======================\n")

        msg = kwargs["msg"]
        default = kwargs["defaultResult"]
    
        result = input_box(msg, default)

        return  result

    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True

    webview.onPromptBox(OnPromtEvent,'PromptBox')
    webview.onWindowClosing(OnCloseEvent,param='App Quit')
    #webview.onDocumentReady2(OnTheEvent,'Document is Ready')
 
    #webview.loadURL('https://www.w3school.com.cn/tiy/t.asp?f=jsck_prompt_1')
    webview.loadFile(f'{father_folder}/res/testdata/prompt.html')

    webview.moveToCenter()
    webview.showWindow(True)
    #wkePumpMessages()
    Wke.runMessageLoop()
    #win32gui.PumpMessages()

if __name__=='__main__':
    main()