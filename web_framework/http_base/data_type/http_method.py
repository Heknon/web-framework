from enum import Enum


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
