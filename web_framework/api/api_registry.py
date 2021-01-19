import importlib
import os
import inspect

from web_framework.api.module import ApiModuleCoordinator
from web_framework.utils import scan_tree


class ApiRegistry:
    def __init__(self, *api_module_paths: str):
        from web_framework.api.type_parsing import AdapterContainer
        self.registered_classes = set()
        self.api_module_paths = api_module_paths
        self.register_api_packages(api_module_paths)
        self.adapter_container = AdapterContainer(self)
        self.api_module_coordinator = ApiModuleCoordinator(self)

    def register_api_packages(self, module_paths):
        for module_path in module_paths:
            self.register_api_package(module_path)

    def register_api_package(self, package_path):
        api = importlib.import_module(package_path)
        dir_path = api.__path__[0]
        paths = [(i.name, i.path) for i in scan_tree(dir_path)]
        for (name, path) in paths:  # recursively go over all __init__ files in package_path directory
            if '__init__.py' in name:
                rel_path = os.path.splitext(os.path.relpath(path).replace('\\', '.'))[0]
                module = importlib.import_module(rel_path)
                for i in dir(module):
                    clazz = getattr(module, i)
                    if inspect.isclass(clazz):
                        self.registered_classes.add(clazz)
