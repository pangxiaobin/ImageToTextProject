from .predict import *

PROMPT_TYPE_MAP = {
    "story": get_story_prompt,
    "poetry": get_poetry_prompt,
}

LLM_MODEL_MAP = {
    "chat_gpt": {
        "LLMCLass": "ChatGPTModel",
        "model_list": [
            "gpt-3.5-turbo",
            "gpt-4o",
            "gpt-4-turbo",
        ],
    },
    "iflytek": {
        "LLMCLass": "iFlytekModel",
        "model_list": ["4.0Ultra", "generalv3.5", "generalv3", "generalv2", "general"],
    },
}
