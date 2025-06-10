#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/8/11 13:51
# @Author : justin.郑 3907721@qq.com
# @File : huggingface.py
# @desc : HuggingFace Embeddings

import os
from raglink.embeddings.base import EmbeddingBase
from sentence_transformers import SentenceTransformer


class HuggingFaceEmbedding(EmbeddingBase):
    def __init__(self, model_name, model_cache=None):
        if model_cache is not None or model_cache != "":
            os.environ["SENTENCE_TRANSFORMERS_HOME"] = model_cache
        self.embeddings = SentenceTransformer(model_name)

    def embed(self, text):
        return self.embeddings.encode(text)

