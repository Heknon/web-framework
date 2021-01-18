from typing import TypeVar, Generic

T = TypeVar("T")


class HttpHeader(Generic[T]):
    def __init__(self, name: str, value: T):
        self.name = name
        self.value = value

    def __str__(self):
        return f"HttpHeader(name: {self.name}, value: {self.value})"
