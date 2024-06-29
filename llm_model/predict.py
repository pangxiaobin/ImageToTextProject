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
    def __init__(self) -> None:
        super().__init__()
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
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

    def __init__(
        self,
        spark_llm_domain="generalv3",
    ):
        self.llm = SparkLLM(
            spark_llm_domain=spark_llm_domain,
            verbose=True,
            # spark_api_url="wss://spark-api.xf-yun.com/v4.0/chat",
        )
        # 初始化讯飞API

    def generate(self, prompt: str) -> str:
        # 调用讯飞API生成故事
        response = self.llm.invoke(prompt)

        return response


def get_story_prompt(
    input_sentence,
    tone="adventurous",
    target_audience="general audience",
    length="200 words",
):
    prompt = f"""
    Please generate a complete and engaging story in Chinese based on 
    the following input sentence. The story should have a clear beginning, 
    middle, and end. Ensure the plot is coherent, creative, and captivating.
    Incorporate vivid descriptions, character development, and an intriguing conflict 
    or challenge that leads to a satisfying resolution. 
    The story should take place around noon and reflect the
    atmosphere and events typical of that time of day. 
    he tone of the story should be {tone}, and it should b
    e appropriate for {target_audience}. The story shoul
    d be approximately {length} long.

    Input Sentence: {input_sentence}

    Please generate the story in Chinese.
    """
    # Assuming you've set up LangChain call, here's an example call

    return prompt


def get_poetry_prompt(input_sentence):
    prompt = f"""
    Please find a historical classical Chinese poem that fits the following input sentence.
    The poem should be relevant to the given scenario. Answer in Chinese, and ensure the response is
   formatted for easy display in HTML, including the title, author, and era if available.

    Input sentence: {input_sentence}
    Response format:
        <poem>
        <title>Title of the Poem</title><br>
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
    # story = iflytek_model.generate(prompt)
    # print(story)
    poetry_prompt = get_poetry_prompt("夕阳西下")
    poetry = iflytek_model.generate(poetry_prompt)
    print(poetry)
