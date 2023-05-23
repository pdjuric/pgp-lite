from Crypto.Hash import SHA1
from Crypto.PublicKey.DSA import DsaKey, generate, import_key
from Crypto.Signature import DSS

from pke.algorithm import PublicKeyAlgorithm
from pke.key import PublicKey, PrivateKey
from code import Code


class DSAAlgorithm(PublicKeyAlgorithm):

    def generate_keys(self, key_size: int) -> (PrivateKey, PublicKey):
        private_impl = generate(key_size)
        public_impl = private_impl.public_key()

        public = DSAPublicKey(public_impl)
        private = DSAPrivateKey(private_impl, public.get_key_ID())

        return public, private

    def load_private_key(self, data: bytes) -> (PrivateKey, PublicKey):
        private_impl = import_key(data)
        public_impl = private_impl.public_key()

        public = DSAPublicKey(public_impl)
        private = DSAPrivateKey(private_impl, public.get_key_ID())

        return public, private

    def load_public_key(self, data: bytes) -> PublicKey:
        public_impl = import_key(data)
        return DSAPublicKey(public_impl)

    def get_code(self) -> Code:
        return Code.DSA


class DSAPrivateKey(PrivateKey):

    def __init__(self, impl: DsaKey, key_ID: bytes):
        self.impl = impl
        super().__init__(key_ID)

    def sign(self, data: bytes) -> bytes:
        h = SHA1.new(data)  # produces 20-byte hash of the message
        return DSS.new(self.impl, 'fips-186-3').sign(h)

    def decrypt(self, ciphertext: bytes) -> bytes:
        raise Exception("Unsupported operation: DSAPrivateKey.decrypt")

    def __bytes__(self) -> bytes:
        return self.impl.export_key()


class DSAPublicKey(PublicKey):

    def __init__(self, impl: DsaKey):
        self.impl = impl

    def verify(self, data: bytes, signature: bytes) -> bool:
        h = SHA1.new(data)
        try:
            DSS.new(self.impl, 'fips-186-3').verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    def encrypt(self, data: bytes) -> bytes:
        raise Exception("Unsupported operation: DSAPublicKey.encrypt")

    def get_key_ID(self) -> bytes:
        return (self.impl.n % (1 << 64)).to_bytes(8, "big")

    def get_signature_size(self) -> int:
        size = self.impl._key['p'].size_in_bytes()
        if size == 128:
            return 40
        elif size == 256:
            return 56
        else:
            raise Exception("DSA Key size is not 128B nor 256B!")

    def __bytes__(self) -> bytes:
        return self.impl.export_key()
