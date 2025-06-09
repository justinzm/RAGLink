#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2025/6/6 21:46
# @File    : modelscope
# @desc    :

from modelscope.models import Model
from raglink.embeddings.base import EmbeddingBase
from langchain_community.embeddings import ModelScopeEmbeddings


class ModelScopeEmbedding(EmbeddingBase):
    def __init__(self, model_id=None, model_path=None):
        if model_id is not None:
            self.embeddings = ModelScopeEmbeddings(model_id=model_id)
        if model_path is not None:
            model = Model.from_pretrained(model_path)
            self.embeddings = ModelScopeEmbeddings(model=model)

    def embed(self, text):
        return self.embeddings.embed_query(text)