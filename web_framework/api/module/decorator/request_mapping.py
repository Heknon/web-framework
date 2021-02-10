from typing import Callable

from web_framework import HttpMethod
from web_framework.api.module import MethodContentType
from ..decorator import RequestMappingMeta
from web_framework.utils import set_meta_attribute


class RequestMapping:
    """
    URL filtering
    Acceptable http methods
    Error handling
    """

    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, acceptable_methods: {HttpMethod} = {},
                 error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods=acceptable_methods, error_handler=error_handler)
        self.meta = meta

    def __call__(self, t):
        return set_meta_attribute(t, self.meta)
