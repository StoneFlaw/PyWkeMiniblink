# -*- coding:utf-8 -*-
import os,sys,platform,time
import win32gui
from wkeMiniblink.wke import *
from wkeMiniblink.wkeEvent import *
from wkeMiniblink.wkeWin32 import *

if __name__=='__main__':
    Wke.init()
    webview = WebviewWindow()
    webview.create(0,0,0,0,800,600)
    def OnCloseEvent(w,param,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True
    Wke.event.onWindowClosing(webview,OnCloseEvent,param='App Quit')
    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
    webview.showWindow(True)
    Wke.runMessageLoop()
 

