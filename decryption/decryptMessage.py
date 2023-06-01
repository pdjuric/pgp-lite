from .conversion import Conversion
from .decompression import Decompression
from .decryption import Decryption
from .verification import Verification
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