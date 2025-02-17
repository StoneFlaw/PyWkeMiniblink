# -*- coding:utf-8 -*-
import sys,os
from ctypes import c_int
from platform import architecture
from pkgutil import extend_path

__version__ = "0.1.16"
__path__ = extend_path(__path__, __name__)

bit=architecture()[0]

_LRESULT=c_int
MINIBLINK_DLL_PATH =""
MINIBLINK_DLL_HANDLE=None

miniblink_core_dll = '\\miniblink.dll'
if bit == '64bit':
    from ctypes import c_longlong
    miniblink_core_dll = '\\miniblink_4975_x64.dll'
    _LRESULT=c_longlong
else:
    miniblink_core_dll = '\\miniblink_4975_x32.dll'
    _LRESULT=c_int

def SetMiniblinkDLL(dll):
    global MINIBLINK_DLL_HANDLE
    MINIBLINK_DLL_HANDLE = dll
    return
def GetMiniblinkDLL():
    global MINIBLINK_DLL_HANDLE
    return MINIBLINK_DLL_HANDLE



def find_miniblink():
    global MINIBLINK_DLL_PATH 

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        #print('running in a PyInstaller bundle')
        # sys._MEIPASS -> _internal directory -D/Temp Folder -F   
        #PyInstaller bundle模式下,释放非exe文件目录就是DLL默认目录位置
        dll_dir = os.path.realpath(sys._MEIPASS)
    else:
        #解释器模式下,解释器目录就是DLL默认目录位置
        dll_dir = os.path.dirname(sys.executable)

    if not os.path.isfile(dll_dir + miniblink_core_dll):
        path = os.environ['PATH']

        #wkeMiniblink Package目录   
        dll_dir = os.path.dirname(__file__) + '\\bin'
        if os.path.isfile(dll_dir + miniblink_core_dll):
            path = dll_dir + ';' + path
            os.environ['PATH'] = path
            MINIBLINK_DLL_PATH = dll_dir + miniblink_core_dll
        else:
            #去系统环境变量下找
            for dll_dir in path.split(';'):
                if os.path.isfile(dll_dir + miniblink_core_dll):
                    MINIBLINK_DLL_PATH = dll_dir + miniblink_core_dll
                    break
            else:
                return
    else:
        MINIBLINK_DLL_PATH = dll_dir + miniblink_core_dll

    try:
        os.add_dll_directory(dll_dir)
    except AttributeError:
        pass


find_miniblink()
del find_miniblink


class WkeCallbackError(RuntimeError):
    pass

