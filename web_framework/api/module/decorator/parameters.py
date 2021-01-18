from collections import Iterable

from . import Parameter


class QueryParameter(Parameter):
    def __init__(self, parameter_type: type, name: str = None, content_type=None, default_value: object = None, required: bool = False):
        super().__init__(parameter_type, name, content_type, default_value, required)

    def get_value_from_request(self, request) -> [bytes]:
        val = request.query_parameters.__dict__.get(self.name, None)
        if val is not None and not isinstance(val, Iterable):
            val = [val]
        return list(map(lambda x: str(x).encode(), val)) if val is not None else None
