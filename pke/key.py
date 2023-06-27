from abc import ABC, abstractmethod
from typing import SupportsBytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Hash import SHA1

from codes import Code
from exceptions import PrivateKeyDecryptionError
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

    @abstractmethod
    def get_algorithm_code(self) -> Code:
        pass


class PublicKey(ABC, SupportsBytes):

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

    @abstractmethod
    def get_algorithm_code(self) -> Code:
        pass


class EncryptedPrivateKey:

    def __init__(self, private_key: PrivateKey, pka_code: Code, passphrase: bytes):
        self.pka_code = pka_code

        passphrase_hash = SHA1.new(passphrase).digest()

        c = AES.new(passphrase_hash[:16], AES.MODE_CBC)
        self.iv = c.iv
        self.bytes = c.encrypt(pad(bytes(private_key), AES.block_size))

    def decrypt(self, passphrase: bytes) -> PrivateKey:
        try:
            passphrase_hash = SHA1.new(passphrase).digest()
            c = AES.new(passphrase_hash[:16], AES.MODE_CBC, self.iv)
            x = c.decrypt(self.bytes)
            b = unpad(x, AES.block_size)
            private_key, _ = PublicKeyAlgorithm.get_by_code(self.pka_code).load_private_key(b)
            return private_key
        except (ValueError, KeyError) as e:
            raise PrivateKeyDecryptionError(e)
