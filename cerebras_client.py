import os
import time
from cerebras.cloud.sdk import Cerebras

DEFAULT_MODEL = "gpt-oss-120b"

# Maximum number of retries for rate-limit (429) errors
MAX_RETRIES = 3
# Base delay in seconds for exponential backoff
BASE_RETRY_DELAY = 2


class RateLimitError(Exception):
    """Raised when the API rate limit or token quota is exceeded after all retries."""
    pass


class CerebrasClient:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("CerebrasClient must be initialized with an API key.")
        self.client = Cerebras(api_key=api_key)

    def get_chat_completion(self, messages, model=DEFAULT_MODEL, **kwargs):
        last_exception = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model=model,
                    **kwargs
                )
                return chat_completion
            except Exception as e:
                status_code = getattr(e, "status_code", None)
                error_str = str(e)
                is_rate_limit = (
                    status_code == 429
                    or "429" in error_str
                    or "quota" in error_str.lower()
                )
                if is_rate_limit and attempt < MAX_RETRIES:
                    last_exception = e
                    delay = BASE_RETRY_DELAY * (2 ** attempt)
                    time.sleep(delay)
                    continue
                if is_rate_limit:
                    raise RateLimitError(
                        "已超出 Cerebras API 每日 Token 配額限制。\n"
                        "建議：\n"
                        "1) 降低「最大 Tokens」設定值；\n"
                        "2) 選擇較小的模型（如 llama3.1-8b）；\n"
                        "3) 等待配額重置後再試。"
                    ) from e
                raise
