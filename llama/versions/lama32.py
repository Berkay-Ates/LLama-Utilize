import requests
from llama.config.settings import Config
from llama.base import LlamaBase
import json
from together import Together


class Llama32(LlamaBase):

    def __init__(self, max_tokens=4096, temperature=0.0, model_size=11):
        self._version = "llama3.2"
        self._api_key = Config.get_together_ai_api_key()
        self._base_url = Config.get_base_url_prompt()
        self.model_size = model_size
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = Together()

        if not self._api_key:
            raise ValueError("API key is missing. Set TOGETHER_API_KEY in your environment.")

    def get_payload(self, messages: dict):
        payload = {
            "model": self.get_model(),
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stop": ["<|eot_id|>", "<|eom_id|>"],
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
        return f"meta-llama/Llama-3.2-{self.model_size}B-Vision-Instruct-Turbo"

    def send_request(self, message: dict):

        try:
            response = self.client.chat.completions.create(
                model=self.get_model(),
                messages=message,
            )

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

        if "error" in response:
            raise Exception(response["error"])

        return response.choices[0].message.content

    def generate(self, message):
        if message is None or message == "":
            raise ValueError("Prompt message should be a valid value!")

        return self.send_request(message)
