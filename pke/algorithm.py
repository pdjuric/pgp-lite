from __future__ import annotations
from abc import ABC, abstractmethod

from codes import Code


class PublicKeyAlgorithm(ABC):
    map: dict[Code, PublicKeyAlgorithm] = {}

    @staticmethod
    def get_by_code(code: Code) -> PublicKeyAlgorithm:
        # todo
        pass

    @abstractmethod
    def generate_keys(self, key_size: int) -> (PrivateKey, PublicKey):
        pass

    @abstractmethod
    def load_private_key(self, data: bytes) -> (PrivateKey, PublicKey):
        pass

    @abstractmethod
    def load_public_key(self, data: bytes) -> PublicKey:
        pass

    @abstractmethod
    def get_code(self) -> Code:
        pass
