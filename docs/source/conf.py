# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PyWkeMiniblink'
copyright = '2025, moonlake_w'
author = 'moonlake_w'
release = '0.1.1'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
import os
import sys
sys.path.insert(0, os.path.abspath(r'../../'))

extensions = ['sphinx.ext.autodoc', 
    #'sphinx_better_include',  # 引入 sphinx-better-include 插件
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',#支持numpy和google风格的docstrings
    'sphinx.ext.autosummary',
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",#对TODO项的支持
    'sphinx.ext.githubpages',#在GitHub页面中发布HTML文档
    #'sphinx.ext.linkcode',# 向源代码添加外部链接
    'recommonmark']

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# Napoleon settings
napoleon_google_docstring = True


#打开TODO词条
todo_include_todos = True

autodoc_mock_imports = ['windll']