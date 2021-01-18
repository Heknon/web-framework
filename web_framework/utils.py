from os import scandir

from typing import ClassVar

from web_framework.api.module.decorator import RequestMappingMeta

META_ATTRIBUTE_KEY = "-__routing_api_meta__-"
CONDITIONAL_HANDLER_KEY = '-__CONDITIONAL_HANDLER__-'


def set_attribute(t, key: str, data):
    if not callable(t):
        raise RuntimeError("Trying to annotate " + t)
    setattr(t, key, data)
    return t


def get_attribute(t, key: str) -> RequestMappingMeta:
    return getattr(t, key)


def has_attribute(t, key: str) -> bool:
    return hasattr(t, key)


def set_meta_attribute(t, meta):
    return set_attribute(t, META_ATTRIBUTE_KEY, meta)


def add_to_meta_attribute(t, name, data):
    if has_meta_attribute(t):
        raise RuntimeError("Must have a RequestMapping in order to add other decorators. RequestMapping must be at the top of all other decorators")
    set_attribute(get_meta_attribute(t), name, data)


def get_attribute_from_meta(t, name):
    if has_meta_attribute(t):
        raise RuntimeError("Must have a RequestMapping in order to get other attributes. RequestMapping must be at the top of all other decorators")
    return getattr(get_meta_attribute(t), name)


def get_meta_attribute(t) -> RequestMappingMeta:
    return getattr(t, META_ATTRIBUTE_KEY)


def has_meta_attribute(t) -> bool:
    return has_attribute(t, META_ATTRIBUTE_KEY)


def get_conditional_handler(t):
    return get_attribute(t, CONDITIONAL_HANDLER_KEY)


def set_conditional_handler(t, value):
    return set_attribute(t, CONDITIONAL_HANDLER_KEY, value)


def has_conditional_handler(t):
    return has_attribute(t, CONDITIONAL_HANDLER_KEY)


def get_base_classes(clazz: ClassVar) -> {ClassVar}:
    bases = set()
    if type(clazz) is not type:
        clazz = clazz.__class__
    for b in clazz.__bases__:
        bases.add(b)
    for i in clazz.__bases__:
        for curr in get_base_classes(i):
            bases.add(curr)
    return bases


def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            yield entry
