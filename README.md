# ImageToTextProject

## 项目介绍

本项目基于Hugging Face的`transformers`库，实现了图片到文本的任务。

### 安装依赖

```shell
# python version == 3.11.2

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 模型下载

- 文件比较大，如果失败请多尝试，或者单独把模型下载到本地
- 文档<https://hf-mirror.com/>


### 推荐网盘下载地址

- [夸克网盘链接](https://pan.quark.cn/s/849887c2d560)
- [百度网盘链接](https://pan.baidu.com/s/1Yvl46DBzt6zfDUMVdLP2gQ) https://pan.baidu.com/s/1Yvl46DBzt6zfDUMVdLP2gQ 提取码: j2wi

> 把下载的models解压到predict_model 下面

目录结构
```
predict_model
├── __init__.py
├── base_model.py
├── bicl_model.py
├── models
│   └── blip-image-captioning-large
│       ├── README.md
│       ├── config.json
│       ├── model.safetensors
│       ├── preprocessor_config.json
│       ├── pytorch_model.bin
│       ├── special_tokens_map.json
│       ├── tf_model.h5
│       ├── tokenizer.json
│       ├── tokenizer_config.json
│       └── vocab.txt
```

```shell
# linux or mac 设置环境变量
export HF_ENDPOINT=https://hf-mirror.com

# windows cmd 设置环境变量
set HF_ENDPOINT=https://hf-mirror.com
# Windows Powershell
$env:HF_ENDPOINT="https://hf-mirror.com"

# 下载模型
# 地址https://hf-mirror.com/Salesforce/blip-image-captioning-large/tree/main

cd predict_model

huggingface-cli download --resume-download  --local-dir-use-symlinks False Salesforce/blip-image-captioning-large --local-dir models/blip-image-captioning-large

```

### LLM 配置

#### 添加环境变量

```shell
cp .env.example .env
```

> 目前支持讯飞、chatgpt

- xunfei

> 讯飞开放平台账号、APPID、APIKey、API_SECRET 具体可参考[讯飞开放平台](https://www.xfyun.cn/)
> 目前讯飞提供了免费token，可申请试用，有效期为一年，参考这个介绍[讯飞api](https://xinghuo.xfyun.cn/sparkapi),[申请文档](https://www.xfyun.cn/doc/platform/quickguide.html#%E7%AC%AC%E4%B8%80%E6%AD%A5%EF%BC%9A%E6%B3%A8%E5%86%8C%E6%88%90%E4%B8%BA%E5%BC%80%E5%8F%91%E8%80%85)
> 需要实名认证，几分钟就可以认证好了

![详情](./img/1.png)

- chatgpt

> [申请地址](https://platform.openai.com/docs/overview)
>
> 申请完成后，会获得一个API Key，将其填入.env文件中

### 运行项目

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 运行截图

![详情](./img/2.png)

![详情](./img/3.png)

![详情](./img/4.png)
