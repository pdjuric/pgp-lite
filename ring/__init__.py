from datetime import datetime
import re

from pke.algorithm import PublicKeyAlgorithm
from pke.key import EncryptedPrivateKey, PrivateKey, PublicKey
from ring.private import PrivateRingEntry
from ring.public import User, PublicRingEntry


def create_rings():
    from .private import PrivateRingEntry
    from .public import PublicRingEntry
    from .ring import Ring

    return Ring[PrivateRingEntry](), Ring[PublicRingEntry]()


PrivateRing, PublicRing = create_rings()


# bool is True if the key is private
def load_key_info(filename: str) -> (str, bool, PublicKeyAlgorithm, (PrivateKey, PublicKey)):
    from pke.ElGamal import ElGamalAlgorithm
    from pke.DSA import DSAAlgorithm
    from pke.RSA import RSAAlgorithm
    from ring.private import PrivateRingEntry

    with open(filename, 'rb') as file:
        pattern = r"-----BEGIN USER INFO-----\n([^\n]*)\n-----END USER INFO-----\n(.*)$"
        m = re.search(pattern, file.read().decode(), re.DOTALL)
        if not m:
            raise ValueError("Not a valid PEM pre boundary")
        user = m.group(1)
        key = m.group(2)

        key_type_pattern = r"-----BEGIN (.*) KEY-----\n([^-]*)"
        m = re.search(key_type_pattern, key, re.DOTALL)
        if not m:
            raise ValueError("Not a valid PEM pre boundary")
        key_type = m.group(1)

        if key_type.count('ELGAMAL'):
            algorithm = ElGamalAlgorithm()
            key = bytes(key, 'utf-8')
        elif key_type.count('RSA'):
            algorithm = RSAAlgorithm()
            key = key.replace('RSA ', '')
        else:
            algorithm = DSAAlgorithm()

        if key_type.count('PRIVATE') > 0:
            private_key, public_key = algorithm.load_private_key(key)
        else:
            private_key, public_key = None, algorithm.load_public_key(key)

        return user, key_type.count('PRIVATE') > 0, algorithm, (private_key, public_key)


def import_private_entry(user: str, is_private: bool, algorithm: PublicKeyAlgorithm, keys, passphrase: bytes):
    if not is_private:
        raise Exception("Not a private key!")

    encrypted_private_key = EncryptedPrivateKey(keys[0], algorithm.get_code(), passphrase)
    private_key_entry = PrivateRingEntry(user, encrypted_private_key, keys[1], datetime.now())
    PrivateRing.add(private_key_entry)


def import_public_entry(user: User, is_private: bool, algorithm: PublicKeyAlgorithm, keys):
    if is_private:
        raise ValueError("Not a public key!")

    public_key_entry = PublicRingEntry(user, keys[1], datetime.now(), algorithm.get_code())
    PublicRing.add(public_key_entry)
