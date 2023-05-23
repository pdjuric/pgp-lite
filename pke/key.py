from abc import ABC, abstractmethod
from typing import SupportsBytes, Optional
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Hash import SHA1

from pke.algorithm import PublicKeyAlgorithm


class PrivateKey(ABC, SupportsBytes):

    def __init__(self, key_ID: bytes):
        self.key_ID = key_ID

    @abstractmethod
    def sign(self, data: bytes) -> bytes:
        """
        Hashes the data using SHA-1, and encrypts the hash
        :param data: data to be signed
        :return: signature (encrypted hash)
        """
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        pass

    def get_key_ID(self) -> bytes:
        return self.key_ID


class PublicKey(ABC):

    @abstractmethod
    def verify(self, data: bytes, signature: bytes) -> bool:
        pass

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def get_key_ID(self) -> bytes:
        pass

    @abstractmethod
    def get_signature_size(self) -> int:
        pass


class EncryptedPrivateKey:

    def __init__(self, private_key: PrivateKey, pka: PublicKeyAlgorithm, passphrase: bytes):
        # should we pass Code or PublicKeyAlgorithm
        self.pka = pka

        passphrase_hash = SHA1.new(passphrase).digest()

        c = AES.new(passphrase_hash, AES.MODE_CBC)
        self.iv = c.iv
        self.bytes = c.encrypt(pad(bytes(private_key), AES.block_size))

    def decrypt(self, passphrase: bytes) -> Optional[PrivateKey]:
        try:
            passphrase_hash = SHA1.new(passphrase).digest()
            c = AES.new(passphrase_hash, AES.MODE_CBC, self.iv)
            b = unpad(c.decrypt(self.bytes), AES.block_size)
            private_key, _ = self.pka.load_private_key(b)
            return private_key
        except (ValueError, KeyError):
            return None
