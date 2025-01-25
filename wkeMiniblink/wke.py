# -*- coding:utf-8 -*-
import os,sys,platform,time
import binascii
from inspect import getmembers


from . import _LRESULT,WkeCallbackError,MINIBLINK_DLL_PATH,SetMiniblinkDLL,GetMiniblinkDLL
from .miniblink import MiniblinkInit
from .wkeStruct import *
from .wkeEvent import WkeEvent

from ctypes import (c_void_p,
    c_int,
    c_ushort,c_longlong,c_ulonglong,
    c_wchar_p,
    c_float,
    byref,
    CFUNCTYPE,
    py_object,
    cast
)


@CFUNCTYPE(None,_LRESULT,_LRESULT)
def _WkeJsBindCallback(execState,c_id):
    """
    jsBind的C-Python 回调函数,调用实际注册在Wke上下文中的Py函数
    """
    if c_id in Wke._jsBinderContext:
        context = Wke._jsBinderContext[c_id]
        return context["func"](es=execState,param=context["param"])   
    return None

class Wke():
    """Wke全局接口

    Examples:
        .. code:: python
        
            Wke.init("miniblink_4975_x32.dll")
            ....
            Wke.runMessageLoop()

    """   
    #动态库
    dll = None
    #js管理
    js = None
    #事件管理
    event = None
    #接口版本数值
    version = 0

    _jsBinderContext = {}


    _localStagePath = None
    _cookiePath =  None
    @staticmethod
    def Version():
        return Wke.dll.wkeVersionString()

    @staticmethod
    def init(path=MINIBLINK_DLL_PATH,**kwargs):
        """加载动态库

        初始化整个mb。此句必须在所有mb api前最先调用。并且所有mb api必须和调用wkeInit的线程为同个线程

        Args:
            path(str):   动态库的文件位置

        """
        
        Wke.dll = MiniblinkInit(path)
        SetMiniblinkDLL(Wke.dll)
        Wke.event = WkeEvent()

        Wke.version = Wke.dll.wkeVersion()
        #复制动态库中所有wke开头的功能函数
        for name,func in getmembers(Wke.dll):
            if name.startswith(("wke")):
                setattr(Wke,name,func)


        

        return
    
    @staticmethod
    def getDLL():
        """返回动态库DLL对象

        Returns:
            cdll: 动态库DLL对象
        """
        return Wke.dll
    
    @staticmethod
    def loaded():
        """查询是否已加载动态库

        Returns:
            bool: 已加载返回True,未加载返回False
        """
        if Wke.dll is None:
            return False
        return True
    

    
    @staticmethod
    def setCookieAndStagePath(**kwargs):
        """设置Cookie/LocalStage的存储路径

        Keyword Args:
            cookie(str): Cookie的存储文件路径
            localStagePath(str): LocalStage的存储目录路径

        """
        if "cookie" in kwargs:
            Wke._cookiePath = os.path.realpath(kwargs["cookie"])
        if "localStage" in kwargs:
            Wke._localStagePath = os.path.realpath(kwargs["localStage"])
        return 

    @staticmethod  
    def _jsBindFunction(jsFuncName,pyCallback, param=0,arg_count=0):
        """设置一个python回调函数作为指定名称的js函数使用

        Args:
            jsFuncName(str):        js函数名
            pyCallback(function):   python函数
            param(any, optional):             回调上下文
            arg_count(int, optional):         参数个数
        """
        return Wke.dll.wkeJsBindFunction(jsFuncName,pyCallback,arg_count,param)   
    
    @staticmethod    
    def runMessageLoop():
        """Wke执行消息循环

        也可以用win32gui.PumpMessages()
        """
        Wke.dll.wkeRunMessageLoop(0)


    
    @staticmethod    
    def jsGC():
        """JS触发垃圾回收
        """
        Wke.dll.jsGC()



    @staticmethod   
    def extend(func,name,param=0,arg_count=1):
        """使用一个指定的python函数作为js扩展实现的函数
  
        Examples:
            .. code:: python

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

            在HTML中

            .. code:: html
            
                <button onclick="jsCallpy('jsCallpy', 666)" style='margin-right: 20px;cursor: pointer;'>jsCallpy</button>

            .. code-block:: c
        
                void wkeJsBindFunction(const char* name, wkeJsNativeFunction fn, void* param, unsigned int argCount); //C原型

        Args:
            func(:obj:`function`):         扩展函数的python实现
            name(:obj:`str`):              扩展的python函数在js中的名称
            param(any, optional):          python函数的回调上下文
            arg_count(int, optional):      扩展函数的参数个数
        Raise:
            SyntaxError : func为不可调用时抛出            
        """  
    
        if not callable(func) :
            raise SyntaxError(f"{func} not callable")
        rawname = name.encode()
        funcid = id(func)
        Wke._jsBinderContext[funcid]={"param":param,"name":name,"rawname":rawname,"func":func,"argcount":arg_count}
        
        return Wke._jsBindFunction(rawname,_WkeJsBindCallback,arg_count,_LRESULT(funcid)) 

    @staticmethod  
    def jsArgCount(arg):
        """获取JS对象中变量的个数

        Args:
            arg(jsVar):   JS对象
        Returns:
            int: JS对象中变量的个数
        """
                
        return Wke.dll.jsArgCount(arg)

    @staticmethod  
    def getJsArgs(es,arg_count):
        """JS状态机中arg_count个对象转换成py对象列表

        Args:
            es(str):        JS状态机
            arg_count(int, optional):         参数个数
        Returns:
            jsVar: JS对象

        """
        val_ls=[None]*arg_count
        for i in range(arg_count):
            arg_type=Wke.dll.jsArgType(es,i)
            
            if arg_type==0:
                val=Wke.dll.jsArg(es,i)
                val=Wke.dll.jsToInt(es, c_longlong(val))
            elif arg_type==1:
                val=Wke.dll.jsArg(es,i)
                val=Wke.dll.jsToTempStringW(es, c_longlong(val))            
            elif arg_type==2:
                val=Wke.dll.jsArg(es,i)
                val=Wke.dll.jsToTempStringW(es, c_longlong(val))
                if val=='false':
                    val=False
                else:
                    val=True
            
            elif arg_type==5 or arg_type==7:
                val=None
            elif arg_type==6:
                val=Wke.dll.jsArg(es,i)
                lens=Wke.dll.jsGetLength(es,c_longlong(val))
                tmp_arr=[None]*lens
                for j in range(lens):
                    tmp_val=Wke.dll.jsGetAt(es,c_longlong(val),j)            
                    if Wke.dll.jsIsNumber(tmp_val)==1:
                        tmp_val=Wke.dll.jsToInt(es, c_longlong(tmp_val))
                    elif Wke.dll.jsIsString(tmp_val)==1:
                        tmp_val=Wke.dll.jsToTempStringW(es, c_longlong(tmp_val))
                        tmp_val=c_wchar_p(tmp_val).value
                    elif Wke.dll.jsIsBoolean(tmp_val)==1:
                        tmp_val=Wke.dll.jsToTempStringW(es, c_longlong(tmp_val))
                        if tmp_val=='false':
                            tmp_val=False
                        else:
                            tmp_val=True
                    tmp_arr[j]=tmp_val
                val=tmp_arr
            else:
                val=Wke.dll.jsArg(es,i)
                val=Wke.dll.jsToTempStringW(es, c_longlong(val))
            val_ls[i]=val
        
        return val_ls
    
    @staticmethod  
    def setJsArgs(es,val):
        """将python对象val转换成JS状态机中的JS对象

        Args:
            es(str):        JS状态机
            val(any):       python对象
        """
        if isinstance(val,str):
            val=Wke.dll.jsStringW(es,val)
        elif isinstance(val,int):
            val=Wke.dll.jsInt(val)
        elif isinstance(val,float):
            val=Wke.dll.jsFloat(val)
        elif isinstance(val,bool):
            val=Wke.dll.jsBoolean(val)

        elif isinstance(val,list):
            lens=len(val)
            tmp_arr=Wke.dll.jsEmptyArray(es)
            for i in range(lens):
                if isinstance(val[i],int):
                    tmp_val=Wke.dll.jsInt(val[i])
                elif isinstance(val[i],str):
                    tmp_val=Wke.dll.jsStringW(es,val[i])
                elif isinstance(val[i],float):
                    tmp_val=Wke.dll.jsFloat(c_float(val[i]))
                Wke.dll.jsSetAt(es, c_longlong(tmp_arr), i, c_longlong(tmp_val))
            val=tmp_arr
        elif isinstance(val,dict): 
            tmp_obj=Wke.dll.jsEmptyObject(es)
            for k,v in val.items():
                if isinstance(v,int):
                    v=Wke.dll.jsInt(v)
                elif isinstance(v,str):
                    v=Wke.dll.jsStringW(es,v)
                elif isinstance(v,float):
                    v=Wke.dll.jsFloat(c_float(v))
                Wke.dll.jsSet(es,c_longlong(tmp_obj),k.encode(),c_longlong(v))
            val=tmp_obj
        return val
    
    @staticmethod  
    def buildProxy(self,ip,port,proxy_type=1,user=None,password=None):
        """创建代理配置对象

        Args:
            ip(str): 代理IP 地址
            port(int): 代理端口
            proxy_type(int): 代理类型
            user(str):  代理账号
            password(str): 代理账号密码
        Returns:
            wkeProxy: 代理对象
        """

        if not all([ip,port]):return None
        if user==None:
            user=b''
        else:
            user=user.encode('utf8')
        if password==None:
            password=b''
        else:
            password=password.encode('utf8')
        ip=ip.encode('utf8')
        port=int(port)

        proxy= wkeProxy(type=c_int(proxy_type), hostname=ip, port=c_ushort(port),username=user,password=password)
      
        return proxy
    
    @staticmethod   
    def setProxy(ip,port,proxy_type=1,user=None,password=None):
        """ 设置全局代理

        Args:
            ip(str): 代理IP 地址
            port(int): 代理端口
            proxy_type(wkeProxyType): 代理类型
            user(str):  代理账号
            password(str): 代理账号密码
        Returns:
            wkeProxy: 代理对象
        """    
       
        proxy= Wke.buildProxy(ip,port,proxy_type,user,password)
        if proxy is not None:
            Wke.dll.wkeSetProxy(proxy)
        return proxy





       
    

    


