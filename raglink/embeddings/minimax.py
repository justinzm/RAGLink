#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/6 下午3:49
# @File    : minimax.py
# @desc    :


from raglink.embeddings.base import EmbeddingBase
from langchain_community.embeddings import MiniMaxEmbeddings


class MinimaxEmbedding(EmbeddingBase):
    def __init__(self, api_key, group_id):
        self.api_key = api_key
        self.group_id = group_id

    def embed(self, text):
        embeddings = MiniMaxEmbeddings(minimax_api_key=self.api_key, minimax_group_id=self.group_id)
        return embeddings.embed_query(text)