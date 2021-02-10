import json

from web_framework.api.type_parsing import TypeAdapter
from web_framework.api.module import MethodContentType


class JsonObjectTypeAdapter(TypeAdapter[object]):
    def __init__(self):
        super().__init__(object, MethodContentType.JSON)

    def decode(self, data: bytes) -> object:
        return json.loads(data.decode())

    def encode(self, data: object) -> bytes:
        return json.dumps(data).encode()
