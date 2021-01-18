import socket
import os
import threading

from web_framework.api import ApiRegistry
from web_framework.utils import get_meta_attribute, get_conditional_handler
from . import HttpClient, HttpStatus
from .http_base import HttpRequest, HttpResponse


class HttpServer:
    def __init__(self, root_index_directory: str, index_file: str, *module_paths: str):
        self.ip = ("0.0.0.0", 8080)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_active = True
        self.root_index_directory = root_index_directory
        self.index_file = index_file
        self.module_paths = module_paths
        self.api_registry = ApiRegistry(*self.module_paths)
        self.client_listen_thread = threading.Thread(target=self.client_listener)
        self.active_clients: [HttpClient] = []

    def stop(self):
        try:
            self.is_active = False
            print("Shutting server down...")
            self.socket.shutdown(socket.SHUT_WR)
        except:
            print("The server has shutdown...")
            os._exit(1)
            exit()

    def start(self):
        self.socket.bind(self.ip)
        self.socket.listen(1)
        self.client_listen_thread.start()
        print("The server is active and listening...")

    def client_listener(self):
        while self.is_active:
            client_socket, address = self.socket.accept()
            client = HttpClient(client_socket, address, lambda client_req, request: self.client_request_handler(client_req, request))
            self.active_clients.append(client)
            client.start()
        exit()

    def client_request_handler(self, client: HttpClient, request: HttpRequest):
        has_method_call = request.url in self.api_registry.api_module_coordinator.full_route_method_map
        for class_route, methods in self.api_registry.api_module_coordinator.conditional_routes.items():
            for method in methods:
                if not has_method_call and request.url.startswith(class_route) and get_conditional_handler(method)(request):
                    self.execute_method(method, request, client)
            break

        if has_method_call:
            method = self.api_registry.api_module_coordinator.find_matching_method(request.url)
            self.execute_method(method, request, client)
        else:
            path = self.root_index_directory + (self.index_file if request.url == "/" else request.url)
            """
            go through request controllers and find controllers controlling specified url
            go through methods and find correct method for route and correct method
            call method to get html response
            """
            response = HttpResponse.build_from_file(request, path, client)
            response.send_to_client(client.socket)
        client.shutdown()
        exit()

    def execute_method(self, method, request, client):
        method_meta = get_meta_attribute(method)
        clazz = getattr(method_meta, 'parent').clazz
        parent_meta = get_meta_attribute(clazz)
        method_http_methods_contains_method = method_meta.acceptable_methods is not None and request.method in method_meta.acceptable_methods
        class_http_methods_contains_method = parent_meta.acceptable_methods is not None and request.method in parent_meta.acceptable_methods

        if not class_http_methods_contains_method and not method_http_methods_contains_method:
            response = HttpResponse.build_empty_status_response(request, HttpStatus.BAD_REQUEST, f'Class {clazz} and method {method} do not accept {request.method}', client)
        else:
            response = HttpResponse.build_from_function(request, method, self.api_registry.adapter_container, client)

        response.send_to_client(client.socket)
