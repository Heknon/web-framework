"""
Main init package for importing all logic from web framework

Packages
--------
api
    Contains all the logic that allows the API to function. Decorators, annotations, builders...
parser
    Contains the text parsers
http_base
    Contains the base HTTP elements such as request and response along with HTTP data types such as HttpStatus
"""

__all__ = ['utils', 'HttpClient', 'HttpServer', 'ApiRegistry', 'MethodContentType', 'ApiClassModule', 'ApiModuleCoordinator',
           'MethodContentType', 'ApiMethodExecutor', 'TypeAdapter', 'AdapterContainer', 'TextTypeAdapter',
           'JsonTypeAdapter', 'HtmlTypeAdapter', 'HttpRequest', 'HttpResponse', 'HttpMethod', 'HttpHeader', 'HttpStatus', 'ContentType',
           'QueryParameters', 'Parser', 'RequestParser', 'RequestMappingMeta', 'RequestMapping', 'GetMapping', 'PutMapping',
           'PatchMapping', 'PostMapping', 'DeleteMapping', 'ConnectMapping', 'TraceMapping', 'HeadMapping', 'OptionsMapping', 'QueryParameter',
           'Parameter', 'ConditionalHandler', 'ApiModule', 'ApiMethodModule', "RequestBody", 'PathVariable']

import web_framework.utils as utils
from .http_base import *
from .parser import *
from .api import *
from .http_client import HttpClient
from .http_server import HttpServer
