from web_framework.api.type_parsing import TypeAdapter
from web_framework.api.module import MethodContentType
from web_framework.api.api_registry import ApiRegistry
from web_framework.utils import get_base_classes
from web_framework.api.type_parsing.default_adapters import *


class AdapterContainer:
    def __init__(self, api_registry: ApiRegistry):
        self.api_registry = api_registry
        self.registered_type_adapters = self.filter_and_get_type_adapters()
        for default_type_adapter in [StringTextAdapter(), BytesTextAdapter(), IntegerTextAdapter(), FloatTextAdapter(), BooleanTextAdapter(), ObjectTextAdapter(), JsonObjectTypeAdapter()]:
            self.registered_type_adapters.add(default_type_adapter)
        self.type_adapter_dictionary = {}
        for i in self.registered_type_adapters:
            if self.type_adapter_dictionary.get(i.content_type, None) is None:
                self.type_adapter_dictionary[i.content_type] = {i.adapting_type: i}
            else:
                if self.type_adapter_dictionary[i.content_type].get(i.adapting_type, None) is not None:
                    raise RuntimeError(f"Two type adapters with type of {i.adapting_type} and content type of {i.content_type} found.")
                self.type_adapter_dictionary[i.content_type][i.adapting_type] = i

    def find_type_adapter(self, adaptee_type: type, content_type: MethodContentType) -> TypeAdapter:
        adapter = self.type_adapter_dictionary.get(content_type, {}).get(adaptee_type, None)
        if adapter is None:
            adapter = self.type_adapter_dictionary.get(content_type, {}).get(object, None)
            if adapter is None:
                raise RuntimeError(f"No adapter found for {adaptee_type} with content type of {content_type}")
        return adapter

    def filter_and_get_type_adapters(self):
        from web_framework.api.type_parsing import TypeAdapter
        adapters = set()
        for clazz in self.api_registry.contains_request_mapping_meta:
            base_classes = get_base_classes(clazz)
            if TypeAdapter.__class__ in base_classes:
                adapters.add(clazz)

        return adapters
