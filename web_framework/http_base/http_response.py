import os
import time
from typing import Callable

from web_framework.http_base.data_type import HttpStatus
from web_framework.http_base import HttpRequest, ContentType


class HttpResponse:
    """
    The job of this class is to build the final HttpResponse in string form after being given all the data required

    Attributes
    ----------
    content_type : str
        the content type of the response
    http_version : str
        the http version of the server used
    status : HttpStatus
        the http status of the response
    html : bytes
        the response body, the data sent for the browser to use
    client : HttpClient
        the http client, used to get data from the client and send data to the socket

    Methods
    -------
    add_header(header, value)
        Adds a header to data using header name and value and encodes it into the header format

    send_to_client()
        requests to build new data and sends it to the client socket

    Static Methods
    --------------
    build_from_function(request: HttpRequest, fn: Callable, adapter_container: AdapterContainer, client: HttpClient)
        builds an HttpResponse object mainly from a method. This method should be an Api Method

    build_empty_status_response(request: HttpRequest, status: HttpStatus, additional_info: str, client: HttpClient)
        Builds an empty HttpResponse using only HttpStatus and some additional info that may be passed

    build_from_file(request: HttpRequest, path: str, client: HttpClient)
        Builds an HttpResponse from a file such as a JavaScript file or HTML
    """

    def __init__(self, content_type: str, http_version: str, status: HttpStatus, html: bytes, client):
        self.content_type = content_type
        self.http_version = http_version
        self.status = status
        self.html = html
        self.client = client
        self.__data = bytes()

    def __build_response(self):
        """
        Builds the response in text form.

        This is not done in the main constructor to allow api users to manually change data about the response
        """

        self.__data = f"{self.http_version} {self.status.value} {self.status.name}\r\n".encode()
        self.__data += f"{self.content_type}\r\n".encode()
        self.add_header("Content-Length", len(self.html))
        self.add_header("Server-Timing", str(time.time() - self.client.receive_time))
        self.__data += '\r\n'.encode()
        self.__data += self.html

    def add_header(self, header, value):
        """
        Adds a header to data using header name and value and encodes it into the header format

        :param header: the name of the header
        :param value: the value of the header
        """

        self.__data += f"{header}: {value}\r\n".encode()

    def send_to_client(self, client):
        """
        Builds the text response and sends it to the client socket

        :param client: the HttpClient to send the data to
        """

        self.__build_response()
        client.send(self.__data)

    @staticmethod
    def build_from_function(request: HttpRequest, fn: Callable, api_registry, client):
        """
        builds an HttpResponse object mainly from a method. This method should be an Api Method

        :param request: the http request that a response is being built for
        :param fn: the method to use to build data with
        :param api_registry: the api registry
        :param client: the http client to send the response to
        :return: the built HttpResponse
        """

        from web_framework.api.module import ApiMethodExecutor
        response_orig = HttpResponse.build_empty_status_response(request, HttpStatus.OK, None, client)
        executor = ApiMethodExecutor(fn, api_registry, response_orig, client)
        res = executor.execute(request)
        return HttpResponse(str(executor.content_type.value), response_orig.http_version, response_orig.status, res, client)

    @staticmethod
    def build_empty_status_response(request: HttpRequest, status: HttpStatus, additional_info: str, client):
        """
        Builds an empty HttpResponse using only HttpStatus and some additional info that may be passed

        :param request: the http request that a response is being built for
        :param status: the http status of the response
        :param additional_info: additional information to send as response body
        :param client: the http client to send the response to
        :return: the built HttpResponse
        """
        if additional_info is None:
            additional_info = ""
        return HttpResponse(str(ContentType('html')), request.http_version, status, additional_info.encode(), client)

    @staticmethod
    def build_from_file(request: HttpRequest, path: str, client):
        """
        Builds an HttpResponse from a file such as a JavaScript file or HTML

        :param request: the http request that a response is being built for
        :param path: the path to the file
        :param client: the http client to send the response to
        :return: the built HttpResponse
        """

        if not os.path.isfile(path):
            return HttpResponse(str(ContentType('text')), request.http_version, HttpStatus.NOT_FOUND, bytes(), client)
        else:
            extension = os.path.splitext(path)[1][1::]
            content_type = ContentType(extension)
            html: bytes
            with open(path, 'rb') as file:
                html = file.read() + b"\r\n\r\n"
            return HttpResponse(str(content_type), request.http_version, HttpStatus.OK, html, client)
