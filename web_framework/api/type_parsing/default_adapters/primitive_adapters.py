from web_framework.api.type_parsing import TextTypeAdapter


class IntegerTextAdapter(TextTypeAdapter[int]):
    def __init__(self):
        super().__init__(int)

    def decode(self, data: bytes) -> int:
        return int(data.decode())

    def encode(self, data: int) -> bytes:
        return str(data).encode()


class FloatTextAdapter(TextTypeAdapter[float]):
    def __init__(self):
        super().__init__(float)

    def decode(self, data: bytes) -> float:
        return float(data.decode())

    def encode(self, data: float) -> bytes:
        return str(data).encode()


class BooleanTextAdapter(TextTypeAdapter[bool]):
    def __init__(self):
        super().__init__(bool)

    def decode(self, data: bytes) -> bool:
        return bool(data.decode())

    def encode(self, data: bool) -> bytes:
        return str(data).encode()


class StringTextAdapter(TextTypeAdapter[str]):
    def __init__(self):
        super().__init__(str)

    def decode(self, data: bytes) -> str:
        return data.decode()

    def encode(self, data: str) -> bytes:
        return data.encode()


class BytesTextAdapter(TextTypeAdapter[bytes]):
    def __init__(self):
        super().__init__(bytes)

    def decode(self, data: bytes) -> bytes:
        return data

    def encode(self, data: bytes) -> bytes:
        return data


class ObjectTextAdapter(TextTypeAdapter[object]):
    def __init__(self):
        super().__init__(object)

    def decode(self, data: bytes) -> object:
        raise NotImplementedError("Cannot decode unknown object from bytes")

    def encode(self, data: object) -> bytes:
        return str(data).encode()
