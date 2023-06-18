
def create_rings():
    from .private import PrivateRingEntry
    from .public import PublicRingEntry
    from .ring import Ring

    return Ring[PrivateRingEntry](), Ring[PublicRingEntry]()


PrivateRing, PublicRing = create_rings()

def import_private_entry(filename: str, passphrase: bytes):
    from pke.ElGamal import ElGamalAlgorithm
    from pke.DSA import DSAAlgorithm
    from pke.RSA import RSAAlgorithm
    from pke.key import EncryptedPrivateKey
    from ring.private import PrivateRingEntry
    from datetime import datetime

    with open(filename, 'rb') as file:
        imported_key = file.read()
        print(imported_key)
        import re
        patern = r"-----BEGIN USER INFO-----\n([^-]*)\n-----END USER INFO-----\n(.*)$"
        m = re.search(patern, imported_key.decode(), re.DOTALL)
        if not m:
            raise ValueError("Not a valid PEM pre boundary")
        user = m.group(1)
        key = m.group(2)

        keyTypePatern = r"-----BEGIN (.*) KEY-----\n([^-]*)"
        m = re.search(keyTypePatern, key, re.DOTALL)
        if not m:
            raise ValueError("Not a valid PEM pre boundary")
        keyType = m.group(1)

        if not keyType.count('PRIVATE'):
            raise Exception("Not a valid key type.")

        if keyType.count('ELGAMAL'):
            algorithm = ElGamalAlgorithm()
        elif keyType.count('RSA'):
            algorithm = RSAAlgorithm()
        else:
            algorithm = DSAAlgorithm()

        private_key, public_key = algorithm.load_private_key(key)
        encrypted_private_key = EncryptedPrivateKey(private_key, algorithm.get_code(), passphrase)
        private_key_entry = PrivateRingEntry(user, encrypted_private_key, public_key, int(datetime.now().timestamp()))
        PrivateRing.add(private_key_entry)


def import_public_entry(filename: str):
    from pke.ElGamal import ElGamalAlgorithm
    from pke.DSA import DSAAlgorithm
    from pke.RSA import RSAAlgorithm
    from ring.public import PublicRingEntry
    from datetime import datetime

    with open(filename, 'rb') as file:
        imported_key = file.read()
        print(imported_key)
        import re
        patern = r"-----BEGIN USER INFO-----\n([^-]*)\n-----END USER INFO-----\n(.*)$"
        m = re.search(patern, imported_key.decode(), re.DOTALL)
        if not m:
            raise ValueError("Not a valid PEM pre boundary")
        user = m.group(1)
        key = m.group(2)

        keyTypePatern = r"-----BEGIN (.*) KEY-----\n([^-]*)"
        m = re.search(keyTypePatern, key, re.DOTALL)
        if not m:
            raise ValueError("Not a valid PEM pre boundary")
        keyType = m.group(1)

        if keyType.count('ELGAMAL'):
            algorithm = ElGamalAlgorithm()
        elif keyType.count('RSA'):
            algorithm = RSAAlgorithm()
        else:
            algorithm = DSAAlgorithm()


        if keyType.count('PRIMARY'):
            _, public_key = algorithm.load_private_key(key)
        else:
            public_key = algorithm.load_public_key(key)
        public_key_entry = PublicRingEntry(user, public_key, int(datetime.now().timestamp()), algorithm.get_code())
        PublicRing.add(public_key_entry)
