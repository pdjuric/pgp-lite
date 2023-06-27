from datetime import datetime
from Crypto.Hash import SHA1
from codes import Code
from encryption.step import Step
from message import Message
from pke import PrivateKey


class AuthenticationStep(Step):

    def __init__(self, private_key: PrivateKey):
        self.private_key = private_key

    def execute_step(self, message: Message):
        timestamp = int(datetime.now().timestamp())
        msg = message.get_bytes(0)
        hash = SHA1.new(msg)
        signature = self.private_key.sign(msg)

        message.prepend(signature)
        message.prepend(hash.digest()[:2])
        message.prepend(self.private_key.get_key_ID())
        message.prepend(timestamp.to_bytes(length=4, byteorder='big'))

    def get_code(self) -> Code:
        return Code.Signed | self.private_key.get_algorithm_code()
