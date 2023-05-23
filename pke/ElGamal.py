from Crypto.PublicKey.ElGamal import ElGamalKey, generate, construct
from Crypto.Random import get_random_bytes

from pke.algorithm import PublicKeyAlgorithm
from pke.key import PublicKey, PrivateKey
from code import Code


class ElGamalAlgorithm(PublicKeyAlgorithm):

    def generate_keys(self, key_size: int) -> (PrivateKey, PublicKey):
        # todo check possible key sizes

        private_impl = generate(key_size, get_random_bytes)
        public_impl = private_impl.publickey()

        public = ElGamalPublicKey(public_impl)
        private = ElGamalPrivateKey(private_impl, public.get_key_ID())

        return public, private

    def load_private_key(self, data: bytes) -> (PrivateKey, PublicKey):
        private_impl = construct(*self.__get_components(data, 4))
        public_impl = private_impl.publickey()

        public = ElGamalPublicKey(public_impl)
        private = ElGamalPrivateKey(private_impl, public.get_key_ID())

        return public, private

    def load_public_key(self, data: bytes) -> PublicKey:
        public_impl = construct(*self.__get_components(data, 3))
        return ElGamalPublicKey(public_impl)

    def get_code(self) -> Code:
        return Code.ElGamal

    @staticmethod
    def __get_components(data: bytes, count: int) -> list[int]:
        sizes = [int.from_bytes(data[2 * i: 2 * i + 2], "big") for i in range(count)]
        seek = count * 2

        comps = []
        for size in sizes:
            t = data[seek: seek + size]
            comps.append(int.from_bytes(t, "big"))
            seek += size

        return comps


class ElGamalPrivateKey(PrivateKey):

    def __init__(self, impl: ElGamalKey, key_ID: bytes):
        self.impl = impl
        super().__init__(key_ID)

    def sign(self, data: bytes) -> bytes:
        raise Exception("Unsupported operation: ElGamalPrivateKey.sign")

    def decrypt(self, ciphertext: bytes) -> bytes:
        # TODO: implement
        raise NotImplementedError

    def __bytes__(self) -> bytes:
        comps = [getattr(self.impl, comp) for comp in ('p', 'g', 'y', 'x')]
        arr = bytearray()

        for component_size in [c.size_in_bytes().to_bytes(2, "big") for c in comps]:
            arr.extend(component_size)

        for component in [int(c).to_bytes(c.size_in_bytes(), "big") for c in comps]:
            arr.extend(component)

        return arr


class ElGamalPublicKey(PublicKey):

    def __init__(self, impl: ElGamalKey):
        self.impl = impl

    def verify(self, data: bytes, signature: bytes) -> bool:
        raise Exception("Unsupported operation: ElGamalPublicKey.verify")

    def encrypt(self, data: bytes) -> bytes:
        # TODO: implement
        raise NotImplementedError

    def get_key_ID(self) -> bytes:
        return (int(self.impl.y) % (1 << 64)).to_bytes(8, "big")
        # int(key.y).to_bytes(key.y.size_in_bytes(), "big")[-8:]

    def get_signature_size(self) -> int:
        raise Exception("Unsupported operation: ElGamalPublicKey.get_signature_size")

    def __bytes__(self) -> bytes:
        comps = [getattr(self.impl, comp) for comp in ('p', 'g', 'y')]
        arr = bytearray()

        for component_size in [c.size_in_bytes().to_bytes(2, "big") for c in comps]:
            arr.extend(component_size)

        for component in [int(c).to_bytes(c.size_in_bytes(), "big") for c in comps]:
            arr.extend(component)

        return arr
