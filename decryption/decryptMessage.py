from .conversion_step import Conversion
from .decompression_step import Decompression
from .decryption_step import Decryption
from .verification_step import Verification
from message import Message


class DecryptMessage:
    def __init__(self):
        self.steps = [
            Conversion(),
            Decryption(),
            Decompression(),
            Verification()
        ]

    def exec(self, message: Message):
        for step in self.steps:
            if not step.execute(message):
                break