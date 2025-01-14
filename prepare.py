# -*- coding:utf-8 -*-

import platform,os,sys,getopt,time
from pathlib import Path
from pprint import pformat
import shutil 

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
tar_file = "wkeMiniblink/bin/miniblink.dll"

if bit == '64bit':
    dllName = "miniblink_4975_x64.dll"
else:
    dllName = "miniblink_4975_x32.dll"

def prepare():
    """
    制作安装包前,创建版本对应dll
    """
    print(f'Prepare [{tar_file}]')

    # 确保目标目录存在，如果不存在则创建
    if not os.path.exists(tar_dir):
        os.makedirs(tar_dir)

    if os.path.exists(tar_file):
        os.remove(tar_file)

    # 打开.zip文件并解压缩
    with zipfile.ZipFile(src_file, 'r') as zip_ref:
        tar_dll = zip_ref.extract(dllName,tar_dir)
        print(f'    文件 {src_file} 已成功解压缩到 {tar_dir} as [{tar_dll}]')

        shutil.move(tar_dll,tar_file)
        print(f'    文件 {tar_dll} =>{tar_file}')
    
    if os.path.exists("README.md"):
        os.remove("README.md")

    shutil.copyfile("documents/source/README.md","README.md")
    return

def clean():
    """
    """
    print(f'Clean [{tar_file}]')
    if os.path.exists(tar_file):
        os.remove(tar_file)
        print(f'    文件 {tar_file} 删除')
    return

if __name__=='__main__':
    argv = sys.argv
    argc = len(sys.argv)
    opt = 'prepare'

    if argc >= 2:
        opt = argv[1]
    
    if opt == 'prepare':
        prepare()
    elif opt == 'clean':
        clean()



 

