#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/8/6 20:27
# @Author : justin.郑 3907721@qq.com
# @File : main.py
# @desc :


import os

from raglink.rag.main import RAGLink
from dotenv import load_dotenv
load_dotenv()

# # 代理服务器地址和端口
# proxy_host = 'localhost'
# proxy_port = '7890'
#
# # 设置 HTTP 和 HTTPS 代理
# os.environ['http_proxy'] = f'http://{proxy_host}:{proxy_port}'
# os.environ['https_proxy'] = f'http://{proxy_host}:{proxy_port}'

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "ggg",
            "vector_size": 1536,
            # "partition_name": "abc",
            # "uri": os.getenv("MILVUS_URI"),
            # "api_key": os.getenv("MILVUS_TOKEN"),
            "host": "localhost",
            "port": 6333
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
            "api_key": os.getenv("MINIMAX_API_KEY"),
            "group_id": os.getenv("MINIMAX_GROUP_ID")
        }
    }
}
rag = RAGLink.from_config(config)
# print(rag.test())

# res = rag.execute_store("./data/aimdt.txt")
res = rag.get_context(question="14个的大型语言模型有哪些", limit=2)
print(res)