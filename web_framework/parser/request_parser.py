from ..http_base.data_type import HttpHeader, HttpMethod, QueryParameters
from ..http_base import HttpRequest
from . import Parser


class RequestParser(Parser):
    def __init__(self, request: str, extra: bytes):
        super().__init__(request)
        self.extra = extra

    def get_http_request(self) -> HttpRequest:
        request = HttpRequest()
        method = self._get_text_till_character(" ")
        url = self._get_text_till_character("[? ]")
        query = self.__parse_query() if self.text[self.cursor - 1] == "?" else None
        version = self._get_text_till_character("\r")
        self._pop()

        headers: [HttpHeader] = []
        while self._peek() != "\n":
            headers.append(self.__parse_header())

        request.method = HttpMethod(method)
        request.url = url
        request.http_version = version
        request.headers = headers
        request.query_parameters = query
        request.mapped_headers = {header.name: header.value for header in headers}
        return request

    def __parse_query(self) -> QueryParameters:
        query_params = QueryParameters()
        while self.text[self.cursor - 1] != " ":
            query = self._get_text_till_character("=")
            value = self._get_text_till_character("[& ]").replace("%20", "")
            values = value.split(",")
            query_params.__dict__[query] = values

        return query_params

    def __parse_header(self) -> HttpHeader:
        header_field = self._get_text_till_character(":")
        self._pop()
        header_value = self._get_text_till_character("\r")
        self.cursor += 1
        return HttpHeader(header_field, header_value)
