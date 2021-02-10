from typing import TypeVar, Generic

from web_framework.api.module import MethodContentType

T = TypeVar('T')


class TypeAdapter(Generic[T]):
    def __init__(self, adapting_type, content_type: MethodContentType):
        self.adapting_type = adapting_type
        self.content_type = content_type

    def decode(self, data: bytes) -> T:
        raise NotImplementedError(f"Must implement decoder for type {type(T)}")

    def encode(self, data: T) -> bytes:
        raise NotImplementedError(f"Must implement encoder for type {type(T)}")

    def __str__(self):
        return f"TypeAdapter(adapting_type: {self.adapting_type}, content_type: {self.content_type})"
