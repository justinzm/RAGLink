#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/6 下午1:50
# @File    : EmbedderFactory.py
# @desc    :


from raglink.utils.tools import load_class


class EmbedderFactory:
    provider_to_class = {
        "openai": "raglink.embeddings.openai.OpenAIEmbedding",
        "minimax": "raglink.embeddings.minimax.MinimaxEmbedding",
        "huggingface": "raglink.embeddings.huggingface.HuggingFaceEmbedding"
    }

    @classmethod
    def create(cls, provider_name, config):
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            embedder_instance = load_class(class_type)
            return embedder_instance(**config)
        else:
            raise ValueError(f"Unsupported Embedder provider: {provider_name}")