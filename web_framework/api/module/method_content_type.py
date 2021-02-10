from enum import Enum

from web_framework.http_base.data_type import ContentType


class MethodContentType(Enum):
    """
    Select Content Types allowed for a method to convert to
    """

    JSON = ContentType('json')
    TEXT = ContentType('text')
    HTML = ContentType('html')
    XML = ContentType('xml')
