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
cookiePath = f'{father_folder }/build/cookie.dat'
localStagePath=f'{father_folder }/build/LocalStage'


count = 0
class Test( unittest . TestCase ):
    """

    """
    
    def test_Timer( self ):
        #无指定窗口
        global count
        def timeCallback(*args,**kwargs):
            global count
            count = count+1
            if count>=9:
                owner = kwargs["owner"]
                owner.stop()
                win32gui.PostQuitMessage(0)
            return

        t = WkeTimer()    
        t.init(timeCallback,None,0,3000)
        t.start()
        Wke.runMessageLoop()
        self.assertEqual(count,9)
        return


    
if __name__=='__main__':
    Wke.init()
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    suit = unittest.TestSuite()
    suit.addTests( [Test("test_Timer")])
    runner = unittest.TextTestRunner()
    runner.run(suit)

 
 

