#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/2 下午4:40
# @File    : base.py
# @desc    : 向量数据库基类


from abc import ABC, abstractmethod


class VectorStoreBase(ABC):
    @abstractmethod
    def create_col(self, collection_name, vector_size, distance):
        """
        创建向量集合
        :param collection_name:
        :param vector_size:
        :param distance:
        :return:
        """
        pass

    @abstractmethod
    def insert(self, name, vectors, payloads=None, ids=None):
        """
        向集合中插入向量。
        :param name:
        :param vectors:
        :param payloads:
        :param ids:
        :return:
        """
        pass

    @abstractmethod
    def search(self, name, query, limit=5, filters=None):
        """
        搜索相似的向量。
        :param name:
        :param query:
        :param limit:
        :param filters:
        :return:
        """
        pass

    @abstractmethod
    def delete(self, name, vector_id):
        """
        按ID删除向量。
        :param name:
        :param vector_id:
        :return:
        """
        pass

    @abstractmethod
    def update(self, name, vector_id, vector=None, payload=None):
        """
        更新向量及其有效载荷。
        :param name:
        :param vector_id:
        :param vector:
        :param payload:
        :return:
        """
        pass

    @abstractmethod
    def get(self, name, vector_id):
        """
        按ID检索向量。
        :param name:
        :param vector_id:
        :return:
        """
        pass

    @abstractmethod
    def list_cols(self):
        """
        列出所有集合。
        :return:
        """
        pass

    @abstractmethod
    def delete_col(self, name):
        """
        删除集合。
        :param name:
        :return:
        """
        pass

    @abstractmethod
    def col_info(self, name):
        """
        获取关于集合的信息。
        :param name:
        :return:
        """
        pass

