#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/2 下午4:50
# @File    : qdrant.py
# @desc    : Qdrant 向量数据库操作


import os
import uuid
import shutil

from qdrant_client import QdrantClient, models
from langchain_core.documents import Document

from raglink.utils.logger import logger
from raglink.vector_stores.base import VectorStoreBase


class Qdrant(VectorStoreBase):
    def __init__(
        self,
        collection_name="raglink",
        vector_size=1536,
        client=None,
        host=None,
        port=None,
        path=None,
        url=None,
        api_key=None,
    ):
        """
        初始化 Qdrant 向量数据库操作类
        :param collection_name:                         向量集合名称
        :param vector_size:                             向量维度
        :param client (QdrantClient, optional):         Qdrant实例对象
        :param host (str, optional):                    Qdrant本地服务器的主机地址。默认为“localhost”。
        :param port (int, optional):                    Qdrant本地服务器的端口。默认为6333。
        :param path (str, optional):                    Qdrant本地数据库的路径。默认为None。
        :param url (str, optional):                     Qdrant远程服务器的完整URL。默认为None。
        :param api_key (str, optional):                 Qdrant远程服务器的API密钥。默认为None。
        """
        if client:
            self.client = client
        else:
            params = {}
            if path:
                params["path"] = path
                if os.path.exists(path) and os.path.isdir(path):
                    shutil.rmtree(path)
            if api_key:
                params["api_key"] = api_key
            if url:
                params["url"] = url
            if host and port:
                params["host"] = host
                params["port"] = port
            self.client = QdrantClient(**params)
        self.collection_name = collection_name
        self.create_col(collection_name, vector_size)

    def create_col(self, name, vector_size, distance=models.Distance.COSINE):
        """
        创建向量集合
        :param collection_name: 向量集合名称
        :param vector_size:     向量维度
        :param distance:        向量之间相似度的距离度量方法 COSINE: 余弦相似度; EUCLID: 欧几里得距离; DOT: 点积
        :return:
        """
        # 如果已经存在，则跳过创建集合
        response = self.list_cols()
        for collection in response.collections:
            if collection.name == name:
                logger.debug(f"集合 {name} 已经存在. 跳过创建")
                return

        self.client.create_collection(
            collection_name=name,
            vectors_config=models.VectorParams(size=vector_size, distance=distance),
        )
        logger.debug(f"创建新集合 {name} 成功")

    def insert(self, embeddings, vectors, payloads=None, ids=None):
        """
        向集合中插入向量
        :param vectors:             向量列表  [[1,2,3,4], [2,3,4,5]]
        :param payloads:            与向量对应的有效载荷列表
        :param ids:                 与向量对应的ID列表
        :return:
        """
        if isinstance(vectors[0], Document):
            points = []
            for doc in vectors:
                points.append(
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embeddings.embed(doc.page_content),
                        payload={
                            "page_content": doc.page_content,
                            "metadata": {
                                "source": doc.metadata['source']
                            }
                        }
                    )
                )
        else:
            points = [
                models.PointStruct(
                    id=idx if ids is None else ids[idx],
                    vector=vector,
                    payload=payloads[idx] if payloads else {},
                )
                for idx, vector in enumerate(vectors)
            ]
        result = self.client.upsert(collection_name=self.collection_name, points=points)
        if result.status == "completed":
            logger.debug(f"成功插入 {len(points)} 个向量进入Qdrant向量数据库")
            return result.status
        else:
            logger.error(f"插入向量失败: {result}")

    def _create_filter(self, filters):
        """
        Create a Filter object from the provided filters.

        Args:
            filters (dict): Filters to apply.

        Returns:
            Filter: The created Filter object.
        """
        conditions = []
        for key, value in filters.items():
            if isinstance(value, dict) and "gte" in value and "lte" in value:
                conditions.append(
                    models.FieldCondition(
                        key=key, range=models.Range(gte=value["gte"], lte=value["lte"])
                    )
                )
            else:
                conditions.append(
                    models.FieldCondition(key=key, match=models.MatchValue(value=value))
                )
        return models.Filter(must=conditions) if conditions else None

    def search(self, query, limit=5, filters=None):
        """
        搜索相似向量数据
        :param query:   查询向量
        :param limit:   返回结果数量
        :param filters: 过滤器
        :return:    返回结果
        """
        query_filter = self._create_filter(filters) if filters else None
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query,
            query_filter=query_filter,
            limit=limit,
        )
        result = []
        for v in hits:
            result.append(
                {
                    "id": v.id,
                    "score": v.score,
                    "source": v.payload['metadata']['source'],
                    "content": v.payload['page_content'],
                }
            )
        return result

    def delete(self, vector_id):
        """
        按ID删除向量。
        :param name:        集合名称
        :param vector_id:   向量ID
        """
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[vector_id],
            ),
        )

    def update(self, vector_id, vector=None, payload=None):
        """
        更新矢量及其有效载荷。
        :param name:        集合名称
        :param vector_id:   向量ID
        :param vector:      向量
        :param payload:     有效载荷
        """
        point = models.PointStruct(id=vector_id, vector=vector, payload=payload)
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def get(self, vector_id):
        """
        按ID检索向量。
        :param vector_id:   向量ID
        :return:        dict 返回向量
        """
        result = self.client.retrieve(
            collection_name=self.collection_name, ids=[vector_id]
        )
        return result[0] if result else None

    def list_cols(self):
        """
        列出所有集合
        Returns:
            list: List of collection names.
        """
        return self.client.get_collections()

    def delete_col(self):
        """
        删除集合
        """
        self.client.delete_collection(collection_name=self.collection_name)

    def col_info(self):
        """
        获取关于集合的信息。
        :return:    dict 集合信息
        """
        return self.client.get_collection(collection_name=self.collection_name)

    def list(self, filters=None, limit=100):
        """
        列出集合中的所有向量
        :param filters: 过滤器
        :param limit:   返回结果数量
        :return:    list 返回向量列表
        """
        query_filter = self._create_filter(filters) if filters else None
        result = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=query_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )
        return result
