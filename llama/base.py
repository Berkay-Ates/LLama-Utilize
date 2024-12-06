from abc import ABC, abstractmethod


class LlamaBase(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs):
        """Abstract method for generating a response."""
        pass

    @abstractmethod
    def send_request(self, endpoint: str, payload: dict):
        """Abstract method to send requests to the API."""
        pass

    @abstractmethod
    def get_model(self, model_name):
        "Abstract method for setting the model name"
        pass
