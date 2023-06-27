from typing import Optional

from codes import Code
from .step import Step
from message import Message
from ring import PrivateRing
from ske import SymmetricKeyAlgorithm


class DecryptionStep(Step):
    def __init__(self):
        self.password_hash = None

    def set_password(self, password):
        self.password = password
        return True

    def execute_step(self, message: Message, algorithm_code: Optional[Code] = None):
        public_key_ID = message.get_bytes(8)
        private_key_entry = PrivateRing.get_by_key_ID(public_key_ID)
        encrypted_session_key = message.get_bytes(private_key_entry.public_key.get_signature_size())
        Step.logger.info("Private key found - using key {}.".format(public_key_ID.hex()))

        from gui.password_prompt import enter_password
        enter_password(self.set_password)

        private_key = private_key_entry.get_private_key(bytes(self.password, 'utf-8'))
        Step.logger.info("Private key decrypted")

        session_key = private_key.decrypt(encrypted_session_key)
        Step.logger.info("Session key decrypted")

        symmetric_key_algorithm = SymmetricKeyAlgorithm.get_by_code(algorithm_code)
        Step.logger.info("Symmetric key algorithm found - using code {}".format(algorithm_code.value))

        plaintext = symmetric_key_algorithm.decrypt(session_key, message.get_remaining_bytes())
        Step.logger.info("Message decrypted.")

        message.set_bytes(plaintext)

    def get_code(self) -> Code:
        return Code.Encrypted