class WebView():
    """Wke网页视图

    实现离屏网页视图功能，包括加载/渲染/设置/Js/Cookie等。
    
    并不实际创建一个窗口,需要绑定一个外部窗口，使用额外的API将Webview的内容绘制到窗口上并处理某些需要的窗口消息。
 
    """

    def __init__(self,*args,**kwargs):
        super().__init__()
        self.dll = Wke.getDLL()
        self.cId = 0
        self.isZoom=False
        self.isTransparent=False
        self.factor = 1.0
        self.type = -1
        self.hwnd = None
        self.hdc = None
        self.x = -1
        self.y = -1
        self.w = -1
        self.h = -1
        self.name = None

        self._localStagePath = None
        self._cookiePath =  None

        return

    def setCookieAndStagePath(self,**kwargs):
        """设置Cookie/LocalStage的存储路径

        Keyword Args:
            cookie(str): Cookie的存储文件路径
            localStagePath(str): LocalStage的存储目录路径
        """

        if "cookie" in kwargs and os.path.exists(kwargs["cookie"]):
            self._cookiePath = os.path.realpath(kwargs["cookie"])
        if "localStage" in kwargs and os.path.exists(kwargs["localStage"]):
            self._localStagePath = os.path.realpath(kwargs["localStage"])
        
        if self._cookiePath is None:
            self._cookiePath = Wke._cookiePath

        self.setCookieJarFullPath(self._cookiePath)

        if self._localStagePath is None:
            self._localStagePath = Wke._localStagePath

        self.setLocalStorageFullPath(self._localStagePath)

        return
    
    def __del__(self):
        if self.cId is not None:
            self.destroy()
        return
    
    @property
    def id(self):
        """页面的句柄

        Returns:
            int: 视图页面的句柄,即c api获取的webview

        """
        return self.cId

    @property
    def width(self):
        """页面宽度  

        Returns:
            int: 视图页面宽度
        """
        self.w = self.dll.wkeWidth(self.cId)
        return self.w
    
    @property   
    def height(self): 
        """页面高度

        Returns:
            int:  视图页面高度
        """
        self.h = self.dll.wkeHeight(self.cId)   
        return self.h
    
    @property   
    def contentsWidth(self): 
        """页面内容宽度

        Returns:
            int: 视图页面内容宽度
        """ 
        return self.dll.wkeContentsWidth(self.cId)

    @property       
    def contentsHeight(self):
        """页面内容高度

        Returns:
            int: 视图页面内容高度
        """ 
        
        return self.dll.wkeContentsHeight(self.cId)
     
    def create(self):
        """创建一个页面webview，但不创建真窗口

        Returns:
            int: 页面的C句柄
        """
        self.cId = self.dll.wkeCreateWebView()
        return self.cId 
    
    def bind(self,hwnd,x=0,y=0,width=640,height=480):
        """为页面绑定一个实际的窗口

        Args:
            hwnd (int):         窗口句柄
            x (int):            窗口绑定区域左上角起始点的x坐标
            y (int):            y坐标
            width (int):        宽度
            height (int):       高度
        Returns:
            int: 页面的C句柄
        """
        if hwnd==0:
            return 0
        
        #创建一个页面,获取句柄
        self.cId = self.dll.wkeCreateWebView()

        #为页面设定窗体句柄
        self.setHandle(hwnd)
        #将页面缩放到适合窗体大小
        self.resize(width,height)
        self.setHandleOffset(x,y)

        self.hwnd = hwnd
        self.x,self.y = x,y
        self.w,self.h = width,height

        return self.cId
    
    
    def destroy(self):
        """销毁wkeWebView对应的所有数据结构，包括真实窗口等
        """
        self.dll.wkeDestroyWebView(self.cId)
        self.hwnd = 0
        self.x,self.y = -1,-1
        self.w,self.h = -1,-1   
        self.isZoom=False
        self.isTransparent=False
        return 
    
    
    def setWebViewName(self,name):
        """设置页面名称

        Args:
            name(:obj:`str`):         窗口名称   
        """
        self.dll.wkeSetWebViewName(self.cId,name.encode())
        self.name = name
        return 


    
    def resize(self,width,height):
        """调整页面大小

        Args:
            width(int):            宽度
            height(int):           高度
        Returns:
            bool: 参数合法返回True,否则False
        """ 
        if width==0 or height==0:return False
        self.w ,self.h = width,height
        self.dll.wkeResize(self.cId,width,height)
        return True

    def setWindowTitle(self,title:str):
        """设置页面标题

        Args:
            title(str):            标题
        """ 
        return self.dll.wkeSetWindowTitleW(self.cId,title)

    def getWindowTitle(self):
        """获取页面标题

        Returns:
            str:            标题
        """ 
        return self.dll.wkeGetWindowTitle(self.cId)


    def showWindow(self,show=True):
        """设置页面显示与隐藏

        Args:
            show(bool):            True显示,False隐藏
        """ 
        self.dll.wkeShowWindow(self.cId,show)
        return 

    def MoveWindow(self,x:int,y:int,w:int,h:int):
        """设置页面位置与大小

        Args:
            x(int):            页面左上点x坐标
            y(int):            页面左上点y坐标
            w(int):            页面宽度
            h(int):            页面高度
        """ 
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.dll.wkeMoveWindow(self.cId,x,w,w,h)
        return

    def moveToCenter(self):
        """移动页面到中央
        """ 
        self.dll.wkeMoveToCenter(self.cId)
        return 

    def setFocus(self):
        """设置webview是焦点态,如果webveiw关联了窗口，窗口也会有焦点
        """ 
        self.dll.wkeSetFocus(self.cId)
        return 
    
    def killFocus(self):
        """设置webview是焦点态,如果webveiw关联了窗口，窗口也会有焦点
        """ 
        self.dll.wkeKillFocus(self.cId)
        return 


    def setDragEnable(self,drag=True):
        """设置页面可拖拽与否

        Args:
            drag(bool):            True可拖拽,False不可拖拽
        """ 
        self.dll.wkeSetDragEnable(self.cId,drag)
        return 
       
    def setZoomFactor(self,factor):
        """设置页面缩放

        Args:
            factor(float):      缩放倍率
        """
        self.factor =factor
        self.dll.wkeSetZoomFactor(self.cId,factor)
        return
    
    def getZoomFactor(self,factor):
        """获取页面缩放

        Returns:
            float:      缩放倍率
        """
        self.factor = self.dll.wkeGetZoomFactor(self.cId)
        return self.factor
    
    def setTransparent(self,transparent):
        """设置页面透明模式与否

        Args:
            transparent(bool):            True透明,False不透明
        """ 
        self.dll.wkeSetTransparent(self.cId,transparent)   
        return
    
    def getCaretRect(self):
        """获取编辑框的游标的位置

        Returns:
            int: 编辑框的游标的位置
        """
        return self.dll.wkeGetCaretRect()

    def getMainFrameId(self):
        """查询主帧编号

        Returns:
            int: 主帧编号
        """
        return self.dll.wkeWebFrameGetMainFrame(self.cId)

    def getFrameUrl(self,frameId:int):
        """查询指定编号帧的链接

        Args:
            int: 帧编号
        Returns:
            str: 帧链接
        """
        url = self.dll.wkeGetFrameUrl(self.cId)
        return url

    def isMainFrame(self,frameId):
        """查询指定编号的帧是否是主帧

        Args:
            frameId(int):      帧编号
        Returns:
            bool: 是主帧返回True,不是返回False
        """
        return self.dll.wkeIsMainFrame(self.cId,frameId)
    
    def getTempCallbackInfo(self):
        """获取视图当前回调函数的临时信息

        Returns:
            WKETempCallbackInfo: 临时信息
        """
        return self.dll.wkeGetTempCallbackInfo(self.cId)

    def setUserKeyValue(self,k,v):
        """为视图的c对象设置一个绑定的k:v对

        Args:
            k(str):      绑定键
            v(any):      绑定对象
        """   
        val = py_object(v)
        k = k.encode()
       
        return self.dll.wkeSetUserKeyValue(self.cId,k,val)

    def getUserKeyValue(self,k:str):
        """获取视图绑定的k键对应的对象

        Args:
            k(str):     绑定键
        Returns:
            object:        绑定对象
        """   
        k = k.encode()
        cPtrOfPyobj = self.dll.wkeGetUserKeyValue(self.cId,k)
        cPyObj = cast(cPtrOfPyobj,py_object)
        return cPyObj.value
   
    



   
    ##############Res##############   
    def setHandleOffset(self,x,y):
        """设置无窗口模式下的绘制偏移。在某些情况下（主要是离屏模式），绘制的地方不在真窗口的(0, 0)处，就需要手动调用此接口

        Args:
            x(int):            绘制偏移x
            y(int):            绘制偏移y
        """
        self.dll.wkeSetHandleOffset(self.cId,x,y)

    def setHandle(self,hwnd):
        """设置wkeWebView对应的窗口句柄
            注意：只有在无窗口模式下才能使用。如果是用wkeCreateWebWindow创建的webview，已经自带窗口句柄了。

        Args:
            hwnd(int):            窗口句柄
        """
        self.dll.wkeSetHandle(self.cId,hwnd)
        self.hwnd = hwnd
        return

    def getWindowHandle(self):
        """获取wkeWebView对应的窗口句柄

        Returns:
            int: 页面的窗口句柄
        """
        return self.dll.wkeGetWindowHandle(self.cId)

    def getViewDC(self): 
        """获取wkeWebView对应的设备上下文句柄

        Returns:
            DC: 页面的设备上下文句柄
        """
        self.hdc = self.dll.wkeGetViewDC(self.cId)
        return self.hdc

    def unlockViewDC(self): 
        """解锁wkeWebView对应的设备上下文句柄


        """
        self.dll.wkeUnlockViewDC(self.cId)
        return 
    ##############Setting##############   

    
    def setUserAgentW(self,ua):
        """设置页面对应的浏览器标识字符串

        Args:
            ua(str): 浏览器标识字符串
        """
        self.dll.wkeSetUserAgentW(self.cId,ua)

    def getUserAgent(self):
        """获取页面对应的浏览器标识字符串

        Returns:
            str: ua浏览器标识字符串
        """
        ua=self.dll.wkeGetUserAgent(self.cId)
        return ua.decode()        
    

    def setProxy(self,ip,port,proxy_type=1,user=None,password=None):
        """设置页面专属的代理

        Args:
            ip(str): 代理IP 地址
            port(int): 代理端口
            proxy_type(int): 代理类型
            user(str):  代理账号
            password(str): 代理账号密码
        Returns:
            wkeProxy: 代理对象
        """
        proxy= Wke.buildProxy(ip,port,proxy_type,user,password)
        if proxy is not None:
            self.dll.wkeSetViewProxy(self.cId,proxy)
        return proxy
    
    def setContextMenuEnabled(self,en:bool):
        """设置页面右键上下文菜单使能与否

        Args:
            en(bool): True使能,False禁止
        """
        self.dll.wkeSetContextMenuEnabled(self.cId,en)


    def addPluginDirectory(self,_path):
        """设置页面右键上下文菜单使能与否

        Todo: 
            API文档上没有这一段

        Args:
            en(bool): True使能,False禁止
        """
        self.dll.wkeAddPluginDirectory(self.cId,_path)
        return

    def setNpapiPluginsEnabled(self,en):
        """开启关闭npapi插件，如flash

        Args:
            en(bool): True使能,False禁止
        """

        self.dll.wkeSetNpapiPluginsEnabled(self.cId,en)
        return
    
    def setCspCheckEnable(self,en=False):
        """关闭后，跨域检查将被禁止，此时可以做任何跨域操作，如跨域ajax，跨域设置iframe

        Args:
            en(bool): True使能,False禁止    
        """
        self.dll.wkeSetCspCheckEnable(self.cId,en)
        return
    
    def setDebugConfig(self,debugString:str,param):
        """开启一些实验性选项。

        Args：
            debugString(str)：选项名称

                =========================     ========================================================
                "showDevTools"	                开启开发者工具，此时param要填写开发者工具的资源路径        
                "wakeMinInterval"	            设置帧率，默认值是10，值越大帧率越低
                "drawMinInterval"	            设置帧率，默认值是3，值越大帧率越低
                "antiAlias"	                    设置抗锯齿渲染。param必须设置为"1"
                "minimumFontSize"	            最小字体
                "minimumLogicalFontSize"	    最小逻辑字体
                "defaultFontSize"	            默认字体
                "defaultFixedFontSize"	        默认fixed字体
                =========================     ========================================================

            param : relate to debugString

            *注意*:开发者工具设置时,param必须是utf8编码,如file:///c:/miniblink-release/front_end/inspector.html。

        """
        debug=debugString.encode()
        if isinstance(param,str):
            param=param.encode()
        self.dll.wkeSetDebugConfig(self.cId,debug,param)

    def setHeadlessEnabled(self,en:bool):  
        """开启无头模式与否
            开启后，将不会渲染页面，提升了网页性能。

        Args:
            en(bool): True使能,False禁止  
        """
        self.dll.wkeSetHeadlessEnabled(self.cId,en)
        return

    def setTouchEnabled(self,en:bool):
        """开启触摸模式与否
            开启后，鼠标事件转换为触摸事件

        Args:
            en(bool): True使能,False禁止  
        """
        b=not en
        self.dll.wkeSetTouchEnabled(self.cId,en)
        self.dll.wkeSetMouseEnabled(self.cId,b)
        return
    
    def setDeviceParameter(self,device,paramStr,paramInt,paramFloat):
        """设置设备模拟器选项

        void wkeSetDeviceParameter(wkeWebView webView, const char* device, const char* paramStr, int paramInt, float paramFloat)
        （已废弃）设置mb模拟的硬件设备环境。主要用在伪装手机设备场

        device：设备的字符串。可取值有：
        ===========================     =================================================================================
        "navigator.maxTouchPoints"	    此时 paramInt 需要被设置，表示 touch 的点数
        "navigator.platform"	        此时 paramStr 需要被设置，表示js里获取的 navigator.platform字符串
        "navigator.hardwareConcurrency"	此时 paramInt 需要被设置，表示js里获取的 navigator.hardwareConcurrency 整数值
        "screen.width"	                此时 paramInt 需要被设置，表示js里获取的 screen.width 整数值
        "screen.height"	                此时 paramInt 需要被设置，表示js里获取的 screen.height 整数值
        "screen.availWidth"	            此时 paramInt 需要被设置，表示js里获取的 screen.availWidth 整数值
        "screen.availHeight"	        此时 paramInt 需要被设置，表示js里获取的 screen.availHeight 整数值
        "screen.pixelDepth"	            此时 paramInt 需要被设置，表示js里获取的 screen.pixelDepth 整数值
        "screen.pixelDepth"	            目前等价于"screen.pixelDepth"
        "window.devicePixelRatio"	    同上
        ===========================     =================================================================================
        """
        device=device.encode()
        if device=='':
            device=b''
        else:
            device=device.encode()
        self.dll.wkeSetDeviceParameter(self.cId, device,paramStr,c_int(paramInt),c_float(paramFloat)) 
        return

    def setNavigationToNewWindowEnable(self,en):
        """设置新窗口跳转允许

        Args:
            en(bool): True允许,False禁止,所有新窗口跳转都在本窗口进行  
        """
        self.dll.wkeSetNavigationToNewWindowEnable(self.cId,en)
        return
    
    ##############File##############           
    def goForward(self):
        """页面前进,在历史列表中前进
        """
        self.dll.wkeGoForward(self.cId)

    def canGoForward(self):
        """页面是否能前进
        """
        return self.dll.wkeCanGoForward(self.cId)

    def goBack(self):
        """网页页面回退
        """
        self.dll.wkeGoBack(self.cId)

    def canGoBack(self):
        """页面是否能回退
        """
        return self.dll.wkeCanGoBack(self.cId)
    

    def editorSelectAll(self):
        """页面全选
        """
        return self.dll.wkeEditorSelectAll(self.cId)       
    def editorUnSelect(self):
        """页面反选
        """
        return self.dll.wkeEditorUnSelect(self.cId)  
    def editorCopy(self):
        """页面选择复制
        """
        return self.dll.wkeEditorCopy(self.cId)    
    def editorCut(self):
        """页面选择复制
        """
        return self.dll.wkeEditorCut(self.cId)  
    
    def editorDelete(self):
        """页面选择删除
        """
        return self.dll.wkeEditorDelete(self.cId)     
    def editorUndo(self):
        """页面选择撤销
        """
        return self.dll.wkeEditorUndo(self.cId) 
    def editorRedo(self):
        """页面选择重做
        """
        return self.dll.wkeEditorRedo(self.cId) 
        
    def loadURL(self,url:str):
        """网页页面加载指定的链接地址

        Args:
            url(str): 网页链接地址
        """
        return self.dll.wkeLoadURL(self.cId,url.encode())

    def loadURLW(self,url):
        """网页页面加载指定的链接地址,unicode

        Args:
            url(str): 网页链接地址
        """
        return self.dll.wkeLoadURLW(self.cId,url)

    def loadHTML(self,html:str):
        """网页页面加载指定的HTML内容,string

        Args:
            html(str): HTML内容
        """
        self.dll.wkeLoadHTML(self.cId,html.encode())

    def loadHTMLW(self,html):
        """网页页面加载指定的HTML内容,unicode

        Args:
            html(str): HTML内容
        """
        self.dll.wkeLoadHTMLW(self.cId,html)

    def loadFile(self,file_path):
        """网页页面加载指定的HTML文件

        Args:
            file_path(str): HTML文件路径
        """
        file_path=file_path.encode()
        self.dll.wkeLoadFile(self.cId,file_path)
        return 
    
    def postURL(self,data):
        """
        """
        data=data.encode()
        lens=len(data)
        self.dll.wkeLoadURLW(self.cId,data,lens)
        return 
    
    def reload(self):
        """网页刷新
        """
        return self.dll.wkeReload(self.cId)

    def stopLoading(self):
        """网页停止加载
        """
        return self.dll.wkeStopLoading(self.cId)



    def getURL(self):
        """获取页面的地址
        
        Returns:
            str:    地址
        """
        url=self.dll.wkeGetURL(self.cId)
        return url.decode()
    
    def getFrameUrl(self,frameId):
        """获取页面的指定编号的frame的链接地址

        Args:  
            frameId(int):   帧编号
        Returns:
            str:    地址
        """
        url=self.dll.wkeGetFrameUrl(self.cId,frameId)
        return url.decode('utf8')  
    
    def getSource(self):
        """获取页面的内容
        
        Returns:
            str:    内容
        """
        source=self.dll.wkeGetSource(self.cId)
        return source.decode()
    
    def utilSerializeToMHTML(self):
        """
        Todo: 
            API文档上没有这一段
        """
        mhtml_content=self.dll.wkeUtilSerializeToMHTML(self.cId)
        return mhtml_content




    def setResponseData(self,job,data='',file_name=None):
        """
        Todo: 
            API文档上没有这一段
        """
        lens=len(data)
        if lens!=0:
            self.dll.wkeNetSetData(job,data,lens)
            return True
        elif file_name!=None:
            with open(file_name) as f:
                data=f.read()
                data=data.encode()
                lens=len(data)
            if lens!=0:
                if '.js' in file_name:
                    self.dll.wkeNetSetMIMEType(job,b'text/javascript')
                elif '.html' in file_name:
                    self.dll.wkeNetSetMIMEType(job,b'text/html')
                self.dll.wkeNetSetData(job,data,lens)
                return True
        return False    
    
    def cancelRequest(self,job,url,ident_ls=['.jpg']):
        """
        FIXME: 
            没修正
        """  
        for x in ident_ls:
            if  x in url:
                self.dll.wkeNetCancelRequest(job)
                return True
        return False
    
    def getPostData(self,job,url,ident=''):
        """
        FIXME: 
            没修正
        """  
        if ident not in url:return '',0,None
        elements=self.dll.wkeNetGetPostBody(job)
        try:
            data=elements.contents.element.contents.contents.data.contents.data
            lens=elements.contents.element.contents.contents.data.contents.length
        except:
            return '',0,None
        data=data[:lens].decode('utf8','ignore')
        print('post_data',data,lens)
        return data,lens,elements
    
    def saveBufData(self,url,buf,lens):
        """
        FIXME: 
            没修正
        """
        if lens==0:return
        contents=(c_char * lens).from_address(buf)
        _type=self.get_type(url)
        if _type==None:return
        name=binascii.crc32(url.encode())
        file_name=f'{name}{_type}'
        try:
            with open(file_name,'wb') as f:
                f.write(contents)
            self.bufs.append({url:file_name})
        except:
            ...
        finally:
            ...
 

    ##############Cookie##############
    def setCookie(self,url,cookie):
        """设置页面cookie

        Args:  
            url(int):   页面文件地址
            cookie(str): 页面cookie字符串
        Returns:
            str:    地址

        .. note::
            cookie必须符合curl的cookie写法。一个例子是：

            PERSONALIZE=123;expires=Monday, 13-Jun-2022 03:04:55 GMT; domain=.fidelity.com; path=/; secure

        """
        cookie=cookie.split(';')
        for x in cookie:
            self.dll.wkeSetCookie(self.cId,url.encode('utf8'),x.encode('utf8'))
        #self.dll.wkePerformCookieCommand(self.cId,2)
        return
    
    def getCookieW(self):
        """获取页面cookie

        Returns:
            str:    页面cookie字符串

        """
        return self.dll.wkeGetCookieW(self.cId)

    def clearCookie(self):
        """清除页面cookie

        TODO:
            官方文档说目前只支持清理所有页面的cookie。
            
        """
        self.dll.wkeClearCookie(self.cId)


    def setLocalStorageFullPath(self,path):
        """设置local storage的全路径

        *注意*：这个接口只能接受目录。如“c:\\mb\\LocalStorage\”
        """
        self.dll.wkeSetLocalStorageFullPath(self.cId,path)
        return
    
    def setCookieJarPath(self,path):
        """设置页面cookie的本地文件目录

        Args:  
            path(str): 页面cookie文件存储目录

        默认是当前目录。cookies存在当前目录的“cookie.dat”里
        """
        return self.dll.wkeSetCookieJarPath(self.cId,path)
   
    def setCookieJarFullPath(self,path):
        """设置页面cookie文件的全路径

        Args:  
            path(str): 页面cookie文件的全路径

        设置cookie的全路径+文件名，如“c:\\mb\\cookie.dat”
        """
        return self.dll.wkeSetCookieJarFullPath(self.cId,path)


    ##############JS##############
    def getJsExec(self):
        return self.dll.wkeGlobalExec(self.cId)

    def runJsCode(self,js_code:str):
        """页面执行一段指定的js代码

        Args:   
            js_code(str):指定的js代码
        Returns:
            str: js代码执行结果
        """
        es=self.getJsExec()
        #闭包执行JS
        val=self.dll.wkeRunJSW(self.cId,js_code)
        val=self.dll.jsToStringW(es,val)
        if val=='undefined':
            val=None
        return val
  
    def runJsFile(self,file_name):
        """页面执行指定路径的文件内容中的js代码

        Args:   
            file_name(str or path):指定的文件路径
        Returns:
            str: js代码执行结果
        """
        with open(file_name) as f:
            js_code=f.read()
            return self.runJsCode(js_code)        
        
    def runJsFunc(self,funcName,paramList=[],thisValue=0):   
        """页面主frame执行js函数

        Args:   
            funcName(str): js函数名
            paramList(list): 参数列表
            this_func(BO)
        Returns:
            str: js代码执行结果

        TODO:
            NO VERIFY
        """
        es=self.getJsExec()
        if thisValue == 0:
            funcName=funcName.encode()
            #获取window上的属性
            func=self.dll.jsGetGlobal(es,funcName)
        else:
            pass

        argCount=len(paramList)
        argsList=(c_longlong *argCount)()

        for i,param in enumerate(paramList):
            if isinstance(param,str):
                param=self.dll.jsStringW(es,param)
            elif isinstance(param,int):
                param=self.dll.jsInt(c_longlong(param))
            elif isinstance(param,float):
                param=self.dll.jsFloat(param)
            elif isinstance(param,bool):
                param=self.dll.jsBoolean(param)
            argsList[i]=param
        #调用js
        #jsValue jsCall(jsExecState es, jsValue func, jsValue thisValue, jsValue* args, int argCount)
        #调用一个func对应的js函数。如果此js函数是成员函数，则需要填thisValue。 否则可以传jsUndefined。args是个数组，个数由argCount控制。 func可以是从js里取的，也可以是自行构造的。
        callRet=self.dll.jsCall(es,c_longlong(func),c_longlong(thisValue),byref(argsList),c_longlong(argCount))
        val=self.dll.jsToStringW(es,c_longlong(callRet))
        return val  
    
    def runJsByFrame(self,frameId,js_code,isInClosure=True):
        """页面指定frameId的frame上运行js

        Args:   
            frameId(int):   页面中帧ID
            js_code(str):   指定的js代码
            isInClosure(bool,optional): 是否在外层包个function() {}形式的闭包
        Returns:
            str: js代码执行结果

        NOTE：
            如果需要返回值，在isInClosure为true时，需要写return，为false则不用

        """
        js_code=js_code.encode()
        val=self.dll.wkeRunJsByFrame(self.cId,frameId,js_code,isInClosure)
        es = self.dll.wkeGetGlobalExecByFrame(self.cId, frameId)
        val=self.dll.jsToTempStringW(es, c_longlong(val))
        return val

    ##############SendEventMessage##############
    def fireMouseEvent(self,msg,x,y,flags=0):
        """向页面发送鼠标事件

        Args:
            message(wkeMouseMsg):   鼠标消息,取WkeConst.MK_LBUTTON等
            x(int):                 鼠标位置x坐标
            y(int):                 鼠标位置y坐标
            flags(wkeMouseFlags):   可取值有WKE_CONTROL、WKE_SHIFT、WKE_LBUTTON、WKE_MBUTTON、WKE_RBUTTON，可通过“或”操作并联。

        """
        
        return self.dll.wkeFireMouseEvent(self.cId,msg,x,y,flags)

    def fireMouseWheelEvent(self,msg,x,y,delta,flags=0):
        """向页面发送鼠标滚轮事件

        Args:
            message(wkeMouseMsg):   鼠标消息,取WkeConst.MK_LBUTTON等
            x(int):                 鼠标位置x坐标
            y(int):                 鼠标位置y坐标
            delta(int),             滚轮进度
            flags(wkeMouseFlags):   可取值有WKE_CONTROL、WKE_SHIFT、WKE_LBUTTON、WKE_MBUTTON、WKE_RBUTTON，可通过“或”操作并联。

        """
        
        return self.dll.wkeFireMouseWheelEvent(self.cId,msg,x,y,flags)
       
    def fireKeyDownEvent(self,virtualKeyCode,flags=0):
        """向页面发送键盘按下事件

        Args:
            virtualKeyCode(int):    键的字符代码。
            flags(wkeKeyFlags):     重复计数、扫描代码、扩展键标志、上下文代码、以前的键状态标志和转换状态标志
         
        Return:
            int: 如果应用程序处理此消息，则应返回零。

        WM_CHAR消息的The character code of the key.见https://msdn.microsoft.com/en-us/library/windows/desktop/ms646276(v=vs.85).aspx
        """
        return self.dll.wkeFireKeyDownEvent(self.cId,virtualKeyCode,flags,False)
    
    def fireKeyUpEvent(self,virtualKeyCode,flags=0):
        """向页面发送键盘弹起事件

        Args:
            virtualKeyCode(int):    键的字符代码。
            flags(wkeKeyFlags):     重复计数、扫描代码、扩展键标志、上下文代码、以前的键状态标志和转换状态标志
       
        Return:
            int: 如果应用程序处理此消息，则应返回零。
        """
        return self.dll.wkeFireKeyUpEvent(self.cId,virtualKeyCode,flags,False)
    
    def fireKeyPressEvent(self,virtualKeyCode,flags=0):
        """向页面发送键盘弹起事件

        Args:
            virtualKeyCode(int):    键的字符代码。
            flags(wkeKeyFlags):     重复计数、扫描代码、扩展键标志、上下文代码、以前的键状态标志和转换状态标志
        Return:
            int: 如果应用程序处理此消息，则应返回零。

        """
        return self.dll.wkeFireKeyPressEvent(self.cId,virtualKeyCode,flags,False)
    
    def fireWindowsMessage(self,msg,wParam,lParam):
        """向页面发送windows消息事件

        Args:
            msg(win32con):    消息
            wParam  :         消息参数
            lParam  :         消息参数  
        Return:
            int: 如果应用程序处理此消息，则应返回零。

        向mb发送任意windows消息。不过目前mb主要用来处理光标相关。mb在无窗口模式下，要响应光标事件，需要通过本函数手动发送光标消息

        """
        #byref(
        result = c_int(-1)
        self.dll.wkeFireWindowsMessage(self.cId,self.hwnd,msg,wParam,lParam,byref(result))
        return result.value

    ##############OnEvent##############
    def onAlertBox(self,param,*args,**kwargs):
        """ 设置网页调用alert的回调 """
        return Wke.event.onAlertBox(self,param,*args,**kwargs)
    def onConfirmBox(self,param,*args,**kwargs):
        """ 设置网页调用confirmBox的回调 """
        return Wke.event.onConfirmBox(self,param,*args,**kwargs)
    def onConsole(self,param,*args,**kwargs):
        """ 设置网页调用console触发的回调 """
        return Wke.event.onConsole(self,param,*args,**kwargs)
    def onCreateView(self,param,*args,**kwargs):
        """ 设置创建新窗口时的回调 """
        return Wke.event.onCreateView(self,param,*args,**kwargs)
    def onDocumentReady2(self,param,*args,**kwargs):
        """ 设置文档就绪时的函数 """
        return Wke.event.onDocumentReady2(self,param,*args,**kwargs)
    def onDownload(self,param,*args,**kwargs):
        """ 设置网页开始下载的回调 """
        return Wke.event.onDownload(self,param,*args,**kwargs)
    def onGetFavicon(self,param,*args,**kwargs):
        """ 设置获取favicon的回调 """
        return Wke.event.onGetFavicon(self,param,*args,**kwargs)
    def onLoadUrlBegin(self,param,*args,**kwargs):
        """ 设置网络请求发起前的回调 """
        return Wke.event.onLoadUrlBegin(self,param,*args,**kwargs)
    def onLoadUrlEnd(self,param,*args,**kwargs):
        """ 设置网络请求结束的回调 """
        return Wke.event.onLoadUrlEnd(self,param,*args,**kwargs)
    def onLoadUrlFail(self,param,*args,**kwargs):
        """ 设置网络请求失败的回调 """
        return Wke.event.onLoadUrlFail(self,param,*args,**kwargs)
    def onLoadUrlFinish(self,param,*args,**kwargs):
        """ 设置网络请求完成的回调 """
        return Wke.event.onLoadUrlFinish(self,param,*args,**kwargs)
    def onMouseOverUrlChanged(self,param,*args,**kwargs):
        """ 设置鼠标划过链接元素的回调 """
        return Wke.event.onMouseOverUrlChanged(self,param,*args,**kwargs)
    def onNavigation(self,param,*args,**kwargs):
        """ 设置网页开始浏览的回调 """
        return Wke.event.onNavigation(self,param,*args,**kwargs)
    def onNetResponse(self,param,*args,**kwargs):
        """ 设置收到网络请求的回调 """
        return Wke.event.onNetResponse(self,param,*args,**kwargs)
    def onPaintBitUpdated(self,param,*args,**kwargs):
        """  设置窗口绘制刷新时回调  """
        return Wke.event.onPaintBitUpdated(self,param,*args,**kwargs)
    def onPaintUpdated(self,param,*args,**kwargs):
        """  设置窗口绘制刷新时回调 """
        return Wke.event.onPaintUpdated(self,param,*args,**kwargs)
    def onPromptBox(self,param,*args,**kwargs):
        """ 设置网页调用PromptBox的回调 """
        return Wke.event.onPromptBox(self,param,*args,**kwargs)
    def onTitleChanged(self,param,*args,**kwargs):
        """ 设置标题变化的回调 """
        return Wke.event.onTitleChanged(self,param,*args,**kwargs)
    def onURLChanged2(self,param,*args,**kwargs):
        """ 设置标题变化的回调 """
        return Wke.event.onURLChanged2(self,param,*args,**kwargs)
    def onWindowClosing(self,param,*args,**kwargs):
        """  设置窗口关闭时回调   """
        return Wke.event.onWindowClosing(self,param,*args,**kwargs)
    def onWindowDestroy(self,param,*args,**kwargs):
        """  设置窗口销毁时回调 """
        return Wke.event.onWindowDestroy(self,param,*args,**kwargs)

        
