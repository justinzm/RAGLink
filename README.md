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
- [x] ModelScopeEmbedding
- [x] OpenAIEmbedding
- [x] MiniMaxEmbedding
- [x] DouBaoEmbedding
- [x] HuggingFaceEmbedding

### Reranker模型
- [x] bce-embedding-base_v1



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
    "vector_store": ……,
    "test_splitter": ……,
    "embedder": ……,
}

rag = RAGLink.from_config(config)
```

#### config 配置

##### 1. 向量数据库配置

milvus：Milvus向量数据库；qdrant：Qdrant向量数据库

```
config = {
    ……
    "vector_store": {
        "provider": "milvus",
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

向量维度   如：doubao embedding  2048；minimax embedding  1536；openai text-embedding-3-small 512

**Milvus向量数据库**

可设置参数：

provider : "milvus"	数据库名称

config ：

- collection_name		集合名称
- vector_size                         向量维度
- partition_name                 分区名称
- connections_name          连接名称 默认：default
- host                                    连接地址  默认：None；本地：localhost
- port                                    连接端口  默认：None； 本地：6333
- uri                                       连接Zilliz服务器地址
- api_key                               连接Zilliz服务器token

**Qdrant向量数据库**

……



##### 2. 向量模型配置

```
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
```
**ModelScope modelscope-embedding模型**

provider: "modelscope"

config ：

- model_name      modelscope embedding model name


**MiniMax Embeddings模型**

provider: "minimax"

config ：

- api_key         minimax api key
- group_id       minimax  group id

**Doubao doubao-embedding模型**

provider: "doubao"

config ：

- api_key         doubao api key
- model           doubao embedding model name

**OpenAI Embeddings模型**

……

**HuggingFace Embeddings模型**

……



##### 3. 文档切分配置

支持文档类型：txt、md、xlsx、pdf、docx、csv

character：固定大小分块； separator：分隔符分块；recursive_character：递归字符分割

```
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
```

**separator：分隔符分块**

provider: "separator"

config ：

- separator                     指定文本分割(分隔符)的依据。 默认：\n\n

**character：固定大小分块**

provider: "character"

config ：

- chunk_size                   每个分块的最大字符数。
- chunk_overlap            分块之间的重叠字符数。
- separator                     指定文本分割(分隔符)的依据。 默认：\n\n
- is_separator_regex     是否将分隔符视为正则表达式。默认：False

**recursive_character：递归字符分割**

provider: "recursive_character"

config ：

- chunk_size                   每个分块的最大字符数。
- chunk_overlap            分块之间的重叠字符数。
- separator                     指定文本分割(分隔符)的依据。 默认：\n\n
- is_separator_regex     是否将分隔符视为正则表达式。默认：False



#### RAGLink 开发用法

##### 文档向量化并存储向量数据库

```python
# 输入单文档进行向量化
rag.execute_store(file_path="./XXX/XXX.txt")

# 输入多文档地址进行向量化
rag.execute_store_files(directory="./XXX")
```

**向量数据管理**

```
# 插入向量数据
# docs list结构 需要包含ID 、source、content数据
rag.execute_insert(docs=docs)

# 修改向量数据
# docs  list结构 需要包含ID 、source、content数据
# is_embeddings 是否使用向量模型 True:使用 False:不使用（传入数据需定义向量数据）
rag.execute_update(docs=docs, is_embeddings=True)

# 执行删除向量数据
# ids list结构 只包含数据ID
rag.execute_delete(ids=ids)
```

**检索获取上下文**

```python
# 输入查询语句进行检索获取上下文
result = rag.get_context(question=question, limit=limit)
```



## 版本更新

```angular2html
v0.1.3
优化embedding 模型模块

v0.1.0
新增 ModelScope Embedding

v0.0.9
新增 DouBao Embedding

v0.0.7
新增Milvus向量数据库，数据插入

v0.0.6
新增Milvus向量数据库，数据修改、删除等功能

v0.0.3
新增HuggingFaceEmbedding


```