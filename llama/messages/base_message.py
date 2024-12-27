from typing import Protocol
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    IPYTHON = "ipython"


class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image_url"


class BaseMessage(Protocol):
    """
    This is a protocol class that defines the structure of a message.
    """

    content: str
    role: MessageRole
    message_type: MessageType

    def get_message(self) -> dict:
        """
        This method should return the message in a specific format.
        It will be overridden in the subclasses.
        """
        return {"role": self.role.value, "content": self.content}
