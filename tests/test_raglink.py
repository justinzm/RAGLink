#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/7 下午5:31
# @File    : test_raglink.py
# @desc    : 测试 RAGLink


from raglink import RAGLink


config = {
    "vector_store": {
        "provider": "milvus",
        "config": {
            "collection_name": "……",
            "vector_size": 1536,
            "partition_name": "……",
            "uri": "……",
            "api_key": "……",
        }
    },
    "test_splitter": {
        "provider": "character",
        "config": {
            "chunk_size": 300,
            "chunk_overlap": 20
        }
    },
    "embedder": {
        "provider": "minimax",
        "config": {
            "api_key": "……",
            "group_id": "……"
        }
    }
}
# 配置 RAGLink
rag = RAGLink.from_config(config)

# 加载文档向量化存储
rag.execute_store("……")

# 检索获取上下文
rag.get_context(question="……", limit=2)


