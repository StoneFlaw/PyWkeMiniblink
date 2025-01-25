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
    CFUNCTYPE
)


from . import _LRESULT,WkeCallbackError,GetMiniblinkDLL


from .wkeStruct import *
from .miniblink import MiniblinkInit

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
        if dll is None:
            self.dll = GetMiniblinkDLL()
        else:
            self.dll = dll
            
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
            pwebview(WebView):   webview对象(py) 
            event(str): 事件名称
            func(function): 事件回调函数(py)  
            param(obj, optional):      文档加载回调上下文参数
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
            pwebview(WebView):   webview对象(py) 

        """ 
        webviewid = pwebview.cId
        if webviewid in self.context :
            self.context[webviewid].clear()
            self.context.pop(webviewid)            
        return 
    
    def _callback(self,cwebview,param,*args,**kwargs):
        """
        依据cwebiew(c),param(id(webview)) 回调注册的响应py函数
        """ 
        eventid = param
        webviewid = cwebview
        if webviewid in self.context :
            if eventid in self.context[webviewid]:
                context = self.context[webviewid][eventid]
                return context["func"](context,*args,**kwargs)
        raise WkeCallbackError(f"No such callback! {param}")

    def entries(self):    
        return self.eventEntries

    def onDocumentReady2(self,pwebview,func,param = None):
        """设置文档就绪时的函数

        对应js里的body onload事件
        
        .. code:: c

            //python 事件响应函数(conext:dict,args=[frameId:int],kwargs=None)         
            typedef void(WKE_CALL_TYPE*wkeDocumentReady2Callback)(wkeWebView webView, void* param, wkeWebFrameHandle frameId); //C原型 

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None

        """
        eventid = self._on(pwebview,'onDocumentReady2',func,param)
        return   self.dll.wkeOnDocumentReady2(pwebview.cId,self._wkeDocumentReady2Callback,eventid)

    @WkeMethod(CFUNCTYPE(None,_LRESULT,_LRESULT,c_int))
    def _wkeDocumentReady2Callback(self,cwebview,param,frameId):
        return self._callback(cwebview,param,frameId)

    
    
    def onCreateView(self,pwebview,func,param = None):    
        """设置创建新窗口时的回调

        网页点击a标签创建新窗口时将触发回调

        .. code:: c

            //python 事件响应函数 int (conext:dict,args=[navigationType:int,url:str,windowFeatures:struct*],kwargs=None)
            typedef wkeWebView(WKE_CALL_TYPE*wkeCreateViewCallback)(wkeWebView webView, void* param, wkeNavigationType navigationType, const wkeString url, const wkeWindowFeatures* windowFeatures); //C原型  
            
        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None

        TODO:
            windowFeatures 未翻译c到py

        """   

        eventid = self._on(pwebview,func,param)
        return   self.dll.wkeOnCreateView(pwebview.cId,self._wkeCreateViewCallback,eventid)

    @WkeMethod(CFUNCTYPE(c_int,_LRESULT, _LRESULT,c_int,c_void_p,POINTER(wkeWindowFeatures)))
    def _wkeCreateViewCallback(self,cwebview,param,navigationType,url,windowFeatures):
        url=self.dll.wkeGetStringW(url)
        return self._callback(cwebview,param,navigationType=navigationType,url=url,windowFeatures=windowFeatures)

    
    def onURLChanged2(self,pwebview,func,param = None):    
        """设置标题变化的回调

        .. code:: c

            //python 事件响应函数(conext:dict,args=[frameId:int,url:str],kwargs=None)
            typedef void(WKE_CALL_TYPE*wkeURLChangedCallback2)(wkeWebView webView, void* param, wkeWebFrameHandle frameId, const wkeString url);//C原型  

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onURLChanged2',func,param)
        return self.dll.wkeOnURLChanged2(pwebview.cId,self._wkeURLChangedCallback2,eventid)

    @WkeMethod(CFUNCTYPE(None, _LRESULT, _LRESULT,c_int,c_void_p))
    def _wkeURLChangedCallback2(self,cwebview,param,frameId,url):
        url=self.dll.wkeGetStringW(url)
        return self._callback(cwebview,param,frameId=frameId,url=url)

    
    def onWindowClosing(self,pwebview,func,param = None):
        """ 设置窗口关闭时回调  

        webview如果是真窗口模式，则在收到WM_CLODE消息时触发此回调。可以通过在回调中返回false拒绝关闭窗口 

        .. code:: c

            //python 事件响应函数(conext:dict,args=[],kwargs=None)
            typedef bool(WKE_CALL_TYPE*wkeWindowClosingCallback)(wkeWebView webWindow, void* param);//C原型  
        
        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onWindowClosing',func,param)
        return self.dll.wkeOnWindowClosing(pwebview.cId,self._wkeWindowClosingCallback,eventid)

    @WkeMethod(CFUNCTYPE(c_bool, _LRESULT, _LRESULT))
    def _wkeWindowClosingCallback(self,cwebview, param):
        return self._callback(cwebview,param)
    

    def onWindowDestroy(self,pwebview,func,param = None):
        """ 设置窗口销毁时回调

        不像wkeOnWindowClosing，这个操作无法取消

        .. code:: c

            //python 事件响应函数(conext:dict,args=[],kwargs=None)
            typedef void(WKE_CALL_TYPE*wkeWindowDestroyCallback)(wkeWebView webWindow, void* param);//C原型
            
        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onWindowDestroy',func,param)
        return self.dll.wkeOnWindowDestroy(pwebview.cId,self._wkeWindowDestroyCallback,eventid)

    @WkeMethod(CFUNCTYPE(None, _LRESULT, _LRESULT))
    def _wkeWindowDestroyCallback(self,cwebview, param):
        return self._callback(cwebview,param)
    
    
    def onPaintUpdated(self,pwebview,func,param = None):
        """ 设置窗口绘制刷新时回调

        页面有任何需要刷新的地方，将调用此回调

        .. code:: c

            //python 事件响应函数(conext:dict,args=[hdc:int,x:int,y:int,cx:int,cy:int],kwargs=None)
            typedef void(*wkePaintUpdatedCallback)(wkeWebView webView, void* param, const HDC hdc, int x, int y, int cx, int cy);//C原型

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onPaintUpdated',func,param)
        return self.dll.wkeOnPaintUpdated(pwebview.cId,self._wkePaintUpdatedCallback ,eventid)
    
    @WkeMethod(CFUNCTYPE(None,_LRESULT,_LRESULT,_LRESULT,c_int,c_int,c_int,c_int))
    def _wkePaintUpdatedCallback(self,cwebview,param,hdc,x,y,cx,cy):
        #HDC=long
        return self._callback(cwebview,param=param,hdc=hdc,x=x,y=y,cx=cx,cy=cy)

    
    def onPaintBitUpdated(self,pwebview,func,param = None):
        """ 设置窗口绘制刷新时回调 

        不同onPaintUpdated的是回调过来的是填充好像素的buffer，而不是DC。方便嵌入到游戏中做离屏渲染

        .. code:: c
        
            //python 事件响应函数(conext:dict,args=[buf:c_char_p,rect:struct,cx:int,cy:int],kwargs=None) 
            typedef void(WKE_CALL_TYPE*wkePaintBitUpdatedCallback)(wkeWebView webView, void* param, const void* buffer, const wkeRect* r, int width, int height);//C原型

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None

        TODO:
            rect
        """   

        eventid = self._on(pwebview,'onPaintBitUpdated',func,param)
        return self.dll.wkeOnPaintBitUpdated(pwebview.cId, self._wkePaintBitUpdatedCallback,eventid)
    
    @WkeMethod(CFUNCTYPE(None,_LRESULT,_LRESULT,c_void_p,POINTER(wkeRect),c_int,c_int))
    def _wkePaintBitUpdatedCallback(self,cwebview,param,buf,rect,width,height):
        return self._callback(cwebview,param=param,buf=buf,rect=rect,width=width,height=height)

    
    def onNavigation(self,pwebview,func,param = None):
        """设置网页开始浏览的回调
       
        .. code:: c

            //python 事件响应函数(conext:dict,args=[navigationType:wkeNavigationType],kwargs=None) 
            typedef bool(*wkeNavigationCallback)(wkeWebView webView, void* param, wkeNavigationType navigationType, const wkeString url);//C原型

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
        return self.dll.wkeOnNavigation(pwebview.cId,self._wkeNavigationCallback,eventid)
    
    @WkeMethod(CFUNCTYPE(c_bool, _LRESULT, _LRESULT,c_int,c_void_p))
    def _wkeNavigationCallback(self,cwebview,param,navigationType,url):
        url=self.dll.wkeGetStringW(url)
        return self._callback(cwebview,param=param,navigationType=navigationType,url=url)
    
    
    def onTitleChanged(self,pwebview,func,param = None):
        """设置标题变化的回调

        .. code:: c

            //python 事件响应函数(conext:dict,args=[title:str],kwargs=None) 
            typedef void(*wkeTitleChangedCallback)(wkeWebView webView, void* param, const wkeString title);//C原型

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
    
        eventid = self._on(pwebview,'onTitleChanged',func,param)       
        return self.dll.wkeOnTitleChanged(pwebview.cId,self._wkeTitleChangedCallback,eventid)
    
    @WkeMethod(CFUNCTYPE(None, _LRESULT, _LRESULT,c_void_p))
    def _wkeTitleChangedCallback(self,cwebview, param, title):
        title=self.dll.wkeGetStringW(title)
        return self._callback(cwebview, param=param, title=title)
        

    def onMouseOverUrlChanged(self,pwebview,func,param = None):
        """设置鼠标划过链接元素的回调

        鼠标划过的元素，如果是链接，则调用此回调，并发送a标签的url的通知回调
 
        .. code:: c

            //python 事件响应函数(conext:dict,args=[url:str],kwargs=None) 
            typedef void(*wkeMouseOverUrlChangedCallback)(wkeWebView webView, void* param, const wkeString url);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onMouseOverUrlChanged',func,param)       
        return self.dll.wkeOnMouseOverUrlChanged(pwebview.cId,self._wkeMouseOverUrlChangedCallback,eventid)
    
    @WkeMethod(CFUNCTYPE(None, _LRESULT, _LRESULT,c_void_p))
    def _wkeMouseOverUrlChangedCallback(self,cwebview, param, url):
        url=self.dll.wkeGetStringW(url)
        return self._callback(cwebview, param=param, url=url)
        

    def onAlertBox(self,pwebview,func,param = None):
        """设置网页调用alert的回调

        .. code:: c

            //python 事件响应函数(conext:dict,args=[msg:str],kwargs=None) 
            typedef void(*wkeAlertBoxCallback)(wkeWebView webView, void* param, const wkeString msg);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """  
        eventid = self._on(pwebview,'onAlertBox',func,param)           
        return self.dll.wkeOnAlertBox(pwebview.cId,self._wkeAlertBoxCallback,eventid)
       
    @WkeMethod(CFUNCTYPE(None, _LRESULT, _LRESULT,c_void_p))
    def _wkeAlertBoxCallback(self,cwebview,param,msg):
        msg=self.dll.wkeGetStringW(msg)
        return self._callback(cwebview, param=param, msg=msg)
        
        
    def onConfirmBox(self,pwebview,func,param = None):
        """设置网页调用confirmBox的回调

        .. code:: c

            //python 事件响应函数(conext:dict,args=[msg:str],kwargs=None) 
            typedef void(*wkeConfirmBoxCallback)(wkeWebView webView, void* param, const wkeString msg);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """  
        eventid = self._on(pwebview,'onConfirmBox',func,param)           
        return self.dll.wkeOnConfirmBox(pwebview.cId,self._wkeConfirmBoxCallback,eventid)
        
    @WkeMethod(CFUNCTYPE(None, _LRESULT, _LRESULT,c_void_p))
    def _wkeConfirmBoxCallback(self,cwebview,param,msg):
        msg=self.dll.wkeGetStringW(msg)
        return self._callback(cwebview, param=param, msg=msg)


    def onPromptBox(self,pwebview,func,param = None):
        """设置网页调用PromptBox的回调

        .. code:: c

            //python 事件响应函数(conext:dict,args=[msg:str,defaultResult:str,result:c_char_p],kwargs=None) 
            typedef void(*wkePromptBoxCallback)(wkeWebView webView, void* param, const wkeString msg,wkeString defaultResult,wkeString result);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """
        eventid = self._on(pwebview,'onPromptBox',func,param)       
        return self.dll.wkeOnPromptBox(pwebview.cId,self._wkePromptBoxCallback,eventid)

    @WkeMethod(CFUNCTYPE(None, _LRESULT, _LRESULT,c_void_p,c_void_p,c_char_p))
    def _wkePromptBoxCallback(self,cwebview,param,msg,defaultResult,result):
        msg=self.dll.wkeGetStringW(msg)
        defaultResult=self.dll.wkeGetStringW(defaultResult)
        return self._callback(cwebview, param=param, msg=msg,defaultResult=defaultResult,result=result)


    def onConsole(self,pwebview,func,param = None):
        """设置网页调用console触发的回调


        .. code:: c

            //python 事件响应函数(conext:dict,args=[level:str,msg:str,sourceName:str,sourceLine:int,stackTrace:str],kwargs=None) 
            typedef void(WKE_CALL_TYPE*wkeConsoleCallback)(wkeWebView webView, void* param, wkeConsoleLevel level, const wkeString message, const wkeString sourceName, unsigned sourceLine, const wkeString stackTrace);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """
        eventid = self._on(pwebview,'onConsole',func,param)       
        return self.dll.wkeOnConsole(pwebview.cId,self._wkeConsoleCallback,eventid)

    @WkeMethod(CFUNCTYPE(None, _LRESULT,_LRESULT, c_int,c_void_p,c_void_p,c_ulonglong,c_void_p))
    def _wkeConsoleCallback(self,cwebview,param,level,msg,sourceName,sourceLine,stackTrace):
        msg=self.dll.wkeGetStringW(msg)
        sourceName=self.dll.wkeGetStringW(sourceName)
        stackTrace=self.dll.wkeGetStringW(stackTrace)
        return self._callback(cwebview, param=param,level=level,msg=msg,sourceName=sourceName,sourceLine=sourceLine,stackTrace=stackTrace)
    

    def onDownload(self,pwebview,func,param = None):
        """设置网页开始下载的回调

    
        .. code:: c

            //python 事件响应函数(conext:dict,args=[url:str],kwargs=None) 
            typedef bool(WKE_CALL_TYPE*wkeDownloadCallback)(wkeWebView webView, void* param, const char* url);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None
        """   
        eventid = self._on(pwebview,'onDownload',func,param)         
        return self.dll.wkeOnDownload(pwebview.cId,self._wkeDownloadCallback,eventid)
        
    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,_LRESULT,c_char_p))
    def _wkeDownloadCallback(self,cwebview,param,url):
        url=self.dll.wkeGetStringW(url)
        return self._callback(cwebview, param=param, url=url)


    def onNetResponse(self,pwebview,func,param = None):
        """设置收到网络请求的回调

        一个网络请求发送后，收到服务器response触发回调

      
        .. code:: c

            //python 事件响应函数(conext:dict,args=[url:str,job:c_void_p],kwargs=None)  
            typedef bool(WKE_CALL_TYPE*wkeNetResponseCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None 

        TODO:
            JOB 参数未C翻译到Py      
        """
        eventid = self._on(pwebview,'onNetResponse',func,param)   
        return self.dll.wkeNetOnResponse(pwebview.cId,self._wkeNetResponseCallback,eventid)   

    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_void_p))
    def _wkeNetResponseCallback(self,cwebview,param,url,job):
        url=url.decode()
        return self._callback(cwebview, param=param, url=url,job=job)


    def onLoadUrlBegin(self,pwebview,func,param = None):
        """设置网络请求发起前的回调
        
        任何网络请求发起前会触发此回调

        
        .. code:: c

            //python 事件响应函数(conext:dict,args=[url:str],kwargs=None)  
            typedef bool(*wkeLoadUrlBeginCallback)(wkeWebView webView, void* param, const char *url, void *job);

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
        return self.dll.wkeOnLoadUrlBegin(pwebview.cId,self._wkeLoadUrlBeginCallback,eventid)

    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,_LRESULT,c_char_p,c_void_p))
    def _wkeLoadUrlBeginCallback(self,cwebview,param,url,job):
        url=url.decode()
        return self._callback(cwebview, param=param,url=url,job=job)


    def onLoadUrlEnd(self,pwebview,func,param = None):
        """设置网络请求结束的回调

            如果在wkeLoadUrlBeginCallback里没设置wkeNetHookRequest，则不会触发wkeOnLoadUrlEnd回调。

        .. code:: c

            //python 事件响应函数(conext:dict,args=[url:str,job:struct *,buf:c_char_p,lens:int],kwargs=None)  
            typedef void(WKE_CALL_TYPE*wkeLoadUrlEndCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job, void* buf, int len);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None    

        TODO:
            job未翻译
        """
        eventid = self._on(pwebview,'onLoadUrllEnd',func,param)   
        return self.dll.wkeOnLoadUrlEnd(pwebview.cId,self._wkeLoadUrlEndCallback,eventid)

    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,_LRESULT,c_char_p,c_void_p,c_void_p,c_int))
    def _wkeLoadUrlEndCallback(self,cwebview,param,url,job,buf,lens):
        url=url.decode()
        return self._callback(cwebview, param=param,url=url,job=job,buf=buf,lens=lens)


    def onLoadUrlFail(self,pwebview,func,param = None):
        """设置网络请求失败的回调

        .. code:: c

            //python 事件响应函数(conext:dict,args=[url:str,job:struct *],kwargs=None)  
            typedef void(WKE_CALL_TYPE*wkeLoadUrlFailCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None    

        TODO:
            job未翻译
        """
        eventid = self._on(pwebview,'onLoadUrllFail',func,param)   
        return self.dll.wkeOnLoadUrlFail(pwebview.cId,self._wkeLoadUrlFailCallback,eventid)

    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,_LRESULT,c_char_p,c_void_p))
    def _wkeLoadUrlFailCallback(self,cwebview,param,url,job):
        return self._callback(cwebview, param=param,url=url,job=job)
    

    def onLoadUrlFinish(self,pwebview,func,param = None):
        """设置网络请求完成的回调

        .. code:: c

            //python 事件响应函数(conext:dict,args=[url:str,result:int,failedReason:str],kwargs=None)  
            typedef void(WKE_CALL_TYPE*wkeLoadUrlFailCallback)(wkeWebView webView, void* param, const utf8* url, wkeNetJob job);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None    
        """
        eventid = self._on(pwebview,'onLoadUrlFinish',func,param)   
        return self.dll.wkeOnLoadUrlFinish(pwebview.cId,self._wkeLoadUrlFinishCallback,eventid)

    @WkeMethod(CFUNCTYPE(c_bool,_LRESULT,_LRESULT,c_char_p,c_int,c_char_p))
    def _wkeLoadUrlFinishCallback(self,cwebview,param,url,result,failedReason):
        url=self.mb.wkeGetStringW(url)
        if result==1:
            failedReason=self.dll.wkeGetStringW(failedReason)            
        return self._callback(cwebview, param=param,url=url,result=result,failedReason=failedReason)
    

    def onGetFavicon(self,pwebview,func,param = None):
        """设置获取favicon的回调

        NOTE:
            此接口必须在wkeOnLoadingFinish回调里调用。可以用下面方式来判断是否是主frame的LoadingFinish:

            	tempInfo = webview.getTempCallbackInfo()
			    if (webview.isMainFrame(temInfo.frame)) :
			        webview.wkeNetGetFavicon(HandleFaviconReceived, divaram);
			    
        .. code:: c

            //python 事件响应函数(conext:dict,args=[url:str,buf:wkeMemBuf *],kwargs=None)  
            typedef void(WKE_CALL_TYPE*wkeOnNetGetFaviconCallback)(wkeWebView webView, void* param, const utf8* url, wkeMemBuf* buf);

        Args:
            pwebview(WebView):      webview对象(py) 
            func(function):         通知回调函数,事件发生时调用
            param(any, optional):   回调上下文参数,默认为None    
        """
        eventid = self._on(pwebview,'onGetFavicon',func,param)   
        return self.dll.wkeNetGetFavicon(pwebview.cId,self._wkeOnNetGetFaviconCallback,eventid) 
    
    @WkeMethod(CFUNCTYPE(None, _LRESULT,_LRESULT,c_char_p,POINTER(wkeMemBuf)))
    def _wkeOnNetGetFaviconCallback(self,cwebview,param,url,buf): 
        url=url.decode()
        return self._callback(cwebview, param=param,url=url,buf=buf)

  