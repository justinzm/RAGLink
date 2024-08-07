#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/6 下午1:41
# @File    : openai.py
# @desc    :

from raglink.embeddings.base import EmbeddingBase
from langchain_openai.embeddings import OpenAIEmbeddings


class OpenAIEmbedding(EmbeddingBase):
    def __init__(self, api_key, model="text-embedding-3-small"):
        self.api_key = api_key
        self.model = model

    def embed(self, text):
        embeddings = OpenAIEmbeddings(api_key=self.api_key, model=self.model)
        return embeddings.embed_query(text)

