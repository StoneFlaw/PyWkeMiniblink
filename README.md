# 简介

PyWkeMiniblink 是 [Miniblink](https://weolar.github.io/miniblink/)的Python绑定，参考自上游项目[MBPython](https://github.com/lochen88/MBPython)。

Miniblink 是 chromium的精简版，裁剪了对于排版渲染没啥大用的如音视频功能。



# 使用

## 安装

```shell
#安装依赖pywin32
pip3 install pywin32
pip3 install WkeMiniblink-xx-py3-none-any.whl
```

## 发布

pyinstall

## 示例

```python
# -*- coding:utf-8 -*-
import os,sys,platform,time
import win32gui
from wkeMiniblink.wke import *
from wkeMiniblink.wkeEvent import *
from wkeMiniblink.wkeWin32 import *

if __name__=='__main__':
    Wke.init()
    webview = WebWindow()
    webview.create(0,0,0,800,600)
    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True
    Wke.event.onWindowClosing(webview,OnCloseEvent,param='App Quit')
    webview.loadURL('https://www.w3school.com.cn/jsref/index.asp')
    webview.showWindow(True)
    Wke.runMessageLoop()
```

# 说明

## 全局接口Wke

### DLL初始化

静态类函数:Wke.init(DLL路径)

需要在所有Wke调用前加载一次，且后续所有wke相关的API调用需要在同一线程。

### Javascript 扩展

静态类函数:Wke.extend(py实现函数，js函数名,上下文参数)

使用一个指定的python函数作为js扩展实现的函数

Example:

```python
    webview = WebWindow()
    webview.create(0,0,0,800,600)
   
    def pyAction(**kwargs):
        es=kwargs['es']
        context =kwargs['param']
        webview = context
        arg_count=Wke.jsArgCount(es)
        val_ls=Wke.getJsArgs(es,arg_count)
        webview.runJsCode('alert("jsCallpy'+str(val_ls)+'")')
        return
    
    Wke.extend(pyAction,'jsCallpy', param=webview)
```

 在html/js 中调用

```html
<button onclick="jsCallpy('jsCallpy', 666)" style='margin-right: 20px;cursor: pointer;'>jsCallpy</button>
```

## 创建网页对象的方式

### 网页视图WebView

网页视图包括加载/渲染/设置/Js/Cookie等,但并不包括实际窗口功能。

### 网页窗口WebWindow

网页窗口继承自WebView，包括窗口功能。

1. WebWindow
    	WebWindow.create(0,x,y,h,w)由miniblink创建一个网页窗口，绘制与消息处理由miniblink内部处理；

    ​	无需额外处理窗口消息与绘制过程。

2. WebWindow
    	WebWindow.build(父窗口hwnd,x,y,h,w)在父窗口内部,由miniblink创建一个网页窗口；

    ​	需要关联处理父窗口与本窗口消息流程，主要为退出和调整大小的同步。

3. WebView
    	WebView.bind(父窗口hwnd,x,y,w,h)在一个已经创建的父窗口hwnd上绑定一个网页视图；

    ​	需要处理父窗口的消息流程，以及自身的离屏绘制。

    

## 窗口消息分发

三种消息读取分发循环：Wke.runMessageLoop()、win32gui.PumpMessages()、wkePumpMessages(block)	

自定义消息分发循环时可以参考wkePumpMessages的两种分发循环。

阻塞式

```python
while True:
    res = windll.user32.GetMessageA(byref(msg), None, 0, 0)
    if  res != 0:
        windll.user32.TranslateMessage(byref(msg))
        windll.user32.DispatchMessageA(byref(msg))
    elif res == 0:
        windll.user32.TranslateMessage(byref(msg))
        windll.user32.DispatchMessageA(byref(msg))
        break
    else:
        raise RuntimeError(f"GetMessage {res}")
```

非阻塞式

```python
while True:
    res = windll.user32.PeekMessageA(byref(msg), None,0, 0, 1)
    if  res != 0:
        windll.user32.TranslateMessage(byref(msg))
        windll.user32.DispatchMessageA(byref(msg))
        if msg.message in[WM_QUIT]: 
            break
        else:
            time.sleep(0.05)
```



## 窗口消息处理

*当WebView/WebWindow绑定在父窗口下时,需要修改父窗口的消息处理函数,实现WebView/WebWindow子窗口的消息处理过程。*

wkeWin32的**HwndMsgAdapter**使用自身的消息处理流程替换指定父窗口的消息处理，接受外部注册的python函数处理指定的消息。

替换后对于已经注册的消息,使用注册函数来响应,如果函数返回None,则继续调用父窗口的默认消息处理流程,若不为None则不调用;对于没注册的消息则使用父窗口的默认消息处理流程。

注册的消息响应函数可以有1~5个参数,如下:

| Arg1    | Arg2   | Arg3   | Arg4   | Arg5   |
| ------- | ------ | ------ | ------ | ------ |
| webview | hwnd   | msg    | wParam | lParam |
| self    | hwnd   | msg    | wParam | lParam |
| hwnd    | msg    | wParam | lParam |        |
| hwnd    | wParam | lParam |        |        |
| wParam  | lParam |        |        |        |
| self    |        |        |        |        |
| hwnd    |        |        |        |        |

HwndMsgAdapter的消息处理流程调用注册的消息响应函数时:

- 参数hwnd/msg/wParam/lParam 使用父窗口的处理流程的句柄/消息/参数带入
- 有5个参数时第一个参数名为self或webview,self则对应HwndProcAdapter类实例带入,webview对应HwndProcAdapter类实例的webview属性带入
- 有1个参数时同上,参数名为其他时,以消息窗口句柄hwnd带入

Example:

```python
	x,y,w,h = 0,0,640,480
    hwnd = createWindow('Window',x,y,w,h)
    webview.build(hwnd,x,y,w,h)   

    a = HwndMsgAdapter()
    def wkeMsgProcQuit(webview,hwnd,msg,wParam,lParam):
        win32gui.PostQuitMessage(0)
        return 
    a.registerMsgProc(WM_SIZE,wkeMsgProcResize)
    a.registerMsgProc(WM_DESTROY,wkeMsgProcQuit)
    a.attach(hwnd,webview)
    webview.loadURL("http://192.168.1.1")
    ....
```



## 事件WkeEvent

*Wke关于webview的事件管理是基于WebView，一个WebView对象的打开/关闭/加载/绘制等一系列事件都会触发执行其事件响应函数。*

**WkeEvent以【webview的id】【事件名称的id】 为二元结构，管理事件响应函数及其上下文。**

### 注册事件处理函数onXXXX(webview,func,param) 

1. ​		接受XXX事件处理的网页对象webview
2. ​		XXX事件处理函数func
3. ​		注册前和调用后的贯穿参数param		

###  事件处理函数func(context,*args,**kwargs)

​		经WkeEvent的翻译，传递给事件响应函数的上下文context：

```python
context = {"id":eventid,"param":param,"func":func,"webview":webview,"id":webview.cId,"event":event}
```

​		不同的事件有特定的扩展参数，例如Paint事件

```python
OnPaintEvent(conext:dict,args=[hdc:int,x:int,y:int,cx:int,cy:int],kwargs=None)
```

Example:

```python
Wke.init()
webview = WebWindow()
webview.create(0,0,0,800,600)
def OnEvent(context,*args,**kwargs):
    param = context["param"]
	print('param',param,'args:',args,'kwargs:',kwargs)
	return 0
event = WkeEvent() #或者event = Wke.event
event.onURLChanged2(webview,OnEvent,'onURLChanged2')
webview.loadURLW('https://baidu.com')
webview.showWindow(True)
Wke.runMessageLoop()  
```

Webview绑定了一系列翻译方法，实现形如:

​		`webview.OnPaintEvent(param,*args,**kwargs）-> Wke.event.OnPaintEvent(webview,param,*args,**kwargs）`

unittest/testWebViewOnEvent.py检查WkeEvent所有事件是否在WebView都有对应的绑定实现，并生成所需要的实现翻译代码。

# Javascript 集成

WebView/WebWindows的runJsCode/runJsFile/runJsFunc方法支持Python端在网页对象中运行js代码。

# 插件支持

Miniblink supports NPAPI plugins.

# 离屏渲染

WebView.bind(父窗口hwnd,x,y,w,h)在一个已经创建的父窗口hwnd上绑定一个网页视图，然后额外的处理父窗口的消息，以及父窗口到网页视图的绘制。

参见wkeWin32ProcMsg中WebViewWithProcHwnd和example/bindWebview.py



# TODO

Wke/WebView的job/request有些地方未修订验证

