from typing import Callable, Tuple

from web_framework.api.module import MethodReturnContentType


class RequestMappingMeta:
    def __init__(self, *routes: str,
                 content_type: MethodReturnContentType = MethodReturnContentType.JSON,
                 acceptable_methods=None, error_handler: Callable[[Exception], object] = None):
        self.routes = routes
        self.content_type = content_type
        self.acceptable_methods = acceptable_methods
        self.error_handler = error_handler

    def __str__(self):
        return f"RequestMappingMeta(routes: {self.routes}, content_type: {self.content_type}, acceptable_methods: {self.acceptable_methods})"
