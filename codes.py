from __future__ import annotations

from enum import Enum


class Code:
    def __init__(self, value:int):
        self.value = value

    def __contains__(self, code: Code) -> bool:
        return self.value & code.value == self.value

    def __and__(self, other: Code) -> Code:
        return Code(self.value & other.value)

    def __or__(self, other: Code) -> Code:
        return Code(self.value | other.value)

    def __xor__(self, other: Code) -> Code:
        return Code(self.value ^ other.value)

    RSA = None
    DSA = None
    ElGamal = None

    AES128 = None
    TripleDES = None

    Plaintext = None
    Signed = None
    Compressed = None
    Encrypted = None
    Radix64Converted = None


Code.RSA = Code(0x00)
Code.DSA = Code(0x01)
Code.ElGamal = Code(0x02)

Code.AES128 = Code(0x04)
Code.TripleDES = Code(0x08)

Code.Plaintext = Code(0x08)
Code.Signed = Code(0x10)
Code.Compressed = Code(0x20)
Code.Encrypted = Code(0x40)
Code.Radix64Converted = Code(0x80)
