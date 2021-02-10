from abc import ABC

from web_framework.api.module import MethodContentType
from web_framework.api.type_parsing import TypeAdapter
from typing import TypeVar

T = TypeVar('T')


class TextTypeAdapter(TypeAdapter[T], ABC):
    def __init__(self, adapting_type):
        super().__init__(adapting_type, MethodContentType.TEXT)


class JsonTypeAdapter(TypeAdapter[T], ABC):
    def __init__(self, adapting_type):
        super().__init__(adapting_type, MethodContentType.JSON)


class HtmlTypeAdapter(TypeAdapter[T], ABC):
    def __init__(self, adapting_type):
        super().__init__(adapting_type, MethodContentType.HTML)
