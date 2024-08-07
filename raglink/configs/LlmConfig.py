#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 上午9:55
# @File    : LlmConfig.py
# @desc    : LLM配置文件


from typing import Optional
from pydantic import BaseModel, Field, field_validator


class LlmConfig(BaseModel):
    provider: str = Field(
        description="Provider of the LLM (e.g., 'minimax', 'openai')", default="openai"
    )
    config: Optional[dict] = Field(
        description="Configuration for the specific LLM", default={}
    )

    @field_validator("config")
    def validate_config(cls, v, values):
        provider = values.data.get("provider")
        if provider in ("openai", "minimax", "deepseek"):
            return v
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
