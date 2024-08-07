#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/6 上午9:19
# @File    : base.py
# @desc    : 分块器基类


from abc import ABC, abstractmethod


class TestSplitterBase(ABC):
    @abstractmethod
    def execute(self, file_content):
        """
        执行分块操作
        :param file_content: 文件内容
        :return: 生成的分块内容
        """
        pass


