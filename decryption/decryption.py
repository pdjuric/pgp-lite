from typing import Optional

from code import Code
from .step import Step
from message import Message
from ring import PrivateRing
from ske import SymmetricKeyAlgorithm


class Decryption(Step):

    def execute_step(self, message: Message, algorithm_code: Optional[Code] = None):
        public_key_ID = message.get_bytes(8)
        encrypted_session_key = message.get_bytes(16)

        private_key_entry = PrivateRing.get_private_key_entry(public_key_ID)
        Step.logger.info("Private key found - using key {}.".format(public_key_ID.hex()))

        # TODO: request password ?
        password_hash = b'1234567890123456'

        private_key = private_key_entry.get_private_key(password_hash)
        Step.logger.info("Private key decrypted")

        session_key = private_key.decrypt(encrypted_session_key)
        Step.logger.info("Session key decrypted")

        symmetric_key_algorithm = SymmetricKeyAlgorithm.get_by_code(algorithm_code)
        Step.logger.error("Symmetric key algorithm found - using {}".format(algorithm_code.str))

        plaintext = symmetric_key_algorithm.decrypt(session_key, message.get_remaining_bytes())
        Step.logger.error("Message decrypted.")

        message.set_bytes(plaintext)

    def get_code(self) -> Code:
        return Code.Encrypted
