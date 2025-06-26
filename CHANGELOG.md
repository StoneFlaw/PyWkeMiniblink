

# V0.1

## 2025/02/16 v0.1.7
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

