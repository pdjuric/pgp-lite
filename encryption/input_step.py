from datetime import datetime

from code import Code
from encryption.step import Step
from message import Message


class InputStep(Step):

    def __init__(self, text):
        self.text = text

    def execute_step(self, message: Message):
        timestamp = int(datetime.now().timestamp())
        message.append(timestamp)
        message.append(self.text)

    def get_code(self) -> Code:
        return Code.Plaintext
