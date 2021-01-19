from enum import Enum

from web_framework.http_base.data_type import ContentType


class MethodReturnContentType(Enum):
    JSON = ContentType('json')
    TEXT = ContentType('text')
    HTML = ContentType('html')
    XML = ContentType('xml')
