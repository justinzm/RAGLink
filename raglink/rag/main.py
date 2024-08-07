#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 上午9:46
# @File    : main.py
# @desc    :


from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ValidationError

from raglink.utils.logger import logger
from raglink.rag.DocumentLoaders import DocumentLoaders

from raglink.embeddings.EmbedderFactory import EmbedderFactory
from raglink.vector_stores.VectorStoreFactory import VectorStoreFactory
from raglink.test_splitter.TestSplitterFactory import TestSplitterFactory

from raglink.configs.VectorStoreConfig import VectorStoreConfig
from raglink.configs.TestSplitterConfig import TestSplitterConfig
from raglink.configs.EmbedderConfig import EmbedderConfig


class RAGConfig(BaseModel):
    vector_store: VectorStoreConfig = Field(
        description="Configuration for the vector store",
        default_factory=VectorStoreConfig,
    )
    test_splitter: TestSplitterConfig = Field(
        description="Configuration for the test splitter",
        default_factory=TestSplitterConfig,
    )
    embedder: EmbedderConfig = Field(
        description="Configuration for the embedding model",
        default_factory=EmbedderConfig,
    )


class RAGLink:
    def __init__(self, config: RAGConfig = RAGConfig()):
        self.config = config
        self.vector_store = VectorStoreFactory.create(self.config.vector_store.provider,
                                                      self.config.vector_store.config)
        self.test_splitter = TestSplitterFactory.create(self.config.test_splitter.provider,
                                                       self.config.test_splitter.config)
        self.embedding_model = EmbedderFactory.create(self.config.embedder.provider,
                                                      self.config.embedder.config)

    @classmethod
    def from_config(cls, config_dict: Dict[str, Any]):
        try:
            config = RAGConfig(**config_dict)
        except ValidationError as e:
            logger.error(f"Configuration validation error: {e}")
            raise
        return cls(config)

    # 执行向量数据存储
    def execute_store(self, file_path):
        # 1. 获取加载内容
        file_content = DocumentLoaders().run(file_path=file_path)

        # 2. 对加载内容进行切割
        docs = self.test_splitter.execute(file_content=file_content)

        # 3. 向量化与向量存储
        result = self.vector_store.insert(embeddings=self.embedding_model, vectors=docs)
        return result

    # 获取上下文信息
    def get_context(self, question, limit=3):
        question_vector = self.embedding_model.embed(question)
        return self.vector_store.search(query=question_vector, limit=limit)



