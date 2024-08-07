#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/6 上午9:32
# @File    : recursive_character.py
# @desc    : 递归字符分割


from raglink.utils.logger import logger
from raglink.test_splitter.base import TestSplitterBase
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RecursiveCharacterTextSplitter(TestSplitterBase):
    def __init__(
        self,
        chunk_size,
        chunk_overlap,
        separator=None,
        is_separator_regex=False
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.is_separator_regex = is_separator_regex

    def execute(self, file_content):
        if self.separator == None:
            self.separator = ["\n\n", "\n", " ", ""]
        text_split = RecursiveCharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=self.is_separator_regex
        )
        try:
            result = text_split.split_documents(file_content)
            logger.info(f"TextSplitter 执行 递归字符 切割文档，切割{len(result)}块")
        except Exception as e:
            logger.error(f"TextSplitter 执行 递归字符 切割文档失败，{e}")
        return result

