#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 上午9:46
# @File    : main.py
# @desc    :


import os
import uuid
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
        self.embedding_model = EmbedderFactory.create(self.config.embedder.provider,
                                                      self.config.embedder.config)
        self.vector_store = VectorStoreFactory.create(self.config.vector_store.provider,
                                                      self.config.vector_store.config)
        self.test_splitter = TestSplitterFactory.create(self.config.test_splitter.provider,
                                                       self.config.test_splitter.config)

    @classmethod
    def from_config(cls, config_dict: Dict[str, Any]):
        try:
            config = RAGConfig(**config_dict)
        except ValidationError as e:
            logger.error(f"Configuration validation error: {e}")
            raise
        return cls(config)

    # 执行向量数据存储,单文件
    def execute_store(self, file_path):
        """
        执行向量数据存储
        :param file_path: 单文件地址
        :return:    list
        """
        logger.info(f"执行文档 {file_path}")
        # 1. 获取加载内容
        file_content = DocumentLoaders().run(file_path=file_path)

        # 2. 对加载内容进行切割
        docs = self.test_splitter.execute(file_content=file_content)

        # 2.1 给加载内容添加ID号
        for doc in docs:
            doc.id = int(uuid.uuid4().int % (2**63))

        # 3. 向量化与向量存储
        result_vector = self.vector_store.insert(docs=docs, embeddings=self.embedding_model)

        id_set = set(result_vector['insert_ids'])
        result = []
        for doc in docs:
            if doc.id in id_set:
                result.append({
                    "id": doc.id,
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })

        logger.debug(f"执行向量数据存储完成: {file_path}")
        return result

    # 执行向量数据存储,文件夹地址 多文件
    def execute_store_files(self, directory):
        """
        执行向量数据存储
        :param directory: 文件夹地址
        :return:    list
        """
        file_paths = []  # 用于存储文件路径的列表
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        result_list = []
        for file_path in file_paths:
            res_list = self.execute_store(file_path)
            result_list.extend(res_list)
        return result_list

    # 修改向量数据   auto_id=True 时需要换成delete insert方式
    def execute_update(self, docs, is_embeddings=True):
        """
        修改向量数据
        :param docs:            list结构 需要包含ID 、source、content数据
        :param is_embeddings:   是否使用向量模型 True:使用 False:不使用（已定义向量数据）
        :return:
        """
        if is_embeddings:
            result_vector = self.vector_store.upsert(docs=docs, embeddings=self.embedding_model)
        else:
            result_vector = self.vector_store.upsert(docs=docs, embeddings=None)
        return result_vector

    # 插入向量数据
    def execute_insert(self, docs, is_embeddings=True):
        """
        插入向量数据
        :param docs:             list结构 需要包含ID 、source、content数据
        :param is_embeddings:    是否使用向量模型 True:使用 False:不使用（已定义向量数据）
        :return:
        """
        if is_embeddings:
            result_vector = self.vector_store.insert(docs=docs, embeddings=self.embedding_model)
        else:
            result_vector = self.vector_store.insert(docs=docs, embeddings=None)
        return result_vector


    # 删除向量数据
    def execute_delete(self, ids):
        """
        删除向量数据
        :param ids:            list结构 需要包含ID
        :return:
        """
        result_vector = self.vector_store.delete(ids=ids)
        return result_vector


    # ================================================================================
    # 获取上下文信息
    def get_context(self, question, limit=3):
        question_vector = self.embedding_model.embed(question)
        return self.vector_store.search(query=question_vector, limit=limit)



