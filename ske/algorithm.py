from __future__ import annotations

import secrets
from abc import ABC, abstractmethod

from code import Code
from exceptions import UnsupportedSymmetricKeyAlgorithm

class SymmetricKeyAlgorithm(ABC):
    key_size_in_bytes: int = 16
    map: dict[Code: SymmetricKeyAlgorithm] = {}

    @staticmethod
    def get_by_code(code: Code) -> SymmetricKeyAlgorithm:
        try:
            return SymmetricKeyAlgorithm.map[code]
        except KeyError:
            raise UnsupportedSymmetricKeyAlgorithm(code)

    @staticmethod
    def generate_session_key() -> bytes:
        # todo
        return secrets.token_bytes(SymmetricKeyAlgorithm.key_size_in_bytes)

    @abstractmethod
    def encrypt(self, key: bytes, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, key: bytes, data: bytes) -> bytes:
        pass

    @abstractmethod
    def get_code(self) -> Code:
        pass
