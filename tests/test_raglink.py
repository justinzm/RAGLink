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
            "host": "localhost",
            "port": 19530
        }
    },
    "test_splitter": {
        "provider": "separator",
        "config": {
            "chunk_size": 300,
            "chunk_overlap": 20,
            "separator": "\n\n"
        }
    },
    "embedder": {
        "provider": "minimax",
        "config": {
            "api_key": "……",
            "group_id": "……",
        }
    }
}
rag = RAGLink.from_config(config)

# ==========================================================================================
# 连接数据库 -- 创建集合 -- 创建分区 -- 加载文件 -- 切割文档 -- 提取向量 -- 存储向量
# 01-1 执行存储文件
# res = rag.execute_store("./data/电信问答.txt")
# 返回内容  执行向量数据存储完成

# 01-2 执行存储多文件
# res = rag.execute_store_batch("./data")


# ============================================================================================
# 执行修改存储数据
# data = [{
#     "id": 572621183905572102,
#     "content": "测试修改功能008",
#     "source": "测试0.txt"
# },{
#     "id": 610785405634847615,
#     "content": "测试修改功能009",
#     "source": "测试0.txt"
# }]
# res = rag.execute_update(docs=data)
# print(res)
# 返回内容  {'delete_count': 2, 'err_count': 0, 'err_index': [], 'insert_count': 2, 'primary_keys': [572621183905572102, 610785405634847615], 'upsert_count': 2, 'succ_count': 2, 'data': [{'id': 572621183905572102, 'source': '测试0.txt', 'content': '测试修改功能008'}, {'id': 610785405634847615, 'source': '测试0.txt', 'content': '测试修改功能009'}]}

# ============================================================================================
# 执行插入新数据
# data = [{
#     "content": "测试修改功能006",
#     "source": "测试0.txt"
# }]
# res = rag.execute_insert(docs=data)
# print(res)
# 返回内容 {'insert_count': 1, 'insert_ids': [2698265309713741189], 'err_count': 0, 'delete_count': 0, 'upsert_count': 0, 'succ_count': 1, 'data': [{'id': 2698265309713741189, 'source': '测试0.txt', 'content': '测试修改功能006'}]}

# ============================================================================================
# 执行删除数据
# res = rag.execute_delete([572621183905572102, 610785405634847615])
# print(res)
# 返回内容 (insert count: 0, delete count: 2, upsert count: 0, timestamp: 0, success count: 0, err count: 0)

# ============================================================================================
# 检索获取上下文
res = rag.get_context(question="查询家里宽带上网方式", limit=2)
print(res)
# 返回内容 [{'id': 1069900184029894104, 'distance': 0.10989413410425186, 'source': './data/电信问答1108.txt', 'content': '问：怎么查询家里宽带上网方式？\n答：您好，如您每次上网都需要点击“宽带连接”说明您是拨号上网，如您开机就可以直接上网说明您是通过路由器上网。'}, {'id': 3813237093392673733, 'distance': 0.619199275970459, 'source': './data/电信问答1108.txt', 'content': '问：什么是单宽带？\n答：您好，单宽带就是只开通宽带一种业务。'}]
