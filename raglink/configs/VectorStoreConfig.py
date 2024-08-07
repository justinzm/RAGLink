#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 下午5:23
# @File    : VectorStoreConfig.py
# @desc    : 向量存储配置


from typing import Optional
from pydantic import BaseModel, Field, field_validator


class VectorStoreConfig(BaseModel):
    provider: str = Field(
        description="Provider of the vector store (e.g., 'qdrant', 'milvus')",
        default="qdrant",
    )
    config: Optional[dict] = Field(
        description="Configuration for the specific vector store",
        default={},
    )

    @field_validator("config")
    def validate_config(cls, v, values):
        provider = values.data.get("provider")
        if provider in ("qdrant", "milvus"):
            return v
        else:
            raise ValueError(f"Unsupported vector store provider: {provider}")