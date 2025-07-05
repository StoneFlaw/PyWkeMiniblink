

# V0.1



## 2025/07/05 v0.1.7

为prepare.py增加输出wke.h.json，以及输出MiniblinkInit函数声明的功能

调整wkeEvent.py中的回调函数中额外参数在**kwargs中，而不是*args中，避免32/64位下错乱不一致

### wkeGetString

wkeEvent.py中32位下wkeGetStringW(str)运行正常,但是64位会c函数内部读异常。

改为wkeGetString(str),然后做binary->str的解码

现在默认wkeString全部是utf8

### String/StingW

Miniblink文档中String对应utf8*而StringW对应utf16*

###  CFunctionType instance

32、64位模式下，函数argtypes与回调函数如果不一致时抛出

ctypes.ArgumentError: argument 2: TypeError: expected CFunctionType instance instead of CFunctionType

所以调整确认MiniblinkInit中的定义与WkeEvent中回调函数声明一直。

### wkeString参数类型

将只读wkeString 全翻译为c_char_p,方便ctypes自动转换字符串。

如果需要写入wkeString,就翻译为c_void_p (c_char_p自动翻译为None)

```
#wkeString:c_void_p,text:str
utf8 = text.encode(encoding)
l = len(utf8)
mb.wkeSetString(cast(wkeString,c_char_p),utf8,l)
```

wkePromptBoxCallback的最后一个参数为wkeString,需要作为传参返回,填入字符串。所以wkeString翻成c_void_p

### PromptBoxCallback的Py形参和返回值

正常情况下

```
typedef bool(WKE_CALL_TYPE*wkePromptBoxCallback)(wkeWebView webView, void* param, const wkeString msg, const wkeString defaultResult, wkeString result);
<<=>>
CFUNCTYPE(c_bool,_LRESULT,c_void_p,c_char_p,c_char_p,c_void_p)
```

​      原回调函数返回值为c_bool,为保持形参形式一致,不做按引用传参数带出返回值,取消形参result,而是python的返回值。

​      实际python回调函数返回值为Str(有字符串确定输入)/None(取消输入)

### Examples

Alert/Prompt/Confirm需要使用wkeEvent的回调函数额外实现相应的GUI及其返回值控制。增加examples下alert/prompt/confirm的示例文件。





## 2025/02/16 v0.1.7a
开始修复x64下兼容性问题。miniblink.py/MiniblinkInit()关于cdll中一些接口函数的省略了部分形参的声明，在32位下缺省为c_int,在x64下缺省c_int将与minibilink.dll不一致导致出错

            X86     X64
BOOL        1       1
CHAR        1       1
SHORT       2       2
INT         4       4
LONG        4       4
LONGLONG    4       4
FLOAT       4       4
DOUBLE      8       8
PRT         4       8

在x64系统中，HWND是窗口句柄的数据类型，用于标识窗口对象。它是一个64位长的整数

只是临时验证,并未完全修正

## 2025/02/16 v0.1.6
增加setup.cfg 配置
setup
增加wkeMiniblink/__pyinstaller/* 用于安装时注册pyinstaller的hook文件
调整wkeMiniblink/__init__.py 识别Pyinstaller打包为exe运行和基于解释器运行时加载默认DLL的路径



## 2025/02/03 v0.1.5

调整WkeWin32.py部分函数名

修正WkeWin32.py的定时器WkeTimer

添加WkeWin32.py的截屏WkeSnapShot

增加截屏和定时器的测试文件

## 2025/01/28 v0.1.4

更新github action

## 2025/01/28 v0.1.3

更新pypi上传

## 2025/01/27 v0.1.2

编写基本完成文档

## 2025/01/15 v0.1.1

完成基本功能

