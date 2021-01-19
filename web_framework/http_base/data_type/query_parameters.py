class QueryParameters:
    """
    Represents the query parameters of a URL and allows for easy, intuitive access

    Methods
    -------
    get(name, default=None)
        gets a query parameter by its name
    """

    def get(self, name, default=None):
        if name not in self.__dict__:
            return default
        return self.__dict__[name]

    def __getitem__(self, name):
        return self.__dict__[name]

    def __str__(self):
        return f"QueryParameters({self.__dict__})"
