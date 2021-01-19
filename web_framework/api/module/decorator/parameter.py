from collections import Iterable


class Parameter:
    def __init__(self, parameter_type: type, name: str = None, content_type=None, default_value: object = None, required: bool = False):
        from web_framework import MethodReturnContentType
        if content_type is None:
            content_type = MethodReturnContentType.TEXT
        self.parameter_type = parameter_type
        self.content_type = content_type
        self.name = name
        self.default_value = default_value
        self.required = required

    def parse(self, method: object, request, adapter_container) -> (str, object):
        """
        parses a method
        :return: the new value of a parameter with its name (name, value)
        """
        annotations = method.__annotations__
        if len(annotations) == 0:
            return None
        for name, value in annotations.items():
            if value is self:
                result: [bytes] = self.get_value_from_request(request)
                if not isinstance(result, Iterable):
                    result = [result]
                if result is None:
                    if self.default_value is None and self.required:
                        raise RuntimeError(f"Parameter {self} has result of None. Parameter is required and cannot be None!")
                    return name, self.default_value

                results = []
                for i in result:
                    if i is None:
                        continue
                    results.append(adapter_container.find_type_adapter(self.parameter_type, self.content_type).decode(i))
                if len(results) == 1:
                    results = results[0]
                return name, results

    def get_value_from_request(self, request) -> [bytes]:
        raise NotImplementedError(f"Must implement get_value_from_request in {self}")
