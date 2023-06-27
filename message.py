from typing import Optional


class Message:

    def __init__(self, payload: bytearray, op1:str="", op2:str=""):
        self.set_bytes(payload)
        self.cursor = 0
        self.data: [bytes] = [payload]
        self.dirty_bit = False
        self.timestamp = None

    def __init__(self, msg: str, timestamp: Optional[int] = None):
        payload = bytes(msg, 'utf-8')
        self.timestamp = timestamp
        self.set_bytes(payload)
        self.cursor = 0
        self.data: [bytes] = [payload]
        self.dirty_bit = False
        self.timestamp = None

    def __set_dirty_bit(self):
        self.dirty_bit = True

    def __reset_dirty_bit(self):
        if not self.dirty_bit:
            return

        self.data = [b''.join(self.data)]
        self.dirty_bit = False

    def reset_cursor(self):
        self.cursor = 0

    def move_cursor(self, offset: int):
        self.cursor += offset

    def get_bytes(self, length: int) -> bytes:
        self.__reset_dirty_bit()

        if length == 0:
            return self.data[0]

        if length > 0 and self.cursor + length > len(self.data[0]):
            raise RuntimeError("Message.get_bytes - Invalid length")

        bytes_to_return = self.data[0][self.cursor: self.cursor + length]
        self.cursor += length
        return bytes_to_return

    def get_remaining_bytes(self) -> bytes:
        bytes_to_return = self.data[0][self.cursor:]
        self.cursor = len(self.data[0])
        return bytes_to_return

    def append(self, data: bytes):
        self.dirty_bit = True
        self.data.append(data)

    def prepend(self, data: bytes):
        self.dirty_bit = True
        self.data.insert(0, data)
        self.cursor += len(data)

    def set_bytes(self, data: bytes):
        self.data = [data]
        self.cursor = 0
        self.dirty_bit = False
