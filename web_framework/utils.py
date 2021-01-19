from os import scandir

from typing import ClassVar

from web_framework.api.module.decorator import RequestMappingMeta

META_ATTRIBUTE_KEY = "-__routing_api_meta__-"
CONDITIONAL_HANDLER_KEY = '-__CONDITIONAL_HANDLER__-'


def set_attribute(t, key: str, data):
    """
    Set an attribute on a callable.

    Mainly used with decorators to allow the decorators to store data onto the callable

    :param t: the callable to store data onto
    :param key: the key of the data, the attributes name.
    :param data: the data to set, the attributes value
    :return: the callable after the modification

    :exception RuntimeError - Raised if a non callable is given as `t`
    """

    if not callable(t):
        raise RuntimeError("Trying to annotate " + t)
    setattr(t, key, data)
    return t


def get_attribute(t, key: str):
    """
    Get an attribute from a given callable

    :param t: the callable
    :param key: the key, the attributes name
    :return: the attribute data
    """

    return getattr(t, key)


def has_attribute(t, key: str) -> bool:
    """
    Check if a callable has an attribute

    :param t: the callable
    :param key: the key, the attributes name
    :return: True if callable contains attribute, otherwise False
    """

    return hasattr(t, key)


def set_meta_attribute(t, meta):
    """Uses set_attribute along with the meta key constant to easily allow setting meta"""

    return set_attribute(t, META_ATTRIBUTE_KEY, meta)


def get_meta_attribute(t) -> RequestMappingMeta:
    """Uses get_attribute along with the meta key constant to easily allow getting meta"""

    return get_attribute(t, META_ATTRIBUTE_KEY)


def has_meta_attribute(t) -> bool:
    """Uses has_attribute along with the meta key constant to easily check if callable has meta"""

    return has_attribute(t, META_ATTRIBUTE_KEY)


def get_conditional_handler(t):
    """Uses get_attribute along with the conditional handler key constant to easily get conditional handler object"""

    return get_attribute(t, CONDITIONAL_HANDLER_KEY)


def set_conditional_handler(t, value):
    """Uses set_attribute along with the conditional handler key constant to easily set conditional handler object"""

    return set_attribute(t, CONDITIONAL_HANDLER_KEY, value)


def has_conditional_handler(t):
    """Uses has_attribute along with the conditional handler key constant to easily check if callable has conditional handler object"""

    return has_attribute(t, CONDITIONAL_HANDLER_KEY)


def get_base_classes(clazz: ClassVar) -> {ClassVar}:
    """
    recursively get the all the base classes of a given class until base class object is reached

    :param clazz: the class to get the base classes of
    :return: a set of all base classes
    """

    bases = set()
    if type(clazz) is not type:
        clazz = clazz.__class__
    for b in clazz.__bases__:
        bases.add(b)
    for i in clazz.__bases__:
        for curr in get_base_classes(i):
            bases.add(curr)
    return bases


def scan_tree(path):
    """Recursively yield DirEntry objects for given directory."""

    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scan_tree(entry.path)  # see below for Python 2.x
        else:
            yield entry
