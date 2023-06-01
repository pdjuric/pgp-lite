from __future__ import annotations

from enum import Enum


class Code(Enum):

    def __init__(self, value: int, verbose: str = ""):
        self.value = value
        self.str = verbose

    # def __init__(self, byte: bytes):
    #     self.value = int.from_bytes(byte, 'big')

    def __contains__(self, code: Code) -> bool:
        return self.value & code.value == code.value

    def __and__(self, other: Code) -> Code:
        return Code(self.value & other.value)

    def __or__(self, other: Code) -> Code:
        return Code(self.value | other.value)

    def __xor__(self, other: Code) -> Code:
        return Code(self.value ^ other.value)


    # lower nibble will be used for algorithm code, bigger for step encoding
    RSA = 0x01, "RSA"
    DSA = 0x02, "DSA"
    ElGamal = 0x04, "ElGamal"

    AES128 = 0x01, "AES128"
    TripleDES = 0x02, "TripleDES"

    Plaintext = 0x00, "Plaintext"
    Signed = 0x10, "Signed"
    Compressed = 0x20, "Compressed"
    Encrypted = 0x40, "Encrypted"
    Radix64Converted = 0x80, "Radix64Converted"
