from enum import Enum


class Code(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    RSA = 'RSA'
    DSA = 'DSA'
    ElGamal = 'ElGamal'
