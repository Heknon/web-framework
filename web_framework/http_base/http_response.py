import os
import time
from typing import Callable

from web_framework.http_base.data_type import HttpStatus
from web_framework.http_base import HttpRequest, ContentType


class HttpResponse:
    def __init__(self, content_type: str, http_version: str, status: HttpStatus, html: bytes, client):
        self.content_type = content_type
        self.http_version = http_version
        self.status = status
        self.html = html
        self.client = client
        self.data = bytes()

    def __build_response(self):
        self.data = f"{self.http_version} {self.status.value} {self.status.name}\r\n".encode()
        self.data += f"{self.content_type}\r\n".encode()
        self.add_header("Content-Length", len(self.html))
        self.add_header("Server-Timing", str(time.time() - self.client.receive_time))
        self.data += '\r\n'.encode()
        self.data += self.html

    def add_header(self, header, value):
        self.data += f"{header}: {value}\r\n".encode()

    def send_to_client(self, client):
        self.__build_response()
        client.send(self.data)

    @staticmethod
    def build_from_function(request: HttpRequest, fn: Callable, adapter_container, client):
        from web_framework.api.module import ApiMethodExecutor
        response_orig = HttpResponse.build_empty_status_response(request, HttpStatus.OK, None, client)
        executor = ApiMethodExecutor(fn, adapter_container, response_orig, client)
        res = executor.execute(request)
        return HttpResponse(executor.content_type, response_orig.http_version, response_orig.status, res, client)

    @staticmethod
    def build_empty_status_response(request: HttpRequest, status: HttpStatus, additional_info: str, client):
        if additional_info is None:
            additional_info = ""
        return HttpResponse(str(ContentType('html')), request.http_version, status, additional_info.encode(), client)

    @staticmethod
    def build_from_file(request: HttpRequest, path: str, client):
        if not os.path.isfile(path):
            return HttpResponse(str(ContentType('text')), request.http_version, HttpStatus.NOT_FOUND, bytes(), client)
        else:
            extension = os.path.splitext(path)[1][1::]
            content_type = ContentType(extension)
            html: bytes
            with open(path, 'rb') as file:
                html = file.read() + b"\r\n\r\n"
            return HttpResponse(str(content_type), request.http_version, HttpStatus.OK, html, client)
