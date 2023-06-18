from Crypto.Cipher import AES

from codes import Code
from ske.algorithm import SymmetricKeyAlgorithm


class AES128(SymmetricKeyAlgorithm):
    def encrypt(self, key: bytes, data: bytes) -> bytes:
        aes_algorithm = AES.new(key, AES.MODE_OPENPGP)
        return aes_algorithm.encrypt(data)

    def decrypt(self, key: bytes, data: bytes) -> bytes:
        encrypted_iv_len = SymmetricKeyAlgorithm.key_size_in_bytes + 2
        iv = data[0:encrypted_iv_len]
        ciphertext = data[encrypted_iv_len:]

        aes_algorithm = AES.new(key, AES.MODE_OPENPGP, iv=iv)
        return aes_algorithm.decrypt(ciphertext)

    def get_code(self) -> Code:
        return Code.AES128