class WebWindow(WebView):
    """Wke网页视图带窗口
    
    
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


        return
    
    def create(self,parent=0,x=0,y=0,width=480,height=320,_type=0):
        """创建一个带真实窗口的wkeWebView

        .. code:: c

            wkeWebView wkeCreateWebWindow(wkeWindowType type, HWND parent, int x, int y, int width, int height);

        Args:
            _type(int):          窗口类型

                ============================    =====    ============================
                WKE_WINDOW_TYPE_POPUP           0           普通窗口
                WKE_WINDOW_TYPE_TRANSPARENT     1           透明窗口。mb内部通过layer window实现
                WKE_WINDOW_TYPE_CONTROL         2           嵌入在父窗口里的子窗口。此时parent需要被设置  
                ============================    =====    ============================


        """
        self.cId = self.dll.wkeCreateWebWindow(_type,parent,x,y,width,height)
        self.type = _type
        
        self.x,self.y = x,y
        self.w,self.h = width,height
        return self.cId
    
    def build(self,hwnd,x=0,y=0,width=640,height=480,_type=2):
        """为一个真实窗口绑定一个wkeWebWindow

        Args:
            hwnd (int):         窗口句柄
            x (int):            窗口绑定区域左上角起始点的x坐标
            y (int):            y坐标
            width (int):        宽度
            height (int):       高度    
        """
        if hwnd==0:
            return 0
        
        self.cId = self.dll.wkeCreateWebWindow(2,hwnd,x,y,width,height)

        self.type = _type
        self.hwnd = hwnd
        #self.dll.wkeShowWindow(id,show)
        self.x,self.y = x,y
        self.w,self.h = width,height
        return
    
    def setWindow(self,_type=0,hwnd=0,x=0,y=0,width=360,height=480):
        self.type = _type
        self.hwnd = hwnd
        self.x = x 
        self.y = y
        self.w = width
        self.h = height
        return 
    


    def destroy(self):
        """销毁wkeWebView对应的所有数据结构，包括真实窗口等
        """
        self.dll.wkeDestroyWebWindow(self.cId)
        return 


    


    


