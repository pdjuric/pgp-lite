from code import Code
from encryption.step import Step
from message import Message
from zlib import compress

class CompressionStep(Step):

    def execute_step(self, message: Message):
        message.set_bytes(compress(message.get_bytes(0)))

    def get_code(self) -> Code:
        return Code.Compressed
