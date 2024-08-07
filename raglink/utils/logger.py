#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/7/23 上午10:40
# @Author : justin.郑 3907721@qq.com
# @File : logger.py
# @desc : 设置日志

import os
from loguru import logger

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 定义日志目录路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')


def setup_logger():
    logger.add(os.path.join(LOG_DIR, "log_file.log"), rotation="3 day", level="WARNING")


setup_logger()
