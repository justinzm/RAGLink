#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/8/3 14:44
# @Author : justin.郑 3907721@qq.com
# @File : milvus.py
# @desc : Milvus 向量数据库操作


from raglink.utils.logger import logger
from raglink.vector_stores.base import VectorStoreBase
from langchain_core.documents import Document
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility


class Milvus():
    def __init__(
        self,
        collection_name,
        vector_size,
        partition_name,
        connections_name="default",
        host=None,
        port=None,
        uri=None,
        api_key=None
    ):
        """
        初始化 Milvus 向量数据库操作类
        :param collection_name:
        :param vector_size:
        :param partition_name:
        :param connections_name:
        :param host:
        :param port:
        :param uri:
        :param token:
        """
        self.collection_name = collection_name
        self.partition_name = partition_name
        if uri and api_key:
            # 连接Zilliz服务器
            connections.connect(
                connections_name,
                uri=uri,
                token=api_key
            )
            logger.info("MILVUS 连接远程数据库")
            self.is_local = False
        else:
            # 连接本地数据库
            connections.connect(connections_name, host=host, port=port)
            logger.info("MILVUS 连接本地数据库")
            self.is_local = True

        # 判断该集合是否存在
        if utility.has_collection(self.collection_name):
            self.client = Collection(self.collection_name)
            # 检查集合索引是否已经加载
            load_status = utility.load_state(self.collection_name)
            if str(load_status) == "NotLoad":
                self.client.load()
            logger.debug(f"Milvus {self.collection_name} 集合已存在载入该集合")
            self._create_partition(partition_name=partition_name, partition_description="")
        else:
            self.create_col(partition_name, vector_size)

    # 创建集合与索引
    def create_col(self, partition_name, vector_size, metric_type='L2'):
        """
            创建集合与索引
            :param name:                    集合分区名
            :param dimension:               向量维度
            :param metric_type:             默认 L2    L2距离(欧氏距离)是向量相似性度量方法，用于衡量向量之间的距离和相似度
            :return:
        """
        # --- 1. 创建集合 ---
        # CollectionSchema 类创建了一个集合模式 schema（纲要），并指定了集合的字段定义和描述信息。
        # 定义字段
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=255),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=30000),
            FieldSchema(name="content_vector", dtype=DataType.FLOAT_VECTOR, dim=vector_size),
        ]
        # 创建schema（纲要）
        schema = CollectionSchema(fields=fields, description="")

        #  创建集合 Collection 类创建了一个名为 collection 的集合对象，并传入集合名称和集合模式（纲要）。
        self.client = Collection(name=self.collection_name, schema=schema)
        logger.debug(f"Milvus 新建 {self.collection_name} 集合")

        # --- 2. 创建索引 ---
        # L2距离(欧氏距离)是向量相似性度量方法，用于衡量向量之间的距离和相似度。
        # params为设置索引的参数：较大的 nlist值有助于提高搜索速度，但会增加索引的内存消耗
        if self.is_local:
            index_params = {
                'metric_type': metric_type,
                'index_type': "IVF_FLAT",  # 倒排文件(Inverted File)的索引方法，适用于高维向量的相似性搜索。
                'params': {"nlist": 1024}
            }
        else:
            index_params = {
                'metric_type': metric_type,
                'index_type': "AUTOINDEX",  # index_type被设置为"AUTOINDEX"，表示使用自动索引
                'params': {}
            }
        # field_name 创建索引的字段名； index_params 索引参数； index_name 索引命名(可选)
        self.client.create_index(field_name='content_vector', index_params=index_params)
        logger.debug(f"Milvus 创建 {self.collection_name} 集合索引成功")
        # 加载集合到内存
        self.client.load()

        # 创建集合分区
        self._create_partition(partition_name=partition_name, partition_description="")

    # 创建集合分区
    def _create_partition(self, partition_name: str, partition_description: str=""):
        """
            创建集合分区
            :param partition_name:          分区名称
            :param partition_description:   分区描述
            :return:
        """
        if utility.has_partition(self.collection_name, partition_name):
            logger.debug(f"Milvus {partition_name}分区已经存在")
        else:
            # 创建分区 分区名称；分区描述
            partition = self.client.create_partition(
                partition_name=partition_name,
                description=partition_description
            )
            # 分区加载到内存
            partition.load()
            logger.debug(f"Milvus 创建 {partition_name} 分区成功")

    # 列出集合所有分区
    def list_cols(self):
        """
            列出集合所有分区。
            :return: 集合中所有分区
        """
        return self.client.partitions

    def col_info(self):
        """
        获取关于集合的信息。
        :param name:
        :return:
        """
        return self.client.list_collections

    def insert(self, embeddings, vectors):
        # 判断分区是否存在，不存在创建分区
        if self.client.has_partition(self.partition_name):
            newpart = self.client.partition(self.partition_name)
        else:
            self.create_partition(self.partition_name)
            newpart = self.client.partition(self.partition_name)

        if isinstance(vectors[0], Document):
            data_list = []
            for doc in vectors:
                data_list.append(
                    {
                        "source": doc.metadata.get("source"),
                        "content": doc.page_content,
                        "content_vector": embeddings.embed(doc.page_content)
                    }
                )
            newpart.insert(data=data_list)
            logger.debug(f"Milvus 分区中插入 {len(data_list)} 条数据完成")

    # 查询分区中的数据
    def search(self, query, limit=3):
        """
        查询分区中的数据
        :param query:           查询向量数据
        :param limit:           输出块数
        :return:
        """
        # 判断该集合中分区是否存在
        if self.client.has_partition(self.partition_name):
            newpart = self.client.partition(self.partition_name)
            # 分区中搜索数据
            res_search = newpart.search(
                data=[query],
                anns_field="content_vector",
                param={"metric_type": "L2"},
                output_fields=["content", "source"],
                limit=limit
            )
            logger.debug(f"Milvus 分区检索结构: {res_search}")
            result = []
            for v in res_search[0]:
                entity = v.entity
                result.append(
                    {
                        "id": entity.id,
                        "distance": entity.distance,
                        "source": entity.fields['source'],
                        "content": entity.fields['content'],
                    }
                )
            return result
        else:
            logger.warning(f"Milvus 该分区不存在，分区名：{self.partition_name}")

    # 删除集合
    def delete_col(self):
        """
            删除集合
            :return:
        """
        try:
            if utility.has_collection(self.collection_name):
                utility.drop_collection(self.collection_name)
                logger.info(f"Milvus 删除 {self.collection_name} 集合成功")
        except Exception as e:
            logger.error(f"Milvus 删除集合 失败: {str(e)}")

    # 删除集合分区
    def delete_partition(self, partition_name=None):
        """
            删除集合分区
            :param partition_name:          分区名称,默认None为初始化设置的分区名
            :return:
        """
        if partition_name is not None:
            self.partition_name = partition_name
        try:
            if utility.has_partition(self.collection_name, self.partition_name):
                self.client.release()
                self.client.drop_partition(self.partition_name)
                logger.info("Milvus 删除集合分区 成功")
        except Exception as e:
            logger.error(f"Milvus 删除集合分区 失败: {str(e)}")