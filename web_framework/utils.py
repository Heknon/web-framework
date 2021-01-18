from os import scandir

from typing import ClassVar

from web_framework.api.module.decorator import RequestMappingMeta

META_ATTRIBUTE_KEY = "__routing_api_meta__"


def set_meta_attribute(t, meta):
    if not callable(t):
        raise RuntimeError("Trying to annotate " + t)
    setattr(t, META_ATTRIBUTE_KEY, meta)
    return t


def get_meta_attribute(t) -> RequestMappingMeta:
    return getattr(t, META_ATTRIBUTE_KEY)


def has_meta_attribute(t) -> bool:
    return hasattr(t, META_ATTRIBUTE_KEY)


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
