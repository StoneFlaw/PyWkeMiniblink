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
from wkeMiniblink.wkeWin32ProcMsg import wkeMsgProcResize,wkeMsgProcQuit

def main():
    
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)
    webview = WebWindow()

    x,y,w,h = 0,0,640,480

    hwnd = wkeCreateWindow('自创建Win窗口',x,y,w,h)
    webview.build(hwnd,x,y,w,h)   
    wkeSetIcon(hwnd,f'{father_folder}/logo.ico')

    a = HwndMsgAdapter()
    a.registerMsgProc(WM_SIZE,wkeMsgProcResize)
    a.registerMsgProc(WM_DESTROY,wkeMsgProcQuit)
    a.attach(hwnd,webview)

    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True
    
    webview.onWindowClosing(OnCloseEvent,param='App Quit')
   
    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')

    webview.showWindow(True)
    win32gui.ShowWindow(hwnd,SW_SHOWNORMAL)
    wkePumpMessages()
    #Wke.runMessageLoop()
    #win32gui.PumpMessages()

if __name__=='__main__':
    main()