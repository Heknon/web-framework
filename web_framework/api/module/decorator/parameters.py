import re
import urllib.parse
from collections import Iterable

from web_framework import HttpRequest
from web_framework.api.module import MethodContentType
from . import Parameter


class QueryParameter(Parameter):
    def __init__(self, parameter_type: type, name: str = None, content_type=None, default_value: object = None, required: bool = False):
        super().__init__(parameter_type, name, content_type, default_value, required)

    def get_value_from_request(self, request: HttpRequest, api_registry) -> [bytes]:
        if request.query_parameters is None:
            return None
        val = request.query_parameters.get(self.name, None)
        if val is not None and not isinstance(val, Iterable):
            val = [val]
        return list(map(lambda x: str(x).encode(), val)) if val is not None else None


class RequestBody(Parameter):
    def __init__(self, parameter_type: type, name: str = None, content_type=None, default_value: object = None, required: bool = False):
        super().__init__(parameter_type, name, content_type, default_value, required)

    def get_value_from_request(self, request: HttpRequest, api_registry) -> [bytes]:
        if request.body is None:
            return None
        val = request.body
        if val is not None and not isinstance(val, Iterable):
            val = [val]
        return val


class PathVariable(Parameter):
    def __init__(self, parameter_type: type = str, name: str = None, content_type=MethodContentType.TEXT, default_value: object = None,
                 required: bool = False):
        super().__init__(parameter_type, name, content_type, default_value, required)

    def get_value_from_request(self, request: HttpRequest, api_registry) -> [bytes]:
        path = api_registry.api_module_coordinator.parameter_method_cache[request.url][1]
        res = self.rescue_path_variables(path, request.url)
        if res is None:
            return None
        else:
            return [urllib.parse.unquote(res).encode()]

    def rescue_path_variables(self, path, url) -> str:
        c = re.compile('{(.*?)}')
        offset = 0
        values = {}

        for match in c.finditer(path):
            start_in_path = match.start()
            path_string = match.group()
            end_in_url = start_in_path + offset
            while end_in_url < len(url) and url[end_in_url] != '/':
                end_in_url += 1

            values[path_string[1:-1]] = url[start_in_path + offset:end_in_url]
            offset = end_in_url - (start_in_path + offset) - len(path_string)

        return values.get(self.name, self.default_value)
