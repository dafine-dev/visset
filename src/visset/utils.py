from __future__ import annotations
from typing import Any, TypeVar
from functools import wraps

Class = TypeVar('Class')


def singleton(_class: Class) -> Class:

    @wraps(_class, updated=())
    class Singleton(_class):
        _instance: Class = None

        def __new__(cls, *args, **kwargs) -> Class:
            if cls._instance is None:
                cls._instance = object.__new__(cls)
                _class.__init__(cls._instance, *args, **kwargs)

            return cls._instance

        def __init__(self, *args, **kwargs) -> None:
            ...

    return Singleton


def self_factory(_class: Class) -> Class:

    key_name = _class.__init__.__code__.co_varnames[1]

    def get_key_value(args, kwargs) -> Any:
        try:
            return kwargs[key_name]
        except KeyError:
            return args[0]

    @wraps(_class, updated=())
    class Factory(_class):
        _instances: dict[Any, Class] = {}

        def __new__(cls, *args, **kwargs) -> Class:
            key = get_key_value(args, kwargs)

            if key not in cls._instances:
                cls._instances[key] = object.__new__(cls)
                _class.__init__(cls._instances[key], key)

            return cls._instances[key]

        def __init__(self, *args, **kwargs) -> None:
            ...

    return Factory


def abstract(_class: Class) -> Class:
    return _class


def interface(_class: Class) -> Class:
    return _class
