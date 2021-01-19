from typing import Callable

from web_framework.utils import has_meta_attribute, get_meta_attribute, has_conditional_handler


class ApiModule:
    __all_routes = set()

    def __init__(self, clazz):
        if not has_meta_attribute(clazz):
            raise RuntimeError(f"Cannot find meta attribute on class {clazz}. Add RequestMapping.")
        self.meta = get_meta_attribute(clazz)
        for i in self.meta.routes:
            if i in self.__all_routes:
                raise RuntimeError(f"Duplicate route use detected between classes ({clazz} and other class)")
            ApiModule.__all_routes.add(i)
        self.clazz = clazz
        self.conditional_routes = []
        self.module_methods = self.get_module_methods()
        self.method_full_route_map = {method: self.get_full_method_routes(method) for method in self.module_methods}
        self.__duplicate_route_check()

    def __duplicate_route_check(self):
        all_routes = set()
        for method, routes in self.method_full_route_map.items():
            for route in routes:
                if route in all_routes:
                    raise RuntimeError(f"Duplicate route use detected between methods in {self.clazz} ({route})")
                all_routes.add(route)

    def get_matching_methods(self, url: str) -> [Callable]:
        methods = []
        for method in self.module_methods:
            full_routes = self.method_full_route_map[method]
            if url in full_routes:
                methods.append(method)
        return methods

    def get_full_method_routes(self, method) -> {str}:
        routes = set()
        method_meta = get_meta_attribute(method)
        for class_route in self.meta.routes:
            for method_route in method_meta.routes:
                route = self.normalize_route(class_route, True) + self.normalize_route(method_route, False)
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

    def get_module_methods(self) -> [Callable]:
        applicable_methods = []
        for attribute in dir(self.clazz):
            method = getattr(self.clazz, attribute)
            if has_meta_attribute(method):
                setattr(get_meta_attribute(method), 'parent', self)
                applicable_methods.append(method)
            if has_conditional_handler(method):
                self.conditional_routes.append(method)
        return applicable_methods
