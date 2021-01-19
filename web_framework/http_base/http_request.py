from web_framework.http_base.data_type import HttpHeader, HttpMethod, QueryParameters


class HttpRequest:
    """
    Class representing an HttpRequest in non-string form

    Attributes
    ----------
    method : HttpMethod
        the http method used to for the request
    url : str
        the sub-url of the website (URI)
    http_version : str
        the http version the client used
    headers : [HttpHeader]
        the headers passed using the request
    mapped_headers : {str: str}
        a dictionary containing all headers mapped to key value pairs. Used to find a header in constant time
    query_parameters : QueryParameters
        The query parameters rescued from the uri
    body : bytes
        the body of the request

    Methods
    -------
    find_header(name: str)
        Finds a header based on its key and returns it
    """

    def __init__(self):
        self.method: HttpMethod = None
        self.url: str = ""
        self.http_version: str = ""
        self.headers: [HttpHeader] = []
        self.mapped_headers = {}
        self.query_parameters: QueryParameters = QueryParameters()
        self.body = bytes()

    def find_header(self, name: str) -> HttpHeader:
        """
        Finds a header based on its key and returns it
        :param name: the key of the header, its name
        :return: the http header matching the key otherwise None
        """

        return self.mapped_headers.get(name, None)

    def __str__(self):
        return f"HttpRequest(method: {self.method}, url: {self.url}, http_version: {self.http_version}, headers: {[str(i) for i in self.headers]})"
