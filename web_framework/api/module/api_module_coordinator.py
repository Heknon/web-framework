import inspect
import os
import re
from typing import Callable

from web_framework.api.module import ApiModule, ApiClassModule, ApiMethodModule
from web_framework.utils import has_meta_attribute, get_conditional_handler


class ApiModuleCoordinator:
    """
    Allows for the coordination of the activities of the api modules

    Creates the APIModule objects along with routing maps

    Attributes
    ----------
    registered_modules : {ApiModule}
        the api modules that will be used for route management
    full_route_method_map : {str: Callable}
        route to api method map. given a route you will be able to get its appropriate method
    conditional_routes : {str: Callable}
        route to api method map. given a route you will be able to get its appropriate method for all conditional methods

    Methods
    -------
    find_matching_method(url: str) -> Callable
        find a method matching the route given

    find_conditional_handler_match(request: HttpRequest) -> Callable
        find a method that is marked with a conditional handler that matches the request condition
    """

    def __init__(self, api_registry):
        self._api_registry = api_registry
        self.registered_modules = self._filter_and_get_registered_modules()
        self.full_route_method_map = self._get_url_method_map()
        self.conditional_routes = self._get_conditional_routes()
        self.parameter_method_cache = {}
        self.__type_decoders = set()
        self.__type_encoders = set()

    def find_matching_method(self, url: str, request) -> Callable:
        """
        find a method matching the route given

        :param url: the route to find a method for
        :param request the request
        :return: method or None if no route found
        """

        if url in self.parameter_method_cache:
            return self.parameter_method_cache[url][0]

        has_method_call = url in self.full_route_method_map
        conditional_method = self.find_conditional_handler_match(request)
        path_method = self.find_parameter_match(request)

        if path_method is not None:
            return path_method
        elif conditional_method is not None:
            return conditional_method
        elif has_method_call:
            return self.full_route_method_map[url]
        else:
            return None

    def find_conditional_handler_match(self, request) -> Callable:
        """
        Finds a method route with a conditional handler that matches request made

        :param request: the request to pass to the conditional handlers
        :return: first method to match conditional handler or None if none found
        """

        has_method_call = request.url in self.full_route_method_map

        for class_route, methods in self.conditional_routes.items():
            for method in methods:
                if not has_method_call and request.url.startswith(class_route) and get_conditional_handler(method)(request.clone()):
                    return method
            break
        return None

    def find_parameter_match(self, request):
        """
        finds a route that matches the request url and uses path variables

        :param request: the request
        :return: None if not found otherwise corresponding method
        """

        c = re.compile('{(.*?)}')
        for (path, method) in self.full_route_method_map.items():
            if c.search(path) is not None and self.url_matches_path(path, request.url):
                self.parameter_method_cache[request.url] = (method, path)
                return method

        return None

    def url_matches_path(self, path, url) -> bool:
        """
        Checks if url matches path with path variables

        :param path: the path
        :param url: the url
        :return: true if match otherwise false
        """

        c = re.compile('({(.*?)})')
        offset = 0

        prev_end_url = 0
        prev_end_path = 0
        for match in c.finditer(path):
            start_in_path = match.start()
            path_string = match.group()
            end_in_url = start_in_path + offset
            while end_in_url < len(url) and url[end_in_url] != '/':
                end_in_url += 1

            if url[prev_end_url:start_in_path + offset] != path[prev_end_path:start_in_path]:
                return False

            prev_end_url = end_in_url
            prev_end_path = match.end()
            offset = end_in_url - start_in_path - offset - len(path_string)

        return url[prev_end_url::] == path[prev_end_path::]

    def _get_conditional_routes(self):
        """
        filters out the registered modules and finds all methods matching the conditional meta

        :return: a map with its key being the route and value being the method with conditional meta
        """

        res = {}
        for i in self.registered_modules:
            if len(i.conditional_routes) == 0:
                continue
            conditionals = i.conditional_routes
            routes = i.meta.routes if len(i.meta.routes) != 0 else ['/']
            for r in routes:
                path = i.normalize_route(r, False)
                if path not in res:
                    res[path] = [*conditionals]
                else:
                    for conditional in conditionals:
                        res[path].append(conditional)

        return res

    def _get_url_method_map(self) -> {str: Callable}:
        """
        filters out the registered modules and finds all methods that have request mapping meta

        :return: a map with its key being the route and value being the method with request mapping meta
        """

        url_method_map = {}
        module: ApiModule
        for module in self.registered_modules:
            for method, routes in module.route_method_association.items():
                for route in routes:
                    if route in url_method_map:
                        raise RuntimeError(
                            f"Duplicate route use detected between ({module} and {method})")
                    url_method_map[route] = method

        return url_method_map

    def _filter_and_get_registered_modules(self) -> {ApiModule}:
        """
        Goes through the registered classes and finds those that have the request mapping meta and adds them to a set

        :return: a set of ApiModules
        """

        modules = set()
        for data in self._api_registry.contains_request_mapping_meta:
            if not has_meta_attribute(data):
                continue

            if inspect.isclass(data):
                modules.add(ApiClassModule(data))
            else:
                modules.add(ApiMethodModule(data))

        return modules
