import os
import socket
import time
from typing import Callable

from web_framework.http_base.data_type import HttpStatus
from web_framework.http_base import HttpRequest, ContentType


class HttpResponse:
    def __init__(self, content_type: str, http_version: str, status: HttpStatus, html: bytes, client):
        self.data = f"{http_version} {status.value} {status.name}\r\n".encode()
        self.data += f"{content_type}\r\n".encode()
        self.add_header("Content-Length", len(html))
        self.add_header("Server-Timing", str(time.time() - client.receive_time))
        self.data += '\r\n'.encode()
        self.data += html

    def add_header(self, header, value):
        self.data += f"{header}: {value}\r\n".encode()

    def send_to_client(self, client: socket.socket):
        client.send(self.data)

    @staticmethod
    def build_from_function(request: HttpRequest, fn: Callable, adapter_container, client):
        from web_framework.api.module import ApiMethodExecutor
        executor = ApiMethodExecutor(fn, adapter_container, client)
        return HttpResponse(executor.content_type, request.http_version, HttpStatus.OK, executor.execute(request), client)

    @staticmethod
    def build_empty_status_response(request: HttpRequest, status: HttpStatus, additional_info: str, client):
        return HttpResponse(str(ContentType('html')), request.http_version, status, additional_info.encode(), client)

    @staticmethod
    def build_from_file(request: HttpRequest, path: str, client):
        extension = os.path.splitext(path)[1][1::]
        content_type = ContentType(extension)
        if not os.path.isfile(path):
            print("fdsfs")
            return HttpResponse(str(content_type), request.http_version, HttpStatus.NOT_FOUND, bytes(), client)
        else:
            html: bytes
            with open(path, 'rb') as file:
                html = file.read() + b"\r\n\r\n"
            return HttpResponse(str(content_type), request.http_version, HttpStatus.OK, html, client)

