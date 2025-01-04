from llama.messages.messages import UserMessage, AssistantMessage, SystemMessage, BaseMessage


class Conservation:
    def __init__(self, system_prompt: SystemMessage = None):
        self.messages = []
        if system_prompt:
            self.system_prompt = system_prompt
            self.messages.append(self.system_prompt)

    def add_message(self, message: BaseMessage):
        if not isinstance(message, BaseMessage):
            raise TypeError("Message must be an instance of BaseMessage or its subclasses.")
        self.messages.append(message)

    def __call__(self):
        return [message.get_message() for message in self.messages]
