#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/8/6 20:27
# @Author : justin.郑 3907721@qq.com
# @File : main.py
# @desc :


import os
from dotenv import load_dotenv
load_dotenv()

from raglink.rag.main import RAGLink

# # 代理服务器地址和端口
# proxy_host = 'localhost'
# proxy_port = '7890'
#
# # 设置 HTTP 和 HTTPS 代理
# os.environ['http_proxy'] = f'http://{proxy_host}:{proxy_port}'
# os.environ['https_proxy'] = f'http://{proxy_host}:{proxy_port}'


config = {
    "vector_store": {
        "provider": "milvus",
        "config": {
            "collection_name": "dx_test_doubao",
            "vector_size": 2560,
            "partition_name": "0208",
            "host": "localhost",
            "port": 19530
        }
    },
    # "test_splitter": {
    #     "provider": "recursive_character",
    #     "config": {
    #         "chunk_size": 500,
    #         "chunk_overlap": 50
    #     }
    # },
    "test_splitter": {
        "provider": "separator",
    },
    "embedder": {
        "provider": "doubao",
        "config": {
            "api_key": os.getenv("DOUBAO_API_KEY"),
            "model": os.getenv("DOUBAO_EMDEDDINGS_MODLE"),
        }
    }
}
rag = RAGLink.from_config(config)
# print(rag.test())

# 执行存储文件
res = rag.execute_store("./data/电信问答1108.txt")
print(res)

# 执行修改存储数据
data = [{
    "id": 530098045657612940,
    "content": "测试修改功能001",
    "source": "测试.txt"
},{
    "id": 533534635482701198,
    "content": "测试修改功能002",
    "source": "测试.txt"
}]
res = rag.execute_update(docs=data)
print(res)

# data = [{
#     "content": "测试修改功能003",
#     "source": "测试.txt"
# }]
# res = rag.execute_insert(docs=data)
# print(res)
# 执行删除存储数据
# res = rag.execute_delete(ids=[4370365826046822406])
# print(res)

# 执行存储多文件
# res = rag.execute_store_batch("./data")

# 获取上下文信息
# res = rag.get_context(question="14个的大型语言模型有哪些", limit=2)
