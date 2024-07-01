from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain_community.llms import SparkLLM
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

# 加载环境变量
from dotenv import load_dotenv

load_dotenv(dotenv_path=ENV_PATH)

IFLYTEK_SPARK_APP_ID = os.getenv("IFLYTEK_SPARK_APP_ID")

print(f"Loading environment variables from {IFLYTEK_SPARK_APP_ID}")


class LanguageModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class ChatGPTModel(LanguageModel):
    def __init__(self, model_name: str = "gpt-3.5-turbo") -> None:
        super().__init__()
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.ainvoke(prompt)
        return response.choices[0].text.strip()


# 示例讯飞模型
class iFlytekModel(LanguageModel):
    """
    doc url:https://api.python.langchain.com/en/latest/llms/langchain_community.llms.sparkllm.SparkLLM.html#
    sparm dom https://www.xfyun.cn/doc/spark/Web.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E

    Spark4.0 Ultra 请求地址,对应的domain参数为4.0Ultra  wss://spark-api.xf-yun.com/v4.0/chat

    Spark Max请求地址,对应的domain参数为generalv3.5
    Spark Pro请求地址,对应的domain参数为generalv3
    Spark V2.0请求地址,对应的domain参数为generalv2
    Spark Lite请求地址,对应的domain参数为general

    """

    def get_api_url(self, domain: str) -> str:
        domin_dict = {
            "4.0Ultra": "wss://spark-api.xf-yun.com/v4.0/chat",
            "generalv3.5": "wss://spark-api.xf-yun.com/v3.5/chat",
            "generalv3": "wss://spark-api.xf-yun.com/v3.1/chat",
            "generalv2": "wss://spark-api.xf-yun.com/v2.1/chat",
            "general": "wss://spark-api.xf-yun.com/v1.1/chat",
        }
        return domin_dict.get(domain, "wss://spark-api.xf-yun.com/v1/chat")

    def __init__(
        self,
        model_name: str = "generalv3",
    ):
        api_url = self.get_api_url(model_name)
        self.llm = SparkLLM(
            spark_llm_domain=model_name,
            verbose=True,
            spark_api_url=api_url,
        )
        # 初始化讯飞API

    def generate(self, prompt: str) -> str:
        # 调用讯飞API生成故事
        response = self.llm.invoke(prompt)

        return response


def get_story_prompt(
    input_sentence,
    length="200 words",
):
    prompt = f"""your are a novel writer, please write a small story (about {length}) in Chinsese according to the user input.
    user input: {input_sentence}"""
    return prompt


def get_poetry_prompt(input_sentence):
    prompt = f"""
    Please find a historical classical Chinese poem that fits the following input sentence.
    The poem should be relevant to the given scenario. Answer in Chinese, and ensure the response is
   formatted for easy display in HTML, including the title, author, and era if available.

    Input sentence: {input_sentence}
    Response format:
        <poem>
        <h3>Title of the Poem</h3><br>
        <author>Author Name</author><br>
        <era>Dynasty/Era</era><br>
        <content>
            Line 1 of the poem<br>
            Line 2 of the poem<br>
            Line 3 of the poem<br>
            Line 4 of the poem
        </content>
        </poem>
    """

    return prompt


if __name__ == "__main__":
    # 测试讯飞模型
    iflytek_model = iFlytekModel()
    prompt = get_story_prompt("I love playing video games.")
    story = iflytek_model.generate()
    print(story)
    poetry_prompt = get_poetry_prompt("夕阳西下")
    poetry = iflytek_model.generate(poetry_prompt)
    print(poetry)
