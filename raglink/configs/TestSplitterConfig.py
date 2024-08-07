#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 下午5:23
# @File    : TestSplitterConfig.py
# @desc    : 文本切割配置


from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TestSplitterConfig(BaseModel):
    provider: str = Field(
        description="Provider of the test splitter (e.g., 'character', 'recursive_character', 'separator')",
        default="character",
    )
    config: Optional[dict] = Field(
        description="Configuration for the specific test splitter",
        default={},
    )

    @field_validator("config")
    def validate_config(cls, v, values):
        provider = values.data.get("provider")
        if provider in ("character", "recursive_character", "separator"):
            return v
        else:
            raise ValueError(f"Unsupported test splitter provider: {provider}")