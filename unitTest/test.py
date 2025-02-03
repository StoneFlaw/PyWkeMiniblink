# -*- coding:utf-8 -*-
import os
import sys
import time
from pathlib import Path
from pprint import pformat
import random
import unittest


current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))
sys.path.append(father_folder)


import ctypes
import win32gui
from win32con import *
from ctypes import windll

from wkeMiniblink.miniblink import *
from wkeMiniblink.wke import Wke,WebView,WebWindow
from wkeMiniblink.wkeEvent import *
from wkeMiniblink.wkeWin32 import *

user32=windll.user32

class Test( unittest . TestCase ):
    def setUp( self ):

        self.webview = WebWindow()
        self.webview.create(0,0,0,800,600)
        self.webview.loadFile(f'{father_folder}/res/testdata/index.html')
        return
        

    def tearDown(self) -> None:
        self.webview.destroy()
        return super().tearDown()
    
    def test_webviewUserKey( self ):
        self.webview.setUserKeyValue("index",self.webview)
        v = self.webview.getUserKeyValue("index")
        self.assertEqual(v,self.webview)
        return

if __name__=='__main__':
    Wke.init()
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    suit = unittest.TestSuite()
    suit.addTests( [Test("test_webviewUserKey")])
    runner = unittest.TextTestRunner()
    runner.run(suit)
 

