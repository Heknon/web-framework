class QueryParameters:
    def __init__(self):
        pass

    def get(self, item, default):
        if item not in self.__dict__:
            return default
        return self.__dict__[item]


    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return f"QueryParameters({self.__dict__})"
