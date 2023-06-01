class UnknownKeyID(Exception):
    def __init__(self, key_id):
        self.key_id = key_id

    def __str__(self):
        return "Key with key ID {} not found.".format(self.key_id.hex())


class PrivateKeyDecryptionError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Private key decryption error: {}".format(self.message)


class DecryptionError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Decryption error: {}".format(self.message)


class UnsupportedSymmetricKeyAlgorithm(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Unsupported Symmetric Key Algorithm: {}".format(self.message)


class HashStartMissmatch(Exception):
    def __init__(self, expected, got):
        self.expected = expected
        self.got = got

    def __str__(self):
        return "Hash start missmatch: expected {}, got {}".format(self.expected.hex(), self.got.hex())


class VerificationFailed(Exception):
    def __init__(self, key_id):
        self.key_id = key_id

    def __str__(self):
        return "Verification with key {} failed".format(self.key_id.hex())
