#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/6 下午1:31
# @File    : EmbedderConfig.py
# @desc    : Embedding配置文件


from typing import Optional
from pydantic import BaseModel, Field, field_validator


class EmbedderConfig(BaseModel):
    provider: str = Field(
        description="Provider of the embedding model (e.g., 'openai', 'minimax')",
        default="openai",
    )
    config: Optional[dict] = Field(
        description="Configuration for the specific embedding model", default=None
    )

    @field_validator("config")
    def validate_config(cls, v, values):
        provider = values.data.get("provider")
        if provider in ["openai", "minimax"]:
            return v
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")