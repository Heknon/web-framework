import socket
import threading
import time

from .http_base import HttpRequest
from web_framework.parser.request_parser import RequestParser
from typing import Callable


class HttpClient:
    """
    Abstracts away the logic that is done with the client

    Handles the incoming data from the client along with parsing the data that came
    and forming an HttpRequest

    Attributes
    ----------
    address: (int, int)
        The ip address of the client (ip, port)

    receive_time: int
        This is set as current time in seconds Epoch when socket receives data in handle_request

    Methods
    -------
    start()
        Starts the incoming request listener thread. Infinitely listens for new requests made by the client.
    send()
        Send data to socket of client
    """

    def __init__(self, client: socket.socket, address: (int, int), request_made_callback: Callable[[any, HttpRequest], None]):
        """
        Initialized the HttpClient's properties

        :param client: the client's socket
        :param address: the client's ip address details
        :param request_made_callback: the callback made when a request has been parsed and is ready to be used by the API
        """

        self._socket: socket.socket = client
        self.address: (int, int) = address
        self._thread = threading.Thread(target=self._handle_request)
        self._request_made_callback = request_made_callback
        self.receive_time = 0

    def start(self):
        """Starts the incoming request listener thread. Infinitely listens for new requests made by the client."""

        self._thread.start()

    def send(self, data: bytes):
        """Sends data to the client's socket"""

        self._socket.send(data)

    def _handle_request(self):
        """
        Once the client's start method is called, a thread enters an infinite loop
        of accepting new data from the socket (client). This data is parsed into HttpRequest
        and we then call the callback to notify the server of the completion
        """

        while True:
            data: bytes = self._socket.recv(6000)
            self.receive_time = time.time()
            if len(data) == 0:
                self.shutdown()
                break
            split = data.split(b"\r\n\r\n")
            split[0] += b"\r\n\r\n"
            request = self.__parse_http_request(split[0].decode(), split[1] if len(split) > 1 else bytes())
            self._request_made_callback(self, request)

    def shutdown(self):
        """Shuts the socket down"""

        self._socket.shutdown(socket.SHUT_WR)

    def __parse_http_request(self, request: str, extra: bytes) -> HttpRequest:
        """
        Parses the request text and turns it into a HttpRequest object
        :param request: the request string
        :param extra: extra bytes that might come from a POST method (the request body)
        :return: the parsed HttpRequest
        """

        request_parser = RequestParser(request, extra)
        request = request_parser.get_http_request()
        if 'Content-Length' in request.mapped_headers:
            extra = int(request.mapped_headers["Content-Length"]) - len(request_parser.extra)
            extra_bytes = self._socket.recv(extra)
            request_body = request_parser.extra + extra_bytes
            request.body = request_body
        return request
