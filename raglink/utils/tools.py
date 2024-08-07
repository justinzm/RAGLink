#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 下午5:10
# @File    : tools.py
# @desc    :


import importlib


def load_class(class_type):
    # 将这个字符串分割为模块路径和类名两部分
    module_path, class_name = class_type.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

