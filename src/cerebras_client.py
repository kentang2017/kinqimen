import os
from cerebras.cloud.sdk import Cerebras

DEFAULT_MODEL = "qwen-3-235b-a22b-instruct-2507"


class CerebrasClient:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("CerebrasClient must be initialized with an API key.")
        self.client = Cerebras(api_key=api_key)

    def get_chat_completion(self, messages, model=DEFAULT_MODEL, **kwargs):
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=model,
            **kwargs
        )
        return chat_completion
