import socket
import threading
import time

from .http_base import HttpRequest
from web_framework.parser.request_parser import RequestParser
from typing import Callable


class HttpClient:
    def __init__(self, client: socket.socket, address: (int, int), request_made_callback: Callable[[any, HttpRequest], None]):
        self.socket: socket.socket = client
        self.address: (int, int) = address
        self.thread = threading.Thread(target=self.handle_request)
        self.request_made_callback = request_made_callback
        self.receive_time = 0

    def start(self):
        self.thread.start()

    def handle_request(self):
        while True:
            data: bytes = self.socket.recv(6000)
            self.receive_time = time.time()
            if len(data) == 0:
                self.shutdown()
                break
            split = data.split(b"\r\n\r\n")
            split[0] += b"\r\n\r\n"
            request = self.__parse_http_request(split[0].decode(), split[1] if len(split) > 1 else bytes())
            self.request_made_callback(self, request)

    def shutdown(self):
        self.socket.shutdown(socket.SHUT_WR)

    def __parse_http_request(self, response: str, extra: bytes) -> HttpRequest:
        request_parser = RequestParser(response, extra)
        request = request_parser.get_http_request()
        if 'Content-Length' in request.mapped_headers:
            extra = int(request.mapped_headers["Content-Length"]) - len(request_parser.extra)
            extra_bytes = self.socket.recv(extra)
            request_body = request_parser.extra + extra_bytes
            request.body = request_body
        return request
