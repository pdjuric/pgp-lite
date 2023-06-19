import base64

from typing import Optional
from codes import Code
from .step import Step
from message import Message


class ConversionStep(Step):

    def execute_step(self, message: Message, algorithm_code: Optional[Code] = None):
        converted_message = base64.b64decode(message.get_bytes(0))
        message.set_bytes(converted_message)
        Step.logger.info("Message converted.")

    def get_code(self) -> Code:
        return Code.Radix64Converted
