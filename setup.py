#coding:utf-8

import platform,os,sys,getopt,time
import traceback
import copy

from pkg_resources import Requirement, resource_filename
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    #自动搜索包含__init__.py的文件夹
    packages=find_packages(exclude=["dist.*", "dist", "tests.*", "tests","__pycache__/*"]),
    package_data={
        "wkeMiniblink": ["bin/*.dll"]#包含指定包下相对目录的匹配文件                 
    },


    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={
        'Documentation': 'https://pywkeminiblink.readthedocs.io/zh-cn/latest/',
        'Source Code': 'https://github.com/StoneFlaw/PyWkeMiniblink',
        'Bug Tracker': 'https://github.com/StoneFlaw/PyWkeMiniblink/issues',
        'Homepage': 'https://pypi.org/project/WkeMiniblink/',
    }
    # could also include long_description, download_url, classifiers, etc.
)