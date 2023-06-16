from abc import ABC, abstractmethod

from code import Code
from message import Message

class Step(ABC):

    def execute(self, message:Message):
        self.execute_step(message)
        code = self.get_code()
        message.prepend(code)

    @abstractmethod
    def execute_step(self, message: Message):
        pass

    @abstractmethod
    def get_code(self) -> Code:
        pass
    