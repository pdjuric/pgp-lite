from abc import ABC, abstractmethod
from typing import Optional
import logging

from code import Code
from message import Message


class Step(ABC):

    logger: logging.Logger = None

    @abstractmethod
    def execute_step(self, message: Message, algorithm_code: Optional[Code] = None):
        pass

    @abstractmethod
    def get_code(self) -> Code:
        pass

    def execute(self, message: Message) -> bool:
        message.reset_cursor()

        code_byte_from_received_msg = message.get_bytes(1)
        code_from_received_msg = Code(int.from_bytes(code_byte_from_received_msg, 'big'))

        if code_from_received_msg in self.get_code():
            try:
                self.execute_step(message, code_from_received_msg ^ self.get_code())
            except Exception as e:
                Step.logger.error("IN {} - {}".format(self.__class__.__name__).format(e))
                return False
        else:
            message.move_cursor(-1)

        return True


