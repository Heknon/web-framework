class QueryParameters:
    def __init__(self):
        pass

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return f"QueryParameters({self.__dict__})"
