#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/6 上午11:19
# @File    : separator.py
# @desc    : 分隔符分块



import re
from langchain_core.documents import Document
from raglink.utils.logger import logger
from raglink.test_splitter.base import TestSplitterBase


class SeparatorTestSplitter(TestSplitterBase):
    def __init__(
        self,
        separator=None,
        chunk_size=None,
        chunk_overlap=None,
        is_separator_regex=False
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.is_separator_regex = is_separator_regex

    def execute(self, file_content):
        if self.separator == None:
            self.separator = "\n\n"
        try:
            tmp = file_content[0].page_content
            result = self.specialized_chunking(file_content[0].page_content, self.separator, file_content[0].metadata["source"])
            logger.info(f"TextSplitter 执行 分隔符 切割文档，切割{len(result)}块")
            return result
        except Exception as e:
            logger.error(f"TextSplitter 执行 分隔符 切割文档失败，{e}")


    def specialized_chunking(self, text, separator, source):
        """
        专门的分块函数，根据特定的分隔符将文本分割成块
        :param text: 输入文本
        :param delimiter: 分隔符，用于定义分块的边界
        :return: 分割后的文本块列表
        """
        # 使用正则表达式根据特定分隔符分割文本
        chunks = re.split(separator, text)
        # 去除空块
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        # list转换为Document格式
        result = []
        for chunk in chunks:
            result.append(
                Document(
                    page_content=chunk,
                    metadata={"source": source}
                )
            )
        return result


