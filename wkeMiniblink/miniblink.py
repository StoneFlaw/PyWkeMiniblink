# -*- coding:utf-8 -*-
import platform
from ctypes import (
    c_int,
    c_uint,
    c_long,
    c_longlong,
    c_float,
    c_char_p,
    c_wchar_p,
    c_bool,
    c_size_t,
    c_void_p,
    POINTER,
    py_object,
    cdll,
    CFUNCTYPE
)
from . import _LRESULT,GetMiniblinkDLL,SetMiniblinkDLL
from .wkeStruct import *

mb = GetMiniblinkDLL()

def pyWkeGetString(binary,encoding='utf-8'):
    global mb
    b = mb.wkeGetString(binary)
    if b :
        return b.decode(encoding)
    return ""

def pyWkeSetString(wkeStr,text,encoding='utf-8'):
    global mb
    utf8 = text.encode(encoding)
    l = len(utf8)
    b = mb.wkeSetString(wkeStr,utf8,l)
    return b

def pyWkeCreateString(text,encoding='utf-8'):
    global mb
    utf8 = text.encode(encoding)
    l = len(utf8)
    wkeStr = mb.wkeCreateString(utf8,l)
    return wkeStr

