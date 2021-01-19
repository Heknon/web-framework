import socket
import os
import threading

from web_framework.api import ApiRegistry
from web_framework.utils import get_meta_attribute, get_conditional_handler
from . import HttpClient, HttpStatus
from .http_base import HttpRequest, HttpResponse


class HttpServer:
    """
    The abstraction for creating an HttpServer.

    This class listens to incoming socket connections along with creating the api module registry for API functionality

    Attributes
    ----------
    module_paths : str
        the packages to go through and recursively look for API modules

    root_index_directory : str
        the root folder for HTML if any

    index_file : str
        the file associated when showing URI of '/'

    api_registry : ApiRegistry
        used to allow interaction between the API and the server

    Methods
    -------
    start()
        starts the server

    stop()
        stops the server forcefully

    execute_method(method: Callable, request: HttpRequest, client: HttpClient)
        executes an API method using all abstractions in order to include decorators and builds response
    """

    def __init__(self, root_index_directory: str, index_file: str, *module_paths: str):
        """
        Initializes the server's properties. Builds the APIRegistry and creates the socket.
        This will go through all __init__.py files in `module_paths` and find classes that are associated with the API
        :param root_index_directory: the root folder for HTML if any
        :param index_file: the file associated when showing URI of '/'
        :param module_paths: the packages to go through and recursively look for API modules
        """

        self._ip = ("0.0.0.0", 80)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._is_active = True
        self.root_index_directory = root_index_directory
        self.index_file = index_file
        self.module_paths = module_paths
        self.api_registry = ApiRegistry(*self.module_paths)
        self._client_listen_thread = threading.Thread(target=self.__client_listener)

    def stop(self):
        """
        Shuts down the server

        Sets the server active flag to false, sends an alert to the server console and shuts down the server socket.
        Due to shutting down the server socket and exception is thrown, once it is caught we know the socket has shutdown
        and we exit forcefully using os._exit in order to close all threads.
        """

        try:
            self._is_active = False
            print("Shutting server down...")
            self._socket.shutdown(socket.SHUT_WR)
        except:
            print("The server has shutdown...")
            os._exit(1)
            exit()

    def start(self):
        """
        Starts the server

        Binds the socket created to the server and starts the client listener thread
        in order to asynchronously listen for new clients.
        Prints a message to console notifying the server is up and running.
        """

        self._socket.bind(self._ip)
        self._socket.listen(2)
        self._client_listen_thread.start()
        print("The server is active and listening...")

    def __client_listener(self):
        """
        Listens to incoming clients and registers them onto the server.

        Loop that runs until the server is shutdown.
        Accepts client sockets and converts them to HttpClient objects and starts their thread
        in order to asynchronously deal with the data and send back a response
        """

        while self._is_active:
            client_socket, address = self._socket.accept()
            client = HttpClient(client_socket, address, lambda client_req, request: self.__client_request_handler(client_req, request))
            client.start()
        exit()

    def __client_request_handler(self, client: HttpClient, request: HttpRequest):
        """
        Callback function for HttpClient to call when the request has been parsed and is ready to create a response. Sends the response and closes the socket.

        Checks if the api registry has a method call for the given route
        and goes through all the ConditionalHandler methods to see if there are any matching ones
        if there are they are executed if there is method for the specific route.
        Once the appropriate method is found, executes it using execute method which returns a response which is then sent to the browser.
        If there is no method available api resorts to local resources if any

        :param client: The HttpClient which will receive the response
        :param request: the parsed HttpRequest
        """

        has_method_call = request.url in self.api_registry.api_module_coordinator.full_route_method_map
        for class_route, methods in self.api_registry.api_module_coordinator.conditional_routes.items():
            for method in methods:
                if not has_method_call and request.url.startswith(class_route) and get_conditional_handler(method)(request):
                    self.execute_method(method, request, client).send_to_client(client)
            break

        if has_method_call:
            method = self.api_registry.api_module_coordinator.find_matching_method(request.url)
            self.execute_method(method, request, client).send_to_client(client)
        else:
            path = self.root_index_directory + (self.index_file if request.url == "/" else request.url)
            response = HttpResponse.build_from_file(request, path, client)
            response.send_to_client(client)
        client.shutdown()
        exit()

    def execute_method(self, method, request, client) -> HttpResponse:
        """
        Executes an API method and builds an HttpResponse

        :param method: the method to execute
        :param request: the HttpRequest made that resulted in the method being called
        :param client: the received client socket
        :return:
        """

        method_meta = get_meta_attribute(method)
        clazz = getattr(method_meta, 'parent').clazz
        parent_meta = get_meta_attribute(clazz)
        method_http_methods_contains_method = method_meta.acceptable_methods is not None and request.method in method_meta.acceptable_methods
        class_http_methods_contains_method = parent_meta.acceptable_methods is not None and request.method in parent_meta.acceptable_methods

        if not class_http_methods_contains_method and not method_http_methods_contains_method:
            response = HttpResponse.build_empty_status_response(
                request, HttpStatus.BAD_REQUEST, f'Class {clazz} and method {method} do not accept {request.method}', client)
        else:
            response = HttpResponse.build_from_function(request, method, self.api_registry.adapter_container, client)

        return response
