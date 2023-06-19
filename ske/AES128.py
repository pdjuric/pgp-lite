from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from codes import Code
from ske.algorithm import SymmetricKeyAlgorithm


class AES128(SymmetricKeyAlgorithm):
    def encrypt(self, key: bytes, data: bytes) -> bytes:
        aes_algorithm = AES.new(key, AES.MODE_OPENPGP)
        return aes_algorithm.encrypt(pad(bytes(data), AES.block_size))

    def decrypt(self, key: bytes, data: bytes) -> bytes:
        encrypted_iv_len = SymmetricKeyAlgorithm.key_size_in_bytes + 2
        iv = data[0:encrypted_iv_len]
        ciphertext = data[encrypted_iv_len:]

        aes_algorithm = AES.new(key, AES.MODE_OPENPGP, iv=iv)
        return unpad(aes_algorithm.decrypt(ciphertext), AES.block_size)

    def get_code(self) -> Code:
        return Code.AES128
