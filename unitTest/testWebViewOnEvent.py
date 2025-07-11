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


class Test( unittest . TestCase ):
    """

    """
  
    def test_webview( self ):

        webview = WebWindow()
        entries = Wke.event.eventEntries
        for event in entries:
            has = hasattr(webview,event)
            self.assertEqual(hasattr(webview,event),True)
            try:
                func = entries[event]
                doc  = func.__doc__
                lines = str(doc).splitlines()
                print(f"def {event}(self,func,param,*args,**kwargs):")
                print("    \"\"\"",lines[0],"\"\"\"")
                print(f"    return Wke.event.{event}(self,func,param,*args,**kwargs)")         
            except:
                pass      
        return


    
if __name__=='__main__':
    
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    print("Miniblink Version :",Wke.version,"\n Version:",Wke.Version(),"\n DLL:",Wke.dllPath)
    suit = unittest.TestSuite()
    suit.addTests( [Test("test_webview")])
    runner = unittest.TextTestRunner()
    runner.run(suit)

 
 

