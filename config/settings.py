# config/settings.py
import os
from dotenv import load_dotenv, find_dotenv


class Config:
    def __init__(self):
        load_dotenv(find_dotenv())

    def get_together_ai_api_key():
        return os.getenv("TOGETHER_API_KEY")

    def get_base_url_prompt():
        return f"{os.getenv('DLAI_TOGETHER_API_BASE', 'https://api.together.xyz')}/v1/chat/completions"
