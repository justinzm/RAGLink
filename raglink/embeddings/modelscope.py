#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2025/6/6 21:46
# @File    : modelscope
# @desc    :

import os
from raglink.embeddings.base import EmbeddingBase
from langchain_community.embeddings import ModelScopeEmbeddings


class ModelScopeEmbedding(EmbeddingBase):
    def __init__(self, model_name, model_cache=None):
        if model_cache is not None or model_cache != "":
            os.environ["MODELSCOPE_CACHE"] = model_cache
        self.embeddings = ModelScopeEmbeddings(model_id=model_name)

    def embed(self, text):
        return self.embeddings.embed_query(text)