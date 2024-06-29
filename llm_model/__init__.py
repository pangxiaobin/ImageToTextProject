from .predict import *

PROMPT_TYPE_MAP = {
    "story": get_story_prompt,
    "poetry": get_poetry_prompt,
}

LLM_MODEL_MAP = {
    "chat_gpt": ChatGPTModel,
    "iflytek": iFlytekModel,
}
