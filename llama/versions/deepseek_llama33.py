import requests
from llama.config.settings import Config
from llama.base import LlamaBase
from together import Together
import json


class DeepSeekLLaMA33(LlamaBase):
    def __init__(self, temperature=0.0, model_size=70):
        self._version = "llama3.1"
        self._api_key = Config.get_together_ai_api_key()
        self._base_url = Config.get_base_url_prompt()
        self.model_size = model_size
        self.temperature = temperature
        self.client = Together()

        if not self._api_key:
            raise ValueError("API key is missing. Set TOGETHER_API_KEY in your environment.")

    def get_payload(self, messages: dict):
        payload = {
            "model": self.get_model(),
            "temperature": self.temperature,
            "messages": messages,
        }

        return payload

    def get_authorization(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        return headers

    def get_model(self):
        return f"deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"

    def send_request(self, messages: dict):
        try:
            response = self.client.chat.completions.create(
                model=self.get_model(),
                messages=messages,
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

        if "error" in response:
            raise Exception(f"API Error: {response['error']}")

        return response.choices[0].message.content

    def generate(self, messages):
        return self.send_request(messages)
