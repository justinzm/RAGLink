#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/9/11 10:31
# @File    : milvus_test
# @desc    :

import os
from dotenv import load_dotenv
load_dotenv()
from pymilvus import MilvusClient

uri=os.getenv("MILVUS_URI_EN"),
token=os.getenv("MILVUS_TOKEN_EN")

client = MilvusClient(
    uri=uri,
    token=token, # replace this with your token
    db_name="default"
)

print(client)