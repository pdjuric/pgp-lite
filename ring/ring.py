from builtins import type
from typing import TypeVar, Generic, Optional

from codes import Code
from exceptions import UnknownKeyID

RingEntry = TypeVar("RingEntry")


class Ring(Generic[RingEntry]):

    def __init__(self):
        self._index_by_key: dict[bytes, RingEntry] = {}
        self._index_by_pka_code: dict[Code, list[RingEntry]] = {}

    def get_all(self) -> list[RingEntry]:
        return list(self._index_by_key.values())

    def get_by_key_ID(self, key_ID: bytes) -> RingEntry:
        try:
            return self._index_by_key[key_ID]
        except KeyError:
            raise UnknownKeyID(key_ID)

    def get_by_pka_code(self, pka_code: Code) -> list[RingEntry]:
        try:
            return self._index_by_pka_code[pka_code]
        except KeyError:
            return []

    def add(self, entry: RingEntry):
        self._index_by_key[entry.public_key.get_key_ID()] = entry
        bucket = self.get_by_pka_code(entry.get_pka_code())
        bucket.append(entry)
        self._index_by_pka_code[entry.get_pka_code()] = bucket

    def remove(self, key_ID: bytes):
        entry = self._index_by_key[key_ID]
        del self._index_by_key[key_ID]
        bucket = self.get_by_pka_code(entry.get_pka_code())
        bucket.remove(entry)
        self._index_by_pka_code[entry.get_pka_code()] = bucket
