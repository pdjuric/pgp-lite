import logging
from datetime import datetime

from .conversion_step import ConversionStep
from .decompression_step import DecompressionStep
from .decryption_step import DecryptionStep
from .verification_step import VerificationStep
from message import Message


class DecryptMessage:
    logger: logging.Logger = logging.getLogger()

    def __init__(self):
        self.steps = [
            ConversionStep(),
            DecryptionStep(),
            DecompressionStep(),
            VerificationStep()
        ]

    def exec(self, message: Message):
        for step in self.steps:
            if not step.execute(message):
                break
        message.reset_cursor()
        code = message.get_bytes(1)
        timestamp = message.get_bytes(4)
        plaintext = message.get_remaining_bytes().decode()
        logging.info('Message sent: {}'.format(datetime.fromtimestamp(int.from_bytes(timestamp, 'big'))))
        logging.info('Original message: {}'.format(plaintext))
