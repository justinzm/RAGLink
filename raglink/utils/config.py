#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/7/23 下午4:30
# @File    : config.py
# @desc    : 获取系统全局参数

import json


class Config:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)

    def get_chat_model_config(self):
        return self.config_data['chat_model']

    def get_milvus_config(self):
        return self.config_data['milvus']

    def get_embeddings_config(self):
        return self.config_data['embeddings']

    def get_splitter_config(self):
        return self.config_data['splitter']

    def get_database_config(self):
        return self.config_data['vector_stores']

    def get_qdrant_config(self):
        return self.config_data['qdrant']

    def is_feature_enabled(self, feature_name):
        return self.config_data.get(feature_name, False)


# 使用环境变量来指定配置文件路径
import os
from dotenv import load_dotenv
load_dotenv()

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = Config(os.path.join(BASE_DIR, 'config.json'))



