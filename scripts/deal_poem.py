# 处理诗歌数据集，只要里面的 title dynasty author content

import os
import json
import pandas as pd

# 读取诗歌数据集
df = pd.read_json("poem_data.json")
# 只要 title dynasty author content
df = df[["title", "dynasty", "author", "content"]]
# 保存为 json 文件
df.to_json("simple_poems.json", orient="records", indent=4, force_ascii=False)
