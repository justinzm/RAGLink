# RAGLink

RAGLink是一个开源的Retrieval-Augmented Generation框架，旨在通过结合检索和大模型生成技术，提升自然语言处理任务的性能和效率。为用户提供了一个强大、灵活且易于扩展的开发环境。

## 🔑核心特性
- 检索增强：通过检索技术，框架能够快速从大量数据中检索相关信息，为生成任务提供上下文支持。
- 生成能力：集成了多种生成大模型，能够根据检索到的信息生成流畅、准确的文本。
- 模块化设计：采用模块化设计，便于开发者根据需求定制和扩展功能。

## 🗺️集成
### 向量数据库
- [x] Milvus
- [x] Qdrant

### Embeddings模型
- [x] OpenAIEmbeddings
- [x] MiniMaxEmbeddings
- [x] HuggingFaceEmbedding

### Reranker模型
- [ ] bce-embedding-base_v1

## 📚使用文档

### 安装说明
可以直接从终端中的pip命令安装RAGLink：
```
pip install raglink
```

### 基本用法

#### 配置 RAGLink
```python
from raglink import RAGLink

# 配置RAGLink
config = {
    ……
}

rag = RAGLink.from_config(config)
```

config 配置
```python
# 文档切分配置
# character：固定大小分块； separator：分隔符分块；recursive_character：递归字符分割
config = {
    ……
    "test_splitter": {
        "provider": "character",
        "config": {
            "chunk_size": 300,
            "chunk_overlap": 20
        }
    }    
    ……
}

# 向量模型配置
# openai：OpenAI的Embeddings模型；minimax：MiniMax的Embeddings模型；huggingface：HuggingFace的Embeddings模型
config = {
    ……
    "embedder": {
        "provider": "minimax",
        "config": {
            "api_key": ……,
            "group_id": ……
        }
    }   
    ……
}

# 向量数据库配置
# qdrant：Qdrant向量数据库；milvus：Milvus向量数据库
config = {
    ……
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "……",
            "vector_size": 1536,
            "host": "localhost",
            "port": 6333
        }
    }   
    ……
}

```

#### 文档向量化
```python

# 输入文档地址进行向量化
rag.execute_store(file_path=file_path)
```

#### 检索获取上下文

```python

# 输入查询语句进行检索获取上下文
result = rag.get_context(question=question, limit=limit)
```

## 版本更新

```angular2html
v0.0.3
新增HuggingFaceEmbedding

```