import importlib
import os
import inspect

from web_framework import HttpResponse, HttpStatus
from web_framework.api.module import ApiModuleCoordinator
from web_framework.utils import scan_tree, get_meta_attribute, has_meta_attribute


class ApiRegistry:
    """
    Encapsulates all the data and logic done by the API

    Attributes
    ----------
    registered_classes : {class}
        a set of all the classes that have any association with the API
    api_module_paths : (str)
        all the paths to recursively search for modules in
    adapter_container : AdapterContainer
        The adapter container which is responsible for adapting data types to base, html readable data
    api_module_coordinator : ApiModuleCoordinator
        Responsible for coordinating all the information flow between the api modules and the client, the programmer.

    Methods
    -------
    register_api_packages(*module_paths: str)
        registers recursively all the api packages the client has asked to register. Finds all callables which have association to API
    """

    def __init__(self, *api_module_paths: str):
        """
        Initializes the ApiRegistry by recursively going through the directories in api_module_paths
        and finding API modules. Initializes the adapter container and the module coordinator.

        :param api_module_paths: all the paths to recursively search for modules in
        """

        from web_framework.api.type_parsing import AdapterContainer
        self.contains_request_mapping_meta = set()
        self.api_module_paths = api_module_paths
        self.register_api_packages(*api_module_paths)
        self.adapter_container = AdapterContainer(self)  # dependent on register_api_packages being called beforehand
        self.api_module_coordinator = ApiModuleCoordinator(self)  # dependent on register_api_packages being called beforehand

    def execute_method(self, method, request, client) -> HttpResponse:
        """
        Executes an API method and builds an HttpResponse

        :param method: the method to execute
        :param request: the HttpRequest made that resulted in the method being called
        :param client: the received client socket
        :return:
        """

        method_meta = get_meta_attribute(method)
        clazz = getattr(method_meta, 'parent')

        if not clazz.request_method_acceptable(method, request):
            response = HttpResponse.build_empty_status_response(
                request, HttpStatus.BAD_REQUEST, f'Class {clazz} and method {method} do not accept {request.method}', client)
        else:
            response = HttpResponse.build_from_function(request, method, self.adapter_container, client)

        return response

    def register_api_packages(self, *module_paths: str):
        """
        registers recursively all the api packages the client has asked to register. Finds all callables which have association to API
        :param module_paths:  the package paths
        """

        for module_path in module_paths:
            self._register_api_package(module_path)

    def _register_api_package(self, package_path):
        """
        registers a single api package the client has asked to register. Finds all callables which have association to API

        Finds all __init__ files in the package path, imports them and looks at all their callables

        :param package_path: the package path
        """

        api = importlib.import_module(package_path)
        dir_path = api.__path__[0]
        paths = [(i.name, i.path) for i in scan_tree(dir_path)]
        for (name, path) in paths:  # recursively go over all __init__ files in package_path directory
            if '__init__.py' in name:
                rel_path = os.path.splitext(os.path.relpath(path).replace('\\', '.'))[0]
                module = importlib.import_module(rel_path)
                self.parse_module(module)

    def parse_module(self, module, max_rec=0):
        if max_rec > 10:
            return
        max_rec += 1
        for i in dir(module):
            data = getattr(module, i)
            if type(data) is type(module):
                self.parse_module(data, max_rec)
            if has_meta_attribute(data):
                self.contains_request_mapping_meta.add(data)
