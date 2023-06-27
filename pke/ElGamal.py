import random
import re

from Crypto.Math._IntegerGMP import IntegerGMP
from Crypto.PublicKey.ElGamal import ElGamalKey, generate, construct
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from pke.algorithm import PublicKeyAlgorithm
from pke.key import PublicKey, PrivateKey
from codes import Code
from binascii import hexlify, unhexlify

IntegerCustomZero = IntegerGMP(0)
IntegerCustomOne = IntegerGMP(1)


def egcd(a, b) -> (IntegerGMP, IntegerGMP, IntegerGMP):
    x, y, u, v = IntegerCustomZero, IntegerCustomOne, IntegerCustomOne, IntegerCustomZero
    while a != IntegerCustomZero:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return b, x, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != IntegerCustomOne:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def remove_key_boundary(data: bytes) -> bytes:
    r = re.compile(r"-----BEGIN([^-]*)-----\n([^\n]*)\n-----END([^-]*)-----")
    m = r.match(data.decode())
    if not m:
        raise ValueError("Not a valid PEM pre boundary")
    marker = m.group(2)

    return unhexlify(bytes(marker, 'utf-8'))


class ElGamalAlgorithm(PublicKeyAlgorithm):

    def generate_keys(self, key_size: int) -> (PrivateKey, PublicKey):
        private_impl = generate(key_size, get_random_bytes)
        public_impl = private_impl.publickey()
        public = ElGamalPublicKey(public_impl)
        private = ElGamalPrivateKey(private_impl, public.get_key_ID())
        return private, public

    def load_private_key(self, data: bytes) -> (PrivateKey, PublicKey):
        private_impl = construct(self.__get_components(remove_key_boundary(data), 4))
        public_impl = private_impl.publickey()

        public = ElGamalPublicKey(public_impl)
        private = ElGamalPrivateKey(private_impl, public.get_key_ID())

        return private, public

    def load_public_key(self, data: bytes) -> PublicKey:
        public_impl = construct(self.__get_components(remove_key_boundary(data), 3))
        return ElGamalPublicKey(public_impl)

    def get_code(self) -> Code:
        return Code.ElGamal

    @staticmethod
    def __get_components(data: bytes, count: int) -> tuple:
        sizes = [int.from_bytes(data[2 * i: 2 * i + 2], "big") for i in range(count)]
        seek = count * 2

        comps = []
        for size in sizes:
            t = data[seek: seek + size]
            comps.append(int.from_bytes(t, "big"))
            seek += size

        return tuple(comps)


class ElGamalPrivateKey(PrivateKey):

    def __init__(self, impl: ElGamalKey, key_ID: bytes):
        self.impl = impl
        super().__init__(key_ID)

    def sign(self, data: bytes) -> bytes:
        raise Exception("Unsupported operation: ElGamalPrivateKey.sign")

    def decrypt(self, ciphertext: bytes) -> bytes:
        ciphertext = bytearray(ciphertext)
        plaintext = bytearray()
        block_size = self.impl.p.size_in_bytes()
        p = self.impl.p
        d = self.impl.x
        for (r, t) in [(ciphertext[2 * i * block_size: (2 * i + 1) * block_size],
                        ciphertext[(2 * i + 1) * block_size: (2 * i + 2) * block_size])
                       for i in range(len(ciphertext) // (2 * block_size))]:
            inv = modinv(IntegerGMP.from_bytes(r), p)
            m = (pow(inv, d, p) * IntegerGMP.from_bytes(t)) % p
            plaintext += IntegerGMP.to_bytes(m)

        return unpad(plaintext, block_size)

    def get_algorithm_code(self) -> Code:
        return Code.ElGamal

    def __bytes__(self) -> bytes:
        comps = [getattr(self.impl, comp) for comp in ('p', 'g', 'y', 'x')]
        arr = bytearray()
        for component_size in [c.size_in_bytes().to_bytes(2, "big") for c in comps]:
            arr.extend(component_size)

        for component in [int(c).to_bytes(c.size_in_bytes(), "big") for c in comps]:
            arr.extend(component)

        res = bytearray()
        res.extend(bytes("-----BEGIN ELGAMAL PRIVATE KEY-----\n", 'utf-8'))
        res.extend(hexlify(bytes(arr)))
        res.extend(bytes("\n-----END ELGAMAL PRIVATE KEY-----", 'utf-8'))
        return bytes(res)


class ElGamalPublicKey(PublicKey):

    def __init__(self, impl: ElGamalKey):
        self.impl = impl

    def verify(self, data: bytes, signature: bytes) -> bool:
        raise Exception("Unsupported operation: ElGamalPublicKey.verify")

    def encrypt(self, data: bytes) -> bytes:
        data = bytearray(data)
        ciphertext = bytearray()
        block_size = self.impl.p.size_in_bytes()
        padded_data = pad(data, block_size)
        p = self.impl.p
        a = self.impl.g
        b = self.impl.y
        for chunk in [padded_data[i * block_size: (i + 1) * block_size] for i in range(len(padded_data) // block_size)]:
            k = random.randint(0, p - 1)
            r = IntegerGMP(pow(a, k, p)).to_bytes(0, 'big')
            t1 = pow(b, k, p)
            t = IntegerGMP.to_bytes((IntegerGMP.from_bytes(chunk, 'big') * t1) % p)
            ciphertext += r + t

        return ciphertext

    def get_key_ID(self) -> bytes:
        return (int(self.impl.y) % (1 << 64)).to_bytes(8, "big")

    def get_signature_size(self) -> int:
        return self.impl.p.size_in_bytes() * 2

    def get_algorithm_code(self) -> Code:
        return Code.ElGamal

    def __bytes__(self) -> bytes:
        comps = [getattr(self.impl, comp) for comp in ('p', 'g', 'y')]
        arr = bytearray()

        for component_size in [c.size_in_bytes().to_bytes(2, "big") for c in comps]:
            arr.extend(component_size)

        for component in [int(c).to_bytes(c.size_in_bytes(), "big") for c in comps]:
            arr.extend(component)

        res = bytearray()
        res.extend(bytes("-----BEGIN ELGAMAL KEY-----\n", 'utf-8'))
        res.extend(hexlify(bytes(arr)))
        res.extend(bytes("\n-----END ELGAMAL KEY-----", 'utf-8'))

        return bytes(res)
