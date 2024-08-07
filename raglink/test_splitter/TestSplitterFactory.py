#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/8/5 上午10:16
# @File    : TestSplitterFactory.py
# @desc    : LLM工厂类


from raglink.utils.tools import load_class


# LLM提供者名称到类名的映射
provider_to_class = {
    "character": "raglink.test_splitter.character.CharacterTestSplitter",
    "recursive_character": "raglink.test_splitter.recursive_character.RecursiveCharacterTextSplitter",
    "separator": "raglink.test_splitter.separator.SeparatorTestSplitter"
}


class TestSplitterFactory:
    def create(provider_name, config):
        class_type = provider_to_class.get(provider_name)
        if class_type:
            test_splitter_instance = load_class(class_type)
            return test_splitter_instance(**config)
        else:
            raise ValueError(f"Unsupported Test Splitter provider: {provider_name}")

