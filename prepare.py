# -*- coding:utf-8 -*-

import platform,os,sys,getopt,time
from pathlib import Path
from pprint import pformat
import shutil 
import json
import re

current_folder = Path(__file__).absolute().parent
os.chdir(str(current_folder))



import ctypes
import win32gui
from win32con import *
from ctypes import windll
import zipfile
from platform import architecture

bit=architecture()[0]

tar_dir = "wkeMiniblink/bin"
src_file = "res/miniblink.zip"


if bit == '64bit':
    dllName = "miniblink_4975_x64.dll"
else:
    dllName = "miniblink_4975_x32.dll"

def prepare():
    """
    制作安装包前,将res中压缩包中dll释放到wkeMiniblink/bin目录
    """
    
    # 打开.zip文件并解压缩
    with zipfile.ZipFile(src_file, 'r') as zip_ref:
        tar_dll = zip_ref.extract("miniblink_4975_x32.dll",tar_dir)
        print(f'    文件 {src_file} 已成功解压缩到 {tar_dir} as [{tar_dll}]')

    with zipfile.ZipFile(src_file, 'r') as zip_ref:
        tar_dll = zip_ref.extract("miniblink_4975_x64.dll",tar_dir)
        print(f'    文件 {src_file} 已成功解压缩到 {tar_dir} as [{tar_dll}]')
  
    return

def doc():
    """
    将当前根目录的README.md和CHANGELOG.md 拷贝到docs/source 以便生成最新的文档
    """
    shutil.copy2("README.md","docs/source/README.md")
    print(f'    文件 README.md    => docs/source/README.md')
    shutil.copy2("CHANGELOG.md","docs/source/CHANGELOG.md")  
    print(f'    文件 CHANGELOG.md =>docs/source/CHANGELOG.md')
    return

def strip_json_comments(json_string):
    """Remove C-style comments from JSON string."""
    def replace_with_space(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " * len(s)
        else:
            return s

    pattern = re.compile(
        r'//.*? $ |/\*.*?\*/', 
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replace_with_space, json_string)

def read_json_with_comment(name):
    ctypeTable = {}
    ctypeCommentTable = {}
    def strips(m):
        m = m.strip()
        m = m.strip("\"")
        return m
    if os.path.exists(name):
        with open(name,"r",encoding="utf-8") as f :  
            content = f.read()
            #ctypeTable = json.loads(strip_json_comments(content))
            lines = content.split("\n")
           
            for line in lines:
                line = line.strip('\t')
                i = line.find(":")
                j = line.rfind("\",")
                k = line.rfind("/*")

                p = strips(line[0:i])
                q = strips(line[i+1:j])
                m = strips(line[k:])

                if p =="":
                    continue

                if q!= "":
                    ctypeTable[p]=q

                if m !=',' and m !='' :
                    ctypeCommentTable[p]=m


    return ctypeTable,ctypeCommentTable
          
def read_json_without_comment(name):
    ctypeTable = {}
    if os.path.exists(name):
        with open(name,"r",encoding="utf-8") as f :  
             content = f.read()
             ctypeTable = json.loads(strip_json_comments(content))
    return ctypeTable

def translate():
    """
    把docs\\source\\wke.h中关于接口函数翻译成py声明
    依据docs\\source\\wke.h.json关于各种数据类型的转换规则
    """
    ctypeTable,ctypeCommentTable = read_json_with_comment("docs\\source\\wke.h.json")

    def translateCtype(c):
        if c not in ctypeTable:
            ctypeTable[c] = None
            #return f"☒{c}"
            raise SyntaxError(f"{c} not explain")
        
        if ctypeTable[c] is not None:
            return ctypeTable[c]
        return f"☒{c}" 

    with open("docs\\source\\wke.h","r",encoding="utf-8") as f :
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            m = line.find("(")
            n = line.rfind(")")
            if line[0:8] == "ITERATOR" and n > m  and m in[9,10]:
                content = line[m+1:n]
                count=int(line[8:m])
                
                #print(line[0:m],count,content)
                # 参数个数,返回值,函数名,参数1,,,参数N,注释
                words= content.split(",")
                if count != len(words) - 3 :
                    raise SyntaxError(f"Error process @ {line}")
   
                res = [words[0].strip(),"☒"]
                res[1] = translateCtype(res[0])
         
                args = []
                for w in words[2:-1]:
                    w = w.strip()
                    pos = w.rfind(" ")
                    if pos < 0 or pos >= len(w) - 1:
                        raise SyntaxError(f"Error process @ {line}")
                    a0,a1 = [w[0:pos],w[pos+1:]]
                    
                    a2 = translateCtype(a0)

                    args.append([a0,a1,a2])
  
                func = words[1].strip()
                explain = words[-1].strip()
                explain=explain.strip("\"")
                if explain!="":
                    explain = f"//{explain}"
   
                '''
                #生成wke.h.json
                #print(f"#{res[0]} {func}(")
                print(f"{res[1]} {func}(",end="")
                for a in args:
                    print(f"{a[2]} {a1}",end="")
                if explain != "":
                    print(f")//{explain}")
                else:
                    print(")")
                '''
               
                print(f"#{res[0]} {func}({(",".join(words[2:-1])).strip()}){explain}")
                
                c = []
                for a in args:
                    if a[2].startswith("CFUNCTYPE"):
                        print(f"#{a[0]} {a[2]} \n#{ctypeCommentTable[a[0]]}")
                        
                    c.append(a[2])

                print(f"{func} = mb.{func}\n{func}.argtypes = [",end="")
                print(f"{",".join(c)}]")

                if res[1]!="None":
                    print(f"{func}.restype = {res[1]}\n")
                else:
                    print("\n")


        msg = json.dumps(ctypeTable,ensure_ascii=False,indent=4)
        #fout = open("docs\\source\\wke.txt","w",encoding="utf-8")
        #fout.write(msg)
        #print(msg)
           
    return
def pth():
    """
    在python解释器的site-packages路径下生成pth文件,将当前目录的绝对路径写入,以便将其加入库搜索路径
    """
    current = os.path.dirname(__file__)

    pypth = os.path.dirname(sys.executable)
    
    sitpth = pypth +os.sep+"Lib\\site-packages"

    pthpth = sitpth+ os.sep+"wkeminiblink.pth"

    with open(pthpth,"w") as f:
        f.write(f"{current}")


    return

if __name__=='__main__':
    argv = sys.argv
    argc = len(sys.argv)

    opt = 'pth'

    optDict = {"prepare":prepare,"doc":doc,"translate":translate,"pth":pth}

    def help():
        for o  in optDict:
            print(f"{o}:{optDict[o].__doc__}")

    if argc >= 2:
        opt = argv[1]
    else:
        if opt not in optDict:
            help()
            sys.exit(-1)

    if opt in optDict:
        optDict[opt]()
    else:
        help()
    



 

