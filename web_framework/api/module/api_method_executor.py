import traceback
from typing import Callable

from web_framework.api.module import Parameter
from web_framework.utils import get_meta_attribute, has_meta_attribute, get_base_classes


class ApiMethodExecutor:
    def __init__(self, method: Callable, adapter_container, client):
        if not has_meta_attribute(method):
            raise RuntimeError(f"Method passed does not have method meta! {method}")
        self.method = method
        self.adapter_container = adapter_container
        self.client = client
        self.meta = get_meta_attribute(method)
        self.content_type = self.meta.content_type
        self.parent = getattr(self.meta, 'parent')

    def execute(self, request) -> bytes:
        try:
            result = self.method(**self.get_results(request, self.client))
            result_type = type(result)
            adapter = self.adapter_container.find_type_adapter(result_type, self.content_type)
            return adapter.encode(result)
        except Exception as error:
            print(traceback.format_exc())
            result = self.meta.error_handler(error, **self.get_results(request, self.client))
            result_type = type(error)
            adapter = self.adapter_container.find_type_adapter(result_type, self.content_type)
            return adapter.encode(result)

    def get_results(self, request, client):
        results = {}
        from web_framework import HttpRequest, HttpClient
        for n, value in self.method.__annotations__.items():
            if value is HttpRequest:
                results[n] = request
                break
            elif value is HttpClient:
                results[n] = client
                break
            if Parameter in get_base_classes(value) and value.name is None:
                value.name = n
            name, result = value.parse(method=self.method, request=request, adapter_container=self.adapter_container)
            results[name] = result
        return results
