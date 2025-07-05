# 简介

PyWkeMiniblink： [项目地址](https://github.com/StoneFlaw/PyWkeMiniblink)  /  [在线文档](https://pywkeminiblink.readthedocs.io/zh-cn/latest/)  / [PYPI主页](https://pypi.org/project/WkeMiniblink/)


PyWkeMiniblink 是 [Miniblink](https://weolar.github.io/miniblink/)的Python绑定，参考源了上游项目[MBPython](https://github.com/lochen88/MBPython)。

Miniblink 是 chromium的精简版，删除了音视频功能,原接口参见[官方接口文档](https://miniblink.net/views/doc/index.html),更完整的参见docs/source/wke.h 。

# 使用

## 安装

```shell
#安装依赖pywin32
pip3 install pywin32
#安装本地文件xx版本
pip3 install WkeMiniblink-xx-py3-none-any.whl
#从PYPI安装
pip3 install WkeMiniblink
```

## 发布

### pyinstaller

(Pyinstaller>=6.0.0 )

- 在Pyinstaller打包 one dir（-D 目录模式）时，除可执行文件外，其余文件都将被转移到 _internal 文件夹

    以此为Package的根目录

- 在Pyinstaller打包 one file （-F 文件模式）时，除可执行文件外，其余文件都将被转移到一个临时文件夹

    以此为Package的根目录

- 在Python解释器模式下,以Lib\site-packages

    以此为Package的根目录



wkeMiniblink 搜索 解释器目录/Package的根目录，具体参见find_miniblink()



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
    hwnd = wkeCreateWindow('Window',x,y,w,h)
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

​		经WkeEvent的翻译，传递给事件响应函数的上下文context是个字典，如下：

```python
context = {"id":eventid,"param":param,"func":func,"webview":webview,"id":webview.cId,"event":event}
```

​		**其中param是注册回调函数绑定的任意python object对象，func是绑定的python回调函数**

​		不同的事件有特定的扩展参数，都写在kwargs中，例如Alert事件中通知消息就在kwargs["msg"]中

Example:

```python
#//python 事件响应函数void OnAlertEvent(context:dict,kwargs={msg:str}) 
#/*typedef void(WKE_CALL_TYPE*wkeAlertBoxCallback)(wkeWebView webView, void* param, const wkeString msg);*/
# OnAlertCallback回调函数执行时包含: kwargs["msg"]
def main():
	Wke.init()
    Wke.setCookieAndStagePath(cookie=f'{father_folder }/build/cookie.dat',localStage=f'{father_folder }/build/LocalStage')
    webview = WebWindow()
    webview.create(0,0,0,800,600)

    def OnAlertEvent(context,*args,**kwargs):
        param = context["param"]
        print(f"{str(param)} \nargs:{pformat(args)}\nkwargs:{pformat(kwargs)}\n=======================\n")
        msg = kwargs["msg"]
        windowTitle = ""
        result  = win32gui.MessageBox(0, msg, windowTitle, win32con.MB_OK)
        return  result

    def OnCloseEvent(context,*args,**kwargs):
        win32gui.PostQuitMessage(0)
        return True

    webview.onAlertBox(OnAlertEvent,param='Alert')
    webview.onWindowClosing(OnCloseEvent,param='App Quit')
    #webview.loadURL('https://www.w3school.com.cn/tiy/t.asp?f=jsck_alert_2')
    webview.loadFile(f'{father_folder}/res/testdata/alert.html')
    
    webview.showWindow(True)
    Wke.runMessageLoop()
```

Webview绑定了一系列事件回调函数注册方法，和使用全局Wke.event管理器注册等价:

```python
Wke.event.OnPaintEvent(webview,param,*args,**kwargs)
webview.OnPaintEvent(param,*args,**kwargs)
```

unittest/testWebViewOnEvent.py检查WkeEvent所有事件是否在WebView都有对应的绑定实现，并生成所需要的实现翻译代码。



## 其它WkeWin32

WkeWin32包含了Win32相关下面的辅助方法：

wkeSetIcon/wkeCreateWindow/wkeCreateTransparentWindow/wkeSetWindowLongHook/wkeGetWindowLongHook 等方法;

定时类WkeTimer/截屏类WkeSnapShot



# Javascript 集成

WebView/WebWindows的runJsCode/runJsFile/runJsFunc方法支持Python端在网页对象中运行js代码。

# 插件支持

Miniblink supports NPAPI plugins.

未验证

# 离屏渲染

WebView.bind(父窗口hwnd,x,y,w,h)在一个已经创建的父窗口hwnd上绑定一个网页视图，然后额外的处理父窗口的消息，以及父窗口到网页视图的绘制。

参见wkeWin32ProcMsg中WebViewWithProcHwnd和example/bindWebview.py

### Ctypes数据类型

参见prepare.py.translate()与wke.h.json



# 其他问题

### Alert/Prompt/Confirm

需要使用wkeEvent的回调函数额外实现相应的GUI及其返回值控制，参见examples.

## PromptBoxCallback的Py形参和返回值

正常情况下

```
typedef bool(WKE_CALL_TYPE*wkePromptBoxCallback)(wkeWebView webView, void* param, const wkeString msg, const wkeString defaultResult, wkeString result);
<<=>>
CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_char_p,c_void_p)
```

​      原回调函数返回值为c_bool,为保持形参形式一致,不做按引用传参数带出返回值,取消形参result,而是python的返回值。

​      实际python回调函数返回值为Str(有字符串确定输入)/None(取消输入)

## wkeGetString/wkeSetString/String/StingW

Miniblink文档中String对应utf8*而StringW对应utf16*

wkeEvent.py中32位下wkeGetStringW(str)运行正常,但是64位会c函数内部读异常

现在默认wkeString全部是utf8，改为wkeGetString(str),然后做binary->str的解码

### wkeString的Ctypes参数类型

将只读wkeString 全翻译为c_char_p,方便ctypes自动转换字符串。

如果需要写入wkeString,就翻译为c_void_p (c_char_p自动翻译为None)

```
#wkeString:c_void_p,text:str
utf8 = text.encode(encoding)
l = len(utf8)
mb.wkeSetString(cast(wkeString,c_char_p),utf8,l)
```

wkePromptBoxCallback的最后一个参数为wkeString,需要作为传参返回,填入字符串。所以wkeString翻成c_void_p





# TODO

Wke/WebView的job/request有些地方未修订验证


# [Contact Us](mailto://wyh917@163.com)

