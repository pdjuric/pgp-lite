from code import Code
from encryption.step import Step
from message import Message
from zlib import compress

from pke import PublicKey
from ske import SymmetricKeyAlgorithm


class EncryptionStep(Step):

    def __init__(self, public_key: PublicKey, algorithm: SymmetricKeyAlgorithm):
        self.public_key = public_key
        self.algorithm = algorithm

    def execute_step(self, message: Message):
        session_key = SymmetricKeyAlgorithm.generate_session_key()
        encrypted_data = SymmetricKeyAlgorithm.encrypt(session_key, message.get_bytes(0))
        encrypted_session_key = self.public_key.encrypt(session_key)

        message.set_bytes(encrypted_data)
        message.prepend(encrypted_session_key)
        message.prepend(self.public_key.get_key_ID())

    def get_code(self) -> Code:
        return Code.Encrypted
