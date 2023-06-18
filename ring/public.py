from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from config import CONST_X, CONST_Y
from pke.key import *


class PublicRingEntry:

    def __init__(self, user: User, public_key: PublicKey, timestamp: datetime, pka_code: Code):
        self.timestamp = timestamp
        self.public_key = public_key
        self.user = user
        self._signatures = []
        self.pka_code = pka_code

    def add_signature(self, signature: User) -> bool:
        if signature in self._signatures:
            return False
        else:
            self._signatures.append(signature)
            return True

    def get_signatures(self) -> list[User]:
        return self._signatures

    def get_key_legitimacy(self) -> bool:
        return sum([int(user.get_trust()) for user in self._signatures]) >= Trust.get_minimal_trust()

    def get_key_ID(self) -> bytes:
        return self.public_key.get_key_ID()

    def export(self, filename):
        res = bytearray()

        res.extend(bytes("-----BEGIN USER INFO-----\n", 'utf-8'))
        res.extend(bytes(self.user, 'utf-8'))
        res.extend(bytes("\n-----END USER INFO-----\n", 'utf-8'))

        res.extend(bytes(self.public_key))

        with open(filename, 'wb') as file:
            file.write(bytes(res))

    def get_pka_code(self) -> Code:
        return self.pka_code

class User:

    all_users: dict[str: User] = {}

    def __init__(self, id: str):
        self.ID = id
        self.trust = Trust.UNKNOWN
        self.public_ring_entry: Optional[PublicRingEntry] = None

    @staticmethod
    def get(user_id: str) -> User:
        # todo should a new user be created?
        try:
            return User.all_users[user_id]
        except KeyError:
            new_user = User(user_id)
            User.all_users[user_id] = new_user
            return new_user

    @staticmethod
    def exists(user_id: str) -> bool:
        return user_id in User.all_users


class Trust(Enum):

    def __new__(cls, *args):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, name: str, value: int):
        self._name_ = name
        self._value_ = value

    def __int__(self):
        return self._value_

    def __str__(self):
        return self._name_

    UNKNOWN = 'unknown', 0
    NO_TRUST = 'untrusted', 0
    PARTIAL_TRUST = 'partially trusted', CONST_Y
    FULL_TRUST = 'fully trusted', CONST_X

    @staticmethod
    def get_minimal_trust() -> int:
        return CONST_Y * CONST_X
