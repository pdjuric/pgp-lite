from typing import Optional
from zlib import decompress

from code import Code
from .step import Step
from message import Message


class Decompression(Step):
    def execute_step(self, message: Message, algorithm_code: Optional[Code] = None):
        message.set_bytes(decompress(message.get_remaining_bytes()))
        Step.logger.info("Message decompressed.")

    def get_code(self) -> Code:
        return Code.Compressed
