from Crypto.Hash import SHA1
from Crypto.PublicKey.RSA import RsaKey, generate, import_key
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP

from pke.algorithm import PublicKeyAlgorithm
from pke.key import PublicKey, PrivateKey
from code import Code


class RSAAlgorithm(PublicKeyAlgorithm):

    def generate_keys(self, key_size: int) -> (PrivateKey, PublicKey):
        # todo check possible key sizes

        private_impl = generate(key_size)
        public_impl = private_impl.public_key()

        public = RSAPublicKey(public_impl)
        private = RSAPrivateKey(private_impl, public.get_key_ID())

        return public, private

    def load_private_key(self, data: bytes) -> (PrivateKey, PublicKey):
        private_impl = import_key(data)
        public_impl = private_impl.public_key()

        public = RSAPublicKey(public_impl)
        private = RSAPrivateKey(private_impl, public.get_key_ID())

        return public, private

    def load_public_key(self, data: bytes) -> PublicKey:
        public_impl = import_key(data)
        return RSAPublicKey(public_impl)

    def get_code(self) -> Code:
        return Code.RSA


class RSAPrivateKey(PrivateKey):

    def __init__(self, impl: RsaKey, key_ID: bytes):
        self.impl = impl
        super().__init__(key_ID)

    def sign(self, data: bytes) -> bytes:
        h = SHA1.new(data)      # produces 20-byte hash of the message
        return pkcs1_15.new(self.impl).sign(h)

    def decrypt(self, ciphertext: bytes) -> bytes:
        return PKCS1_OAEP.new(self.impl).decrypt(ciphertext)

    def __bytes__(self) -> bytes:
        return self.impl.export_key()


class RSAPublicKey(PublicKey):

    def __init__(self, impl: RsaKey):
        self.impl = impl

    def verify(self, data: bytes, signature: bytes) -> bool:
        h = SHA1.new(data)
        try:
            pkcs1_15.new(self.impl).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    def encrypt(self, data: bytes) -> bytes:
        return PKCS1_OAEP.new(self.impl).encrypt(data)

    def get_key_ID(self) -> bytes:
        return (self.impl.n % (1 << 64)).to_bytes(8, "big")

    def get_signature_size(self) -> int:
        return self.impl.size_in_bytes()

    def __bytes__(self) -> bytes:
        return self.impl.export_key()
