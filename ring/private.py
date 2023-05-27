from datetime import datetime

from pke.key import *


class PrivateRingEntry:

    def __init__(self, user: str, encrypted_private_key: EncryptedPrivateKey, public_key: PublicKey,
                 timestamp: datetime):
        self.timestamp = timestamp
        self._encrypted_private_key = encrypted_private_key
        self.public_key = public_key
        self.user = user

    def get_private_key(self, passphrase: bytes) -> PrivateKey:
        return self._encrypted_private_key.decrypt(passphrase)

    def get_pka_code(self) -> Code:
        return self._encrypted_private_key.pka_code
