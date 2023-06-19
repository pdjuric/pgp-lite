from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

from codes import Code
from ske.algorithm import SymmetricKeyAlgorithm


class TripleDES(SymmetricKeyAlgorithm):
    def encrypt(self, key: bytes, data: bytes) -> bytes:
        try:
            key = DES3.adjust_key_parity(key)
        except ValueError:
            raise Exception("TripleDES encryption error. Invalid key size or degenerates into Single DES.")

        des3_algorithm = DES3.new(key, DES3.MODE_OPENPGP)
        return des3_algorithm.encrypt(pad(data, DES3.block_size))

    def decrypt(self, key: bytes, data: bytes) -> bytes:
        encrypted_iv_len = SymmetricKeyAlgorithm.key_size_in_bytes // 2 + 2
        iv = data[0:encrypted_iv_len]
        ciphertext = data[encrypted_iv_len:]

        try:
            key = DES3.adjust_key_parity(key)
        except ValueError:
            raise Exception("TripleDES decryption error. Invalid key size or degenerates into Single DES.")

        des3_algorithm = DES3.new(key, DES3.MODE_OPENPGP, iv=iv)
        return unpad(des3_algorithm.decrypt(ciphertext), DES3.block_size)

    def get_code(self) -> Code:
        return Code.TripleDES
