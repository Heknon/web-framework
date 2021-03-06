import traceback
from typing import Callable

from web_framework.http_base import HttpResponse
from web_framework.api.module import Parameter
from web_framework.utils import get_meta_attribute, has_meta_attribute, get_base_classes


class ApiMethodExecutor:
    def __init__(self, method: Callable, api_registry, response, client):
        if not has_meta_attribute(method):
            raise RuntimeError(f"Method passed does not have method meta! {method}")
        self.method = method
        self.api_registry = api_registry
        self.response = response
        self.client = client
        self.meta = get_meta_attribute(method)
        self.content_type = self.meta.content_type
        self.parent = getattr(self.meta, 'parent')

    def execute(self, request) -> bytes:
        try:
            result = self.method(**self.get_results(request))
            result_type = type(result)
            adapter = self.api_registry.adapter_container.find_type_adapter(result_type, self.content_type)
            return adapter.encode(result)
        except Exception as error:
            print(traceback.format_exc())
            if self.meta.error_handler is None:
                return b""
            result = self.meta.error_handler(error, **self.get_results(request))
            result_type = type(error)
            adapter = self.api_registry.adapter_container.find_type_adapter(result_type, self.content_type)
            return adapter.encode(result)

    def get_results(self, request):
        results = {}
        from web_framework import HttpRequest, HttpClient
        for n, value in self.method.__annotations__.items():
            if n == 'return':
                continue
            if value is HttpRequest:
                results[n] = request
                continue
            elif value is HttpClient:
                results[n] = self.client
                continue
            elif value is HttpResponse:
                results[n] = self.response
                continue
            if Parameter in get_base_classes(value) and value.name is None:
                value.name = n
            name, result = value.parse(method=self.method, request=request, api_registry=self.api_registry)
            results[name] = result
        return results
