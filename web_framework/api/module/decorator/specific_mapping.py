from typing import Callable

from web_framework.api.module import MethodContentType
from web_framework.http_base.data_type import HttpMethod
from . import RequestMappingMeta, RequestMapping


class GetMapping(RequestMapping):
    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods={}, error_handler=error_handler)
        meta.acceptable_methods = {HttpMethod.GET}
        super().__init__(meta=meta)


class PostMapping(RequestMapping):
    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods={}, error_handler=error_handler)
        meta.acceptable_methods = {HttpMethod.POST}
        super().__init__(meta=meta)


class PutMapping(RequestMapping):
    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods={}, error_handler=error_handler)
        meta.acceptable_methods = {HttpMethod.PUT}
        super().__init__(meta=meta)


class PatchMapping(RequestMapping):
    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods={}, error_handler=error_handler)
        meta.acceptable_methods = {HttpMethod.PATCH}
        super().__init__(meta=meta)


class DeleteMapping(RequestMapping):
    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods={}, error_handler=error_handler)
        meta.acceptable_methods = {HttpMethod.DELETE}
        super().__init__(meta=meta)


class HeadMapping(RequestMapping):
    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods={}, error_handler=error_handler)
        meta.acceptable_methods = {HttpMethod.HEAD}
        super().__init__(meta=meta)


class ConnectMapping(RequestMapping):
    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods={}, error_handler=error_handler)
        meta.acceptable_methods = {HttpMethod.CONNECT}
        super().__init__(meta=meta)


class OptionsMapping(RequestMapping):
    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods={}, error_handler=error_handler)
        meta.acceptable_methods = {HttpMethod.OPTIONS}
        super().__init__(meta=meta)


class TraceMapping(RequestMapping):
    def __init__(self, *routes: str, content_type: MethodContentType = MethodContentType.JSON, error_handler: Callable[[Exception], object] = None, meta: RequestMappingMeta = None):
        if meta is None:
            meta = RequestMappingMeta(*routes, content_type=content_type, acceptable_methods={}, error_handler=error_handler)
        meta.acceptable_methods = {HttpMethod.TRACE}
        super().__init__(meta=meta)
