from dataclasses import dataclass
from llama.messages.base_message import MessageRole, BaseMessage, MessageType
import base64
import os


@dataclass
class SystemMessage(BaseMessage):
    """
    This is a protocol class that defines the structure of a system message.
    """

    content: str
    role: MessageRole = MessageRole.SYSTEM
    message_type: MessageType = MessageType.TEXT


@dataclass
class UserMessage(BaseMessage):
    """
    This is a protocol class that defines the structure of a user message.
    """

    content: str
    role: MessageRole = MessageRole.USER
    message_type: MessageType = MessageType.TEXT


@dataclass
class AssistantMessage(BaseMessage):
    """
    This is a protocol class that defines the structure of an assistant message.
    """

    content: str
    role: MessageRole = MessageRole.ASSISTANT
    message_type: MessageType = MessageType.TEXT


@dataclass
class IPythonMessage(BaseMessage):
    """
    This is a protocol class that defines the structure of an IPython message.
    """

    content: str
    role: MessageRole = MessageRole.IPYTHON
    message_type: MessageType = MessageType.TEXT


@dataclass
class ImageMessage(BaseMessage):
    """
    This is a protocol class that defines the structure of an image message.
    """

    content: str
    image: str | os.PathLike
    role: MessageRole = MessageRole.USER
    message_type: MessageType = MessageType.IMAGE

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def get_image(self, image):
        if os.path.exists(image):
            return f"data:image/png;base64,{self.encode_image(image)}"

        return image

    def get_message(self) -> dict:
        """
        This method should return the message in a specific format.
        It will be overridden in the subclasses.
        """
        return {
            "role": self.role.value,
            "content": [
                {"type": "text", "text": self.content},
                {
                    "type": self.message_type.value,
                    "image_url": {"url": self.get_image(self.image)},
                },
            ],
        }
