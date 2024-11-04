#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/8/3 17:41
# @Author : justin.郑 3907721@qq.com
# @File : setup.py
# @desc :

from setuptools import find_packages, setup
import os

URL = 'https://github.com/justinzm/RAGLink'
NAME = 'RAGLink'
VERSION = '0.0.6'
DESCRIPTION = 'RAGLink是一个开源的Retrieval-Augmented Generation框架，旨在通过结合检索和大模型生成技术，提升自然语言处理任务的性能和效率。为用户提供了一个强大、灵活且易于扩展的开发环境。'
if os.path.exists('README.md'):
    with open('README.md', encoding='utf-8') as f:
        LONG_DESCRIPTION = f.read()
else:
    LONG_DESCRIPTION = DESCRIPTION
AUTHOR = 'Justin ZM'
AUTHOR_EMAIL = '3907721@qq.com'
LICENSE = 'MIT'
PLATFORMS = [
    'all',
]
REQUIRES = [
    'langchain==0.2.5',
    'langchain-community==0.2.5',
    'langchain-openai==0.1.8',
    'loguru==0.7.2',
    'pymilvus==2.4.1',
    'python-dotenv==1.0.1',
    'unstructured==0.15.0',
    'openpyxl==3.1.5',
    'python-magic==0.4.27',
    'qdrant-client==1.10.1',
    'docx2txt==0.8'
]
# CONSOLE_SCRIPT = 'my-cmd=my_pkg.my_cmd:main'
# # 如果想在 pip install 之后自动生成一个可执行命令，就靠它了:
# # <command>=<package_name>.<python_file_name>:<python_function>
# # 值得注意的是：
# # python_file_name 是不能用"-"的，需要用"_"，但 command 可以用"-"
# # my_cmd.py 也很简单，正常写即可，方法名也不一定是 main

# 需要的信息就在 setup() 中加上，不需要的可以不加
setup(
    name=NAME,
    version=VERSION,
    description=(
        DESCRIPTION
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=find_packages(),
    platforms=PLATFORMS,
    url=URL,
    install_requires=REQUIRES,
)
