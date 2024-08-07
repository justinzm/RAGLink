#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 下午5:14
# @File    : VectorStoreFactory.py
# @desc    : 向量存储工厂类


from raglink.utils.tools import load_class


provider_to_class = {
    "qdrant": "raglink.vector_stores.qdrant.Qdrant",
    "milvus": "raglink.vector_stores.milvus.Milvus"
}


class VectorStoreFactory:
    def create(provider_name, config):
        class_type = provider_to_class.get(provider_name)
        if class_type:
            vector_store_instance = load_class(class_type)
            return vector_store_instance(**config)
        else:
            raise ValueError(f"Unsupported VectorStore provider: {provider_name}")