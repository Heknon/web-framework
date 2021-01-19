from web_framework.http_base.data_type import HttpHeader, HttpMethod, QueryParameters


class HttpRequest:
    def __init__(self):
        self.method: HttpMethod = None
        self.url: str = ""
        self.http_version: str = ""
        self.headers: [HttpHeader] = []
        self.mapped_headers = {}
        self.query_parameters: QueryParameters = QueryParameters()
        self.body = bytes()

    def find_header(self, name) -> HttpHeader:
        if name not in self.mapped_headers:
            return None
        return self.mapped_headers[name]

    def __str__(self):
        return f"HttpRequest(method: {self.method}, url: {self.url}, http_version: {self.http_version}, headers: {[str(i) for i in self.headers]})"
