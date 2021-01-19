from enum import Enum


class HttpMethod(Enum):
    """
    Enum that represents all HttpMethod's available
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
