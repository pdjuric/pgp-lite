from typing import Optional

from code import Code
from .step import Step
from message import Message


class Conversion(Step):

    def execute_step(self, message: Message, algorithm_code: Optional[Code] = None):
        # todo
        raise NotImplemented

    def get_code(self) -> Code:
        return Code.Radix64Converted
