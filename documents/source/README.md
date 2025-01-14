# 简介

Miniblink 是 chromium的精简版,裁剪了对于排版渲染没啥大用的如音视频功能。

PyWkeMiniblink 是 Miniblink的Python绑定。

# 安装

要求 pywin32

`pip3 install WkeMiniblink-0.1.1-py3-none-any.whl`



# 示例

  

```python
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
```



# Javascript integration


```python

```

# Plugins and Flash support

Miniblink supports NPAPI plugins.

# Off-screen rendering

