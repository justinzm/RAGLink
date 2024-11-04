#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/6/21 下午2:26
# @Author : justin.郑 3907721@qq.com
# @File : DocumentLoaders.py
# @desc : 文档加载类

"""
可加载格式为 txt、md、csv、xlsx、pdf、docx
"""

from raglink.utils.logger import logger
from langchain_community.document_loaders import (TextLoader,
                                                  UnstructuredExcelLoader,
                                                  PyPDFLoader,
                                                  Docx2txtLoader,
                                                  CSVLoader)


class DocumentLoaders:
    def __init__(self):
        self.loaders = {
            "txt": TextLoader,
            "md": TextLoader,
            "xlsx": UnstructuredExcelLoader,
            "pdf": PyPDFLoader,
            "docx": Docx2txtLoader,
            "csv": CSVLoader
        }

    def run(self, file_path):
        file_extension = file_path.split('.')[-1]
        loader_class = self.loaders.get(file_extension)
        if loader_class:
            try:
                if file_extension in ["pdf", "docx"]:
                    loader = loader_class(file_path)
                else:
                    loader = loader_class(file_path, encoding="utf-8")
                text = loader.load()
                logger.info(f"DocumentLoaders 成功加载{file_path}文件")
                return text
            except Exception as e:
                logger.error(f"DocumentLoaders 加载{file_path}文件失败，错误：{e}")
        else:
            logger.warning(f"DocumentLoaders 不支持的文件扩展名：{file_extension}")
            return None


if __name__ == "__main__":
    # file_path = "../data/iPhone14.txt"
    # file_path = "../data/loader.md"
    # file_path = "../data/fake.xlsx"
    # file_path = "../data/loader.csv"
    file_path = "../../data/电信问答.txt"
    res = DocumentLoaders().run(file_path)
    print(res)

