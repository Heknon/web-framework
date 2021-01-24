from abc import ABC
from typing import Callable

from web_framework.api.module.decorator import RequestMappingMeta
from web_framework.utils import has_meta_attribute, get_meta_attribute, has_conditional_handler
import inspect


class ApiModule(ABC):
    __all_routes = set()

    def __init__(self, callable_object):
        self.callable_object = callable_object
        self.is_class = '.' in callable_object.__qualname__

        if not has_meta_attribute(callable_object):
            raise RuntimeError(f"Cannot find meta attribute on {'class' if self.is_class else 'function'} {callable_object}. Add RequestMapping.")

        self.meta: RequestMappingMeta = get_meta_attribute(callable_object)

        self.encapsulated_methods = self.get_encapsulated_methods()
        self.conditional_routes = self.__get_conditional_routes()
        self.route_method_association = self.__get_routes_function_association()

    def get_encapsulated_methods(self):
        raise NotImplementedError(f"Must implement get_encapsulated_methods() in {self.__class__}")

    def get_parent(self):
        raise NotImplementedError(f"Must implement get_parent() in {self.__class__}")

    def request_method_acceptable(self, method, request) -> bool:
        parent = self.get_parent()
        method_meta = get_meta_attribute(method)
        method_http_methods_contains_method = self.meta.acceptable_methods is not None and request.method in method_meta.acceptable_methods

        if parent is not None:
            class_http_methods_contains_method = self.meta.acceptable_methods is not None and request.method in self.meta.acceptable_methods
            return method_http_methods_contains_method or class_http_methods_contains_method
        else:
            return method_http_methods_contains_method

    def __get_conditional_routes(self):
        res = set()

        for method in self.encapsulated_methods:
            if not has_conditional_handler(method):
                continue
            res.add(method)

        return res

    def __get_routes_function_association(self):
        return {method: self.__get_function_routes(method) for method in self.encapsulated_methods}

    def __get_function_routes(self, function):
        if not has_meta_attribute(function):
            raise RuntimeError(f"Cannot find meta attribute on function {function}. Add RequestMapping.")
        if not inspect.isfunction(function) and not inspect.ismethod(function):
            raise RuntimeError(f"Argument passed must be of type function or method!")

        function_meta: RequestMappingMeta = get_meta_attribute(function)
        parent_class = self.get_parent()

        routes = set()
        if parent_class is not None:
            for class_route in self.meta.routes:
                for method_route in function_meta.routes:
                    route = self.normalize_route(class_route, True) + self.normalize_route(method_route, False)
                    routes.add(route)
        else:
            for method_route in function_meta.routes:
                route = self.normalize_route(method_route, False)
                routes.add(route)

        return routes

    @staticmethod
    def normalize_route(route: str, is_class_route: bool) -> str:
        normalized: str = route
        if normalized == '/' and is_class_route:
            return ''
        elif normalized == '/' or normalized == '':
            return '/'
        if normalized[len(normalized) - 1] == '/':
            normalized = normalized[0:len(normalized) - 1]
        if normalized[0] != '/':
            normalized = '/' + normalized[0::]
        return normalized


class ApiClassModule(ApiModule):

    def get_parent(self):
        return self

    def get_encapsulated_methods(self):
        applicable_methods = []
        for attribute in dir(self.callable_object):
            method = getattr(self.callable_object, attribute)
            if has_meta_attribute(method):
                setattr(get_meta_attribute(method), 'parent', self)
                applicable_methods.append(method)
        return applicable_methods


class ApiMethodModule(ApiModule):
    def get_parent(self):
        return None

    def get_encapsulated_methods(self):
        setattr(get_meta_attribute(self.callable_object), 'parent', self)
        return [self.callable_object]
