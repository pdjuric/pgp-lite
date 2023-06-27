from Crypto.Hash import SHA1
from Crypto.PublicKey.RSA import RsaKey, generate, import_key
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP

from exceptions import DecryptionError
from pke.algorithm import PublicKeyAlgorithm
from pke.key import PublicKey, PrivateKey
from codes import Code


saved_hash = None
saved_signature = None

class RSAAlgorithm(PublicKeyAlgorithm):

    def generate_keys(self, key_size: int) -> (PrivateKey, PublicKey):
        private_impl = generate(key_size)
        public_impl = private_impl.public_key()

        public = RSAPublicKey(public_impl)
        private = RSAPrivateKey(private_impl, public.get_key_ID())

        return private, public

    def load_private_key(self, data: bytes) -> (PrivateKey, PublicKey):
        private_impl = import_key(data)
        public_impl = private_impl.public_key()

        public = RSAPublicKey(public_impl)
        private = RSAPrivateKey(private_impl, public.get_key_ID())

        return private, public

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
        saved_signature = pkcs1_15.new(self.impl).sign(h)
        return saved_signature

    def decrypt(self, ciphertext: bytes) -> bytes:
        try:
            return PKCS1_OAEP.new(self.impl).decrypt(ciphertext)
        except (ValueError, TypeError) as e:
            raise DecryptionError(e)

    def get_algorithm_code(self) -> Code:
        return Code.RSA

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
        except (ValueError, TypeError) as e:
            return False

    def encrypt(self, data: bytes) -> bytes:
        return PKCS1_OAEP.new(self.impl).encrypt(data)

    def get_key_ID(self) -> bytes:
        return (self.impl.n % (1 << 64)).to_bytes(8, "big")

    def get_signature_size(self) -> int:
        return self.impl.size_in_bytes()

    def get_algorithm_code(self) -> Code:
        return Code.RSA

    def __bytes__(self) -> bytes:
        exported = self.impl.export_key()
        return exported[:11] + bytes("RSA ", 'utf-8') + exported[11:]
