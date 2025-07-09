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
from . import *
from .wkeStruct import *

def pyWkeGetString(wkeStr,encoding='utf-8'):
    """获取c wkeString指针中字符串
    Args:
        wkeStr(c_char_p):   wkeString zi
    Returns:
        str: 字符串
    """
    b = wkeGetString(wkeStr)
    if b :
        return b.decode(encoding)
    return ""

def pyWkeSetString(wkeStr,text,encoding='utf-8'):
    """设置c wkeString指针中字符串
    Args:
        wkeStr(c_char_p):   JS对象
        text(str):   JS对象
    Returns:
        int: 返回值
    """
    utf8 = text.encode(encoding)
    l = len(utf8)
    b = wkeSetString(wkeStr,utf8,l)
    return b

def pyWkeCreateString(text,encoding='utf-8'):
    """创建c wkeString指针
    Args:
        binary(c_char_p):   JS对象
    Returns:
        c_char_p: c wkeString指针
    """
    utf8 = text.encode(encoding)
    l = len(utf8)
    wkeStr = wkeCreateString(utf8,l)
    return wkeStr

