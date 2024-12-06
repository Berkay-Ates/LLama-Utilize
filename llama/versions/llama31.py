import requests
from config.settings import Config
from llama.base import LlamaBase
import json


class Llama31(LlamaBase):
    def __init__(self, temperature=0.0, model_size=8):
        self._version = "llama3.1"
        self._api_key = Config.get_together_ai_api_key()
        self._base_url = Config.get_base_url_prompt()
        self.model_size = model_size
        self.temperature = temperature

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
        return f"meta-llama/Meta-Llama-3.1-{self.model_size}B-Instruct-Turbo"

    def send_request(self, messages: dict):
        try:
            response = requests.post(
                self._base_url, headers=self.get_authorization(), data=json.dumps(self.get_payload(messages))
            )
            response.raise_for_status()  # Raises HTTPError for bad responses
            res = response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

        if "error" in res:
            raise Exception(f"API Error: {res['error']}")

        return res["choices"][0]["message"]["content"]

    def generate(self, messages):
        return self.send_request(messages)
