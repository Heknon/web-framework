from typing import Callable

from web_framework.api.module import ApiModule
from web_framework.utils import has_meta_attribute


class ApiModuleCoordinator:
    def __init__(self, api_registry):
        self.api_registry = api_registry
        self.registered_modules = self.filter_and_get_registered_modules()
        self.full_route_method_map = self.get_url_method_map()
        self.conditional_routes = self.get_conditional_routes()
        self.__type_decoders = set()
        self.__type_encoders = set()

    def get_conditional_routes(self):
        res = {}
        for i in self.registered_modules:
            for r in i.meta.routes:
                res[i.normalize_route(r, False)] = i.conditional_routes

        return res

    def get_url_method_map(self) -> {str: Callable}:
        url_method_map = {}
        module: ApiModule
        for module in self.registered_modules:
            for method, routes in module.method_full_route_map.items():
                for route in routes:
                    url_method_map[route] = method

        return url_method_map

    def find_matching_method(self, url: str) -> Callable:
        if url not in self.full_route_method_map:
            return None
        else:
            return self.full_route_method_map[url]

    def filter_and_get_registered_modules(self) -> {ApiModule}:
        modules = set()
        for clazz in self.api_registry.registered_classes:
            if has_meta_attribute(clazz):
                modules.add(ApiModule(clazz))

        return modules
