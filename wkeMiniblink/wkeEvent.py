# -*- coding:utf-8 -*-


import sys
import binascii
import json
from inspect import getmembers



from ctypes import (c_void_p,
    c_int,
    c_ushort,c_longlong,
    c_wchar_p,
    c_float,
    c_ulonglong,
    byref,
    cast,
    CFUNCTYPE
)


from . import _LRESULT,WkeCallbackError,GetMiniblinkDLL

from . import *
from .wkeStruct import *
from .miniblink import *

class WkeEvent():
    """Wke关于webview的事件管理

    事件注册:   onXXXX(webview,func,param)

    卸载    :   offXXX(webview,func)

    事件回调:   func(webview,param,*args,**kwargs)

    Example:
        .. code:: python

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
    """
  
    def __init__(self,dll=None):
        """WkeEvent构造函数

        """
    
        self.context ={}
        self.eventEntries = {}
        #创建所有onXXX对应的注销函数ofXXX
        
        for name,func in getmembers(self):
            if name.startswith("on"):
                suf = name[2:]
                self.eventEntries[name] = func
                #offname = f"off{suf}"
                #setattr(self,offname,lambda pwebview: self._off(pwebview,name))
          
        return


    
    def __del__(self):
        return

    def _on(self,pwebview,event,func,param,*args,**kwargs):
        """为pwebiew(pyobject)创建func对应的上下文

        Args:
            pwebview(WebView):      webview对象(py对象) 
            event(str):             事件名称
            func(function):         事件回调函数(py函数)  
            param(obj, optional):   回调上下文参数(py对象)-> void * param (c指针),默认为None(NULL) 
            args(list, optional):   具体回调函数需要的额外参数
   
        Return:
            id(int):                事件ID

        """ 

        eventid = id(event)
        webviewid = pwebview.cId

        if webviewid not in self.context:
            self.context[webviewid]={}
       
        self.context[webviewid][eventid]={"id":eventid,"param":param,"func":func,"webview":pwebview,"id":pwebview.cId,"event":event}
        return eventid
    
    def _off(self,pwebview,event):
        eventid = id(event)
        webviewid = pwebview.cId
        if webviewid in self.context :
            if eventid in self.context[webviewid]:
                self.context[webviewid].pop(eventid)
        self.context.pop(webviewid)            

        return 

    def offWebViewAllEvent(self,pwebview):
        """注销所有webview的事件回调函数(仅py端)

        Args:
            pwebview(WebView):   webview对象(py对象) 

        """ 
        webviewid = pwebview.cId
        if webviewid in self.context :
            self.context[webviewid].clear()
            self.context.pop(webviewid)            
        return 
    
    def _callback(self,cwebview,param,*args,**kwargs):
        """
        依据cwebiew(webview 句柄),param(id(webview)) 回调注册的响应py函数

        Args:
            cwebview(int,webView id):       webview 句柄(c) 
            func(function):                 通知回调python函数,事件发生时C回调函数调用该py函数
            param(any, optional):           回调上下文参数,默认为None 
                  
        Return:
            ret(any) :                      回调python函数的返回值

        """ 
        eventid = param
        webviewid = cwebview
        if webviewid in self.context :
            if eventid in self.context[webviewid]:
                context = self.context[webviewid][eventid]
                return context["func"](context,*args,**kwargs)
        raise WkeCallbackError(f"No such callback! {param}")

    def onDocumentReady2(self,pwebview,func,param = None):
        """设置文档就绪时的函数

        对应js里的body onload事件

        回调函数执行时包含: kwargs["frameId"]
        
        .. code:: c

            //python 事件响应函数(context:dict,kwargs={frameId:int})         
            /*typedef void(WKE_CALL_TYPE*wkeDocumentReady2Callback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
    
        """
        eventid = self._on(pwebview,'onDocumentReady2',func,param)
        return   wkeOnDocumentReady2(pwebview.cId,self._wkeDocumentReady2Callback,eventid)

    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p))
    def _wkeDocumentReady2Callback(self,cwebview,param,frameId):
        return self._callback(cwebview,param,frameId=frameId)

    
    
    def onCreateView(self,pwebview,func,param = None):    
        """设置创建新窗口时的回调

        网页点击a标签创建新窗口时将触发回调

        回调函数执行时包含:kwargs["navigationType"],kwargs["url"],kwargs["windowFeatures"]

        .. code:: c

            //python 事件响应函数 int (context:dict,kwargs=[navigationType:wkeNavigationType,url:str,windowFeatures:wkeWindowFeatures])
            /*typedef wkeWebView(WKE_CALL_TYPE*wkeCreateViewCallback)(wkeWebView webView, void* param, wkeNavigationType navigationType, const wkeString url, const wkeWindowFeatures* windowFeatures);*/
            
        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None

        """   

        eventid = self._on(pwebview,func,param)
        return   wkeOnCreateView(pwebview.cId,self._wkeCreateViewCallback,eventid)

    @WkeMethod(CFUNCTYPE(_LRESULT,_LRESULT,c_void_p,c_int,c_char_p,POINTER(wkeWindowFeatures)))
    def _wkeCreateViewCallback(self,cwebview,param,navigationType,url,windowFeatures):
        url=pyWkeGetString(url)
        return self._callback(cwebview,param,navigationType=navigationType,url=url,windowFeatures=windowFeatures)

    
    def onURLChanged2(self,pwebview,func,param = None):    
        """设置标题变化的回调

        回调函数执行时包含: kwargs["frameId"],kwargs["url"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={frameId:int,url:str})
            /*typedef void(WKE_CALL_TYPE*wkeURLChangedCallback2)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, const wkeString url);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        
        """   
        eventid = self._on(pwebview,'onURLChanged2',func,param)
        return wkeOnURLChanged2(pwebview.cId,self._wkeURLChangedCallback2,eventid)

    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,c_char_p))
    def _wkeURLChangedCallback2(self,cwebview,param,frameId,url):
        url=pyWkeGetString(url)
        return self._callback(cwebview,param,frameId=frameId,url=url)

    
    def onWindowClosing(self,pwebview,func,param = None):
        """ 设置窗口关闭时回调  

        webview如果是真窗口模式，则在收到WM_CLODE消息时触发此回调。可以通过在回调中返回false拒绝关闭窗口 

        回调函数执行时返回false拒绝关闭窗口,返回true接受关闭

        .. code:: c

            //python 事件响应函数(context:dict,kwargs=None)
            /*typedef bool(WKE_CALL_TYPE*wkeWindowClosingCallback)(wkeWebView webWindow, void* param);*/ 
        
        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onWindowClosing',func,param)
        return wkeOnWindowClosing(pwebview.cId,self._wkeWindowClosingCallback,eventid)

    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,c_void_p))
    def _wkeWindowClosingCallback(self,cwebview, param):
        return self._callback(cwebview,param)
    

    def onWindowDestroy(self,pwebview,func,param = None):
        """ 设置窗口销毁时回调

        不像wkeOnWindowClosing，这个操作无法取消

        .. code:: c

            //python 事件响应函数(context:dict,kwargs=None)
            /*typedef void(WKE_CALL_TYPE*wkeWindowDestroyCallback)(wkeWebView webWindow, void* param);*/
            
        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onWindowDestroy',func,param)
        return wkeOnWindowDestroy(pwebview.cId,self._wkeWindowDestroyCallback,eventid)

    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p) )
    def _wkeWindowDestroyCallback(self,cwebview, param):
        return self._callback(cwebview,param)
    
    
    def onPaintUpdated(self,pwebview,func,param = None):
        """ 设置窗口绘制刷新时回调

        页面有任何需要刷新的地方，将调用此回调

        回调函数执行时包含: kwargs["hdc"],kwargs["x"],kwargs["y"],kwargs["cx"],kwargs["cy"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={hdc:_LRESULT,x:int,y:int,cx:int,cy:int})
            /*typedef void(WKE_CALL_TYPE*wkePaintUpdatedCallback)(wkeWebView webView, void* param, const HDC hdc, int x, int y, int cx, int cy);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onPaintUpdated',func,param)
        return wkeOnPaintUpdated(pwebview.cId,self._wkePaintUpdatedCallback ,eventid)
    
    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,_LRESULT,c_int,c_int,c_int,c_int))
    def _wkePaintUpdatedCallback(self,cwebview,param,hdc,x,y,cx,cy):
        #HDC=long
        return self._callback(cwebview,param=param,hdc=hdc,x=x,y=y,cx=cx,cy=cy)

    
    def onPaintBitUpdated(self,pwebview,func,param = None):
        """ 设置窗口绘制刷新时回调 

        不同onPaintUpdated的是回调过来的是填充好像素的buffer,而不是DC。方便嵌入到游戏中做离屏渲染

        回调函数执行时包含: kwargs["buf"],kwargs["rect"],kwargs["width"],kwargs["height"]

        .. code:: c
        
            //python 事件响应函数(context:dict,kwargs={buf:c_char_p,rect:struct,cx:int,cy:int}) 
            /*typedef void(WKE_CALL_TYPE*wkePaintBitUpdatedCallback)(wkeWebView webView, void* param, const void* buffer, const wkeRect* r, int width, int height);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None

        """   

        eventid = self._on(pwebview,'onPaintBitUpdated',func,param)
        return wkeOnPaintBitUpdated(pwebview.cId, self._wkePaintBitUpdatedCallback,eventid)
    
    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_void_p,POINTER(wkeRect),c_int,c_int))
    def _wkePaintBitUpdatedCallback(self,cwebview,param,buf,rect,width,height):
        return self._callback(cwebview,param=param,buf=buf,rect=rect,width=width,height=height)

    
    def onNavigation(self,pwebview,func,param = None):
        """设置网页开始浏览的回调

        回调函数执行时包含: kwargs["navigationType"],kwargs["url"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={navigationType:wkeNavigationType,url:str}) 
            /*typedef bool(WKE_CALL_TYPE*wkeNavigationCallback)(wkeWebView webView, void* param, wkeNavigationType navigationType, wkeString url);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None

        NOTE:

            wkeNavigationCallback回调的返回值，如果是true，表示可以继续进行浏览，false表示阻止本次浏览。

            wkeNavigationType: 表示浏览触发的原因。可以取的值有：

            ==================================      ==================================
            WKE_NAVIGATION_TYPE_LINKCLICK           点击a标签触发
            WKE_NAVIGATION_TYPE_FORMSUBMITTE        点击form触发
            WKE_NAVIGATION_TYPE_BACKFORWARD         前进后退触发
            WKE_NAVIGATION_TYPE_RELOAD              重新加载触发
            WKE_NAVIGATION_TYPE_FORMRESUBMITT       表单提交触发
            ==================================      ==================================
        """   
        eventid = self._on(pwebview,'onNavigation',func,param)   
        return wkeOnNavigation(pwebview.cId,self._wkeNavigationCallback,eventid)
    
    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_int,c_char_p))
    def _wkeNavigationCallback(self,cwebview,param,navigationType,url):
        url=pyWkeGetString(url)
        return self._callback(cwebview,param=param,navigationType=navigationType,url=url)
    
    
    def onTitleChanged(self,pwebview,func,param = None):
        """设置标题变化的回调

        回调函数执行时包含: kwargs["title"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={title:str}) 
            /*typedef void(WKE_CALL_TYPE*wkeTitleChangedCallback)(wkeWebView webView, void* param, const wkeString title);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
    
        eventid = self._on(pwebview,'onTitleChanged',func,param)       
        return wkeOnTitleChanged(pwebview.cId,self._wkeTitleChangedCallback,eventid)
    
    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p))
    def _wkeTitleChangedCallback(self,cwebview, param, title):
        title=pyWkeGetString(title)
        return self._callback(cwebview, param=param, title=title)
        

    def onMouseOverUrlChanged(self,pwebview,func,param = None):
        """设置鼠标划过链接元素的回调

        鼠标划过的元素，如果是链接，则调用此回调，并发送a标签的url的通知回调

        回调函数执行时包含: kwargs["url"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={url:str}) 
            /*typedef void(WKE_CALL_TYPE*wkeTitleChangedCallback)(wkeWebView webView, void* param, const wkeString title);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onMouseOverUrlChanged',func,param)       
        return wkeOnMouseOverUrlChanged(pwebview.cId,self._wkeMouseOverUrlChangedCallback,eventid)
    
    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p))
    def _wkeMouseOverUrlChangedCallback(self,cwebview, param, url):
        url=pyWkeGetString(url)
        return self._callback(cwebview, param=param, url=url)
        

    def onAlertBox(self,pwebview,func,param = None):
        """设置网页调用alert的回调

        回调函数执行时包含: kwargs["msg"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={msg:str}) 
            /*typedef void(WKE_CALL_TYPE*wkeAlertBoxCallback)(wkeWebView webView, void* param, const wkeString msg);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """  
        eventid = self._on(pwebview,'onAlertBox',func,param)           
        return wkeOnAlertBox(pwebview.cId,self._wkeAlertBoxCallback,eventid)
       
    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p))
    def _wkeAlertBoxCallback(self,cwebview,param,msg):
        msg=pyWkeGetString(msg)
        return self._callback(cwebview, param=param, msg=msg)
        
        
    def onConfirmBox(self,pwebview,func,param = None):
        """设置网页调用confirmBox的回调

        回调函数执行时包含: kwargs["msg"]

        NOTE：       
            回调函数执行返回值true/false表示是否接受。但对应关系文档没说。

            实际运行不会弹出Confirm框,需要回调函数自己实现GUI。回调函数返回值返回true就是点击了确认，返回False就是点击了取消

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={msg:str}) 
            /*typedef bool(WKE_CALL_TYPE*wkeConfirmBoxCallback)(wkeWebView webView, void* param, const wkeString msg);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """  
        eventid = self._on(pwebview,'onConfirmBox',func,param)           
        return wkeOnConfirmBox(pwebview.cId,self._wkeConfirmBoxCallback,eventid)
        
    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p))
    def _wkeConfirmBoxCallback(self,cwebview,param,msg):
        msg=pyWkeGetString(msg)
        return self._callback(cwebview, param=param, msg=msg)


    def onPromptBox(self,pwebview,func,param = None):
        """设置网页调用PromptBox的回调

        回调函数执行时包含: kwargs["msg"],kwargs["defaultResult"]

        NOTE：       
            回调函数执行返回值true/false表示是否接受。但对应关系文档没说。

            实际运行不会弹出Prompt框,需要回调函数自己实现GUI。C语言回调函数返回值返回true就是点击了确认，返回False就是点击了取消。

            原回调函数返回值为c_bool,为保持形参形式一致,不做按引用传参数带出返回值,取消形参result,而是python的返回值。
            
            实际python回调函数返回值为Str(有字符串确定输入)/None(取消输入)

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={msg:str,defaultResult:str}) 
            /*typedef bool(WKE_CALL_TYPE*wkePromptBoxCallback)(wkeWebView webView, void* param, const wkeString msg, const wkeString defaultResult, wkeString result);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """
        eventid = self._on(pwebview,'onPromptBox',func,param)       
        return wkeOnPromptBox(pwebview.cId,self._wkePromptBoxCallback,eventid)

    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_char_p,c_void_p))
    def _wkePromptBoxCallback(self,cwebview,param,msg,defaultResult,wkeResult):
        msg=pyWkeGetString(msg)
        defaultResult=pyWkeGetString(defaultResult)

        result = self._callback(cwebview, param=param, msg=msg,defaultResult=defaultResult,result = "")
        if result :
            pyWkeSetString(cast(wkeResult,c_char_p),result)
            return True

        return False

    def onConsole(self,pwebview,func,param = None):
        """设置网页调用console触发的回调

        回调函数执行时包含: kwargs["level"],kwargs["msg"],kwargs["sourceName"],kwargs["sourceLine"],kwargs["stackTrace"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={level:str,msg:str,sourceName:str,sourceLine:int,stackTrace:str}) 
            /*typedef void(WKE_CALL_TYPE*wkeConsoleCallback)(wkeWebView webView, void* param, wkeConsoleLevel level, const wkeString message, const wkeString sourceName, unsigned sourceLine, const wkeString stackTrace);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """
        eventid = self._on(pwebview,'onConsole',func,param)       
        return wkeOnConsole(pwebview.cId,self._wkeConsoleCallback,eventid)

    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_uint,c_char_p,c_char_p,c_int,c_char_p))
    def _wkeConsoleCallback(self,cwebview,param,level,msg,sourceName,sourceLine,stackTrace):
        msg= pyWkeGetString(msg)
        sourceName=pyWkeGetString(sourceName)
        stackTrace=pyWkeGetString(stackTrace)
        return self._callback(cwebview, param=param,level=level,msg=msg,sourceName=sourceName,sourceLine=sourceLine,stackTrace=stackTrace)
    

    def onDownload(self,pwebview,func,param = None):
        """设置网页开始下载的回调

        回调函数执行时包含: kwargs["url"]

        NOTE：
            回调函数执行时返回值true/false表示是否接受。但对应关系文档没说。

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={url:str}) 
            /*typedef bool(WKE_CALL_TYPE*wkeDownloadCallback)(wkeWebView webView, void* param, const char* url);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onDownload',func,param)         
        return wkeOnDownload(pwebview.cId,self._wkeDownloadCallback,eventid)
        
    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p))
    def _wkeDownloadCallback(self,cwebview,param,url):
        url=pyWkeGetString(url)
        return self._callback(cwebview, param=param, url=url)


    def onNetResponse(self,pwebview,func,param = None):
        """设置收到网络应答的回调

        一个网络请求发送后，收到服务器response触发回调

        回调函数执行时包含: kwargs["url"],kwargs["job"]

        NOTE：
            回调函数执行时返回值true/false表示是否接受网络应答。但对应关系文档没说。
        
        .. code:: c

            //python 事件响应函数(context:dict,kwargs={url:str,job:c_void_p})  
            /*typedef bool(WKE_CALL_TYPE*wkeNetResponseCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None 

        TODO:
            JOB 参数未C翻译到Py      
        """
        eventid = self._on(pwebview,'onNetResponse',func,param)   
        return wkeNetOnResponse(pwebview.cId,self._wkeNetResponseCallback,eventid)   

    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p))
    def _wkeNetResponseCallback(self,cwebview,param,url,job):
        url=url
        return self._callback(cwebview, param=param, url=url,job=job)


    def onLoadUrlBegin(self,pwebview,func,param = None):
        """设置网络请求发起前的回调
        
        任何网络请求发起前会触发此回调

        回调函数执行时包含: kwargs["url"],kwargs["job"]

        回调函数执行时返回值true/false表示是否处理此网络请求。如果wkeLoadUrlBeginCallback回调里返回true，表示mb不处理此网络请求（既不会发送网络请求）。返回false，表示mb依然会发送网络请求。

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={url:str,job:c_void_p})  
            /*typedef bool(WKE_CALL_TYPE*wkeLoadUrlBeginCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None    

        NOTE：
            1. 此回调功能强大，在回调里，如果对job设置了wkeNetHookRequest，则表示mb会缓存获取到的网络数据，并在这次网络请求 结束后调用wkeOnLoadUrlEnd设置的回调，同时传递缓存的数据。在此期间，mb不会处理网络数据。
            2. 如果在wkeLoadUrlBeginCallback里没设置wkeNetHookRequest，则不会触发wkeOnLoadUrlEnd回调。
            3. 如果wkeLoadUrlBeginCallback回调里返回true，表示mb不处理此网络请求（既不会发送网络请求）。返回false，表示mb依然会发送网络请求。

        """
        eventid = self._on(pwebview,'onLoadUrlBegin',func,param)   
        return wkeOnLoadUrlBegin(pwebview.cId,self._wkeLoadUrlBeginCallback,eventid)

    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p))
    def _wkeLoadUrlBeginCallback(self,cwebview,param,url,job):
        url=url
        return self._callback(cwebview, param=param,url=url,job=job)


    def onLoadUrlEnd(self,pwebview,func,param = None):
        """设置网络请求结束的回调

            如果在wkeLoadUrlBeginCallback里没设置wkeNetHookRequest，则不会触发wkeOnLoadUrlEnd回调。

            回调函数执行时包含: kwargs["url"],kwargs["job"],kwargs["buf"],kwargs["len"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={url:str,job:c_void_p,buf:c_char_p,len:int})  
            /*typedef void(WKE_CALL_TYPE*wkeLoadUrlEndCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job, void* buf, int len);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None    

        TODO:
            job未翻译
        """
        eventid = self._on(pwebview,'onLoadUrllEnd',func,param)   
        return wkeOnLoadUrlEnd(pwebview.cId,self._wkeLoadUrlEndCallback,eventid)

    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_void_p,c_int))
    def _wkeLoadUrlEndCallback(self,cwebview,param,url,job,buf,len):
        url=url
        return self._callback(cwebview, param=param,url=url,job=job,buf=buf,len=len)


    def onLoadUrlFail(self,pwebview,func,param = None):
        """设置网络请求失败的回调
        
        回调函数执行时包含: kwargs["url"],kwargs["job"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={url:str,job:c_void_p})  
            /*typedef void(WKE_CALL_TYPE*wkeLoadUrlFailCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None    

        TODO:
            job未翻译
        """
        eventid = self._on(pwebview,'onLoadUrllFail',func,param)   
        return wkeOnLoadUrlFail(pwebview.cId,self._wkeLoadUrlFailCallback,eventid)

    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p))
    def _wkeLoadUrlFailCallback(self,cwebview,param,url,job):
        return self._callback(cwebview, param=param,url=url,job=job)
    

    def onLoadUrlFinish(self,pwebview,func,param = None):
        """设置网络请求完成的回调

            回调函数执行时包含: kwargs["url"],kwargs["result"],kwargs["failedReason"]

        .. code:: c

            //python 事件响应函数(context:dict,kwargs={url:str,result:int,failedReason:str})  
            /*typedef void(WKE_CALL_TYPE*wkeLoadUrlFinishCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job, int len);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None    
        """
        eventid = self._on(pwebview,'onLoadUrlFinish',func,param)   
        return wkeOnLoadUrlFinish(pwebview.cId,self._wkeLoadUrlFinishCallback,eventid)

    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,c_void_p,c_int))
    def _wkeLoadUrlFinishCallback(self,cwebview,param,url,result,failedReason):
        url=pyWkeGetString(url)
        if result==1:
            failedReason=pyWkeGetString(failedReason)            
        return self._callback(cwebview, param=param,url=url,result=result,failedReason=failedReason)
    

    def onGetFavicon(self,pwebview,func,param = None):
        """设置获取favicon的回调

            回调函数执行时包含: kwargs["url"],kwargs["buf"]

        NOTE:
            此接口必须在wkeOnLoadingFinish回调里调用。可以用下面方式来判断是否是主frame的LoadingFinish:
            
            .. code:: python

            	tempInfo = webview.getTempCallbackInfo()
			    if (webview.isMainFrame(temInfo.frame)) :
			        webview.wkeNetGetFavicon(HandleFaviconReceived, divaram);
			    
        .. code:: c

            //python 事件响应函数(context:dict,kwargs={url:str,buf:wkeMemBuf *})  
            /*typedef void(WKE_CALL_TYPE*wkeOnNetGetFaviconCallback)(wkeWebView webView, void* param, const utf8* url, wkeMemBuf* buf);*/

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None    
        """
        eventid = self._on(pwebview,'onGetFavicon',func,param)   
        return wkeNetGetFavicon(pwebview.cId,self._wkeOnNetGetFaviconCallback,eventid) 
    
    @WkeMethod(CFUNCTYPE(None,_LRESULT,c_void_p,c_char_p,POINTER(wkeMemBuf)))
    def _wkeOnNetGetFaviconCallback(self,cwebview,param,url,buf): 
        url=pyWkeGetString(url)
        return self._callback(cwebview, param=param,url=url,buf=buf)

  