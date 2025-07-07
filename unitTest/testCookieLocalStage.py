# -*- coding:utf-8 -*-
import os
import sys
import time
from pathlib import Path
from pprint import pformat
import random
import shutil
import unittest


current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))
sys.path.append(father_folder)


import ctypes
import win32gui
from win32con import *
from ctypes import windll
from threading import  Lock,Event,Thread

from wkeMiniblink.miniblink import *
from wkeMiniblink.wke import Wke,WebView,WebWindow
from wkeMiniblink.wkeEvent import *
from wkeMiniblink.wkeWin32 import *

from wkeMiniblink.wkeWin32ProcMsg import wkeMsgProcResize,wkeMsgProcQuit

user32=windll.user32
cookiePath = f'{father_folder }\\build\\cookie.dat'
localStagePath=f'{father_folder }\\build\\LocalStage'


class Test( unittest . TestCase ):
    """

    消息分发循环30秒后发出WM_QUIT消息，退出GUI后验证cookie和LocalStage是否设置到
    """
  
    def test_webview( self ):
        if os.path.exists(cookiePath ):
            os.remove(cookiePath)
        if os.path.exists(localStagePath):
            shutil.rmtree(localStagePath)
        self.assertEqual(os.path.isfile(cookiePath),False)
        self.assertEqual(os.path.isdir(localStagePath),False)
        Wke.init()
       
        print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)


    
        webview = WebWindow()
        webview.create(0,0,0,400,300)
        #webview.setCookieAndStagePath(cookie=cookiePath,localStage=localStagePath)
        webview.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')

        #需要网页确实触发Cookie和Stage动作
        webview.loadFile(f'{father_folder}/res/testdata/countdown.html')
        webview.moveToCenter()
        webview.showWindow(True)

        t0 = time.time()
        msg = MSG()
        while True:
            res = windll.user32.PeekMessageA(byref(msg), None,0, 0, 1)
            if  res != 0:
                windll.user32.TranslateMessage(byref(msg))
                windll.user32.DispatchMessageA(byref(msg))
                if msg.message in[WM_QUIT]: 
                    break
            else:
                time.sleep(0.05)

            t1 = time.time()
            if t1-t0 > 30:
                win32gui.PostQuitMessage(0)


        self.assertEqual(os.path.isfile(cookiePath),True)
        self.assertEqual(os.path.isdir(localStagePath),True)
        return


    
if __name__=='__main__':

    suit = unittest.TestSuite()
    suit.addTests( [Test("test_webview")])
    runner = unittest.TextTestRunner()
    runner.run(suit)

 
 

