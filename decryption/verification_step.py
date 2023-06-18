from datetime import datetime
from typing import Optional

from Crypto.Hash import SHA1

from codes import Code
from .step import Step
from exceptions import HashStartMissmatch, VerificationFailed
from message import Message
from ring import PublicRing


class VerificationStep(Step):

    def execute_step(self, message: Message, algorithm_code: Optional[Code] = None):
        timestamp = message.get_bytes(4)
        public_key_ID = message.get_bytes(8)
        hash_start = message.get_bytes(2)

        public_key_entry = PublicRing.get_public_key_entry(public_key_ID)
        Step.logger.info("Public key found - using key {}.".format(public_key_ID.hex()))


        # todo: make sure to use int(datetime.now().timestamp()) when generating timestamp

        info_str = 'User: {}. Signing time: {}.'\
            .format(public_key_entry.user.ID)\
            .format(datetime.fromtimestamp(int.from_bytes(timestamp, 'big')))

        if public_key_entry.get_key_legitimacy():
            Step.logger.info("{} Key legitimate!".format(info_str))
        else:
            Step.logger.error("{} Key not legitimate!".format(info_str))

        public_key = public_key_entry.get_public_key()

        signature = message.get_bytes(public_key.get_signature_size())
        message_hash = SHA1.new(message.get_remaining_bytes())      #todo ??

        if message_hash.digest() != hash_start:
            raise HashStartMissmatch(hash_start, message_hash.digest())

        if not public_key.verify(message.get_remaining_bytes(), signature):
            raise VerificationFailed(public_key_ID)

        Step.logger.info("Message verified.")

    def get_code(self) -> Code:
        return Code.Signed
