#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/8/11 13:51
# @Author : justin.郑 3907721@qq.com
# @File : huggingface.py
# @desc : HuggingFace Embeddings


from raglink.embeddings.base import EmbeddingBase
from langchain_huggingface import HuggingFaceEmbeddings


class HuggingFaceEmbedding(EmbeddingBase):
    def __init__(self, model_name):
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'batch_size': 64, 'normalize_embeddings': True}

        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

    def embed(self, text):
        return self.embeddings.embed_query(text)

