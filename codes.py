from __future__ import annotations

from enum import Enum


class Code(Enum):

    def __contains__(self, code: Code) -> bool:
        return self.value & code.value == code.value

    def __and__(self, other: Code) -> Code:
        return Code(self.value & other.value)

    def __or__(self, other: Code) -> Code:
        return Code(self.value | other.value)

    def __xor__(self, other: Code) -> Code:
        return Code(self.value ^ other.value)


    RSA = 0x01
    DSA = 0x02
    ElGamal = 0x04

    AES128 = 0x01
    TripleDES = 0x02

    Plaintext = 0x00
    Signed = 0x10
    Compressed = 0x20
    Encrypted = 0x40
    Radix64Converted = 0x80
