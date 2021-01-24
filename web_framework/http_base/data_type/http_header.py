from typing import TypeVar, Generic

T = TypeVar("T")


class HttpHeader(Generic[T]):
    """
    Class for representing an HttpHeader

    Attributes
    ----------
    name : str
        the name of the header
    value : T
        the value of the header
    """

    def __init__(self, name: str, value: T):
        self.name = name
        self.value = value
        
    def clone(self):
        return HttpHeader(self.name, self.value)

    def __str__(self):
        return f"HttpHeader(name: {self.name}, value: {self.value})"
