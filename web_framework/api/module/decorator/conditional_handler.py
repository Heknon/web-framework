from typing import Callable

from web_framework.http_base import HttpRequest
from web_framework.utils import set_conditional_handler


class ConditionalHandler:
    def __init__(self, condition: Callable[[HttpRequest], bool]):
        self.condition = condition

    def __call__(self, t):
        return set_conditional_handler(t, self.condition)
