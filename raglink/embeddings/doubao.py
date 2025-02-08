#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2025/2/7 21:19
# @File    : doubao
# @desc    : 豆包 Embedding

from openai import OpenAI
from raglink.embeddings.base import EmbeddingBase


class DouBaoEmbedding(EmbeddingBase):
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    def embed(self, text):
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://ark.cn-beijing.volces.com/api/v3",
        )

        resp = client.embeddings.create(
            model=self.model,
            input=[text],
            encoding_format="float"
        )
        return resp.data[0].embedding