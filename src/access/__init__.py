# -*- coding: utf-8 -*-

import functools

__author__ = """Wayne Warren"""
__email__ = 'waynr+python-access@sdf.org'
__version__ = '0.0.0'


PRIVATE = "private"
PROTECTED = "protected"


def private(function):

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


def protected(function):

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


def public(function):

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


def default(access_level):

    def decorator(Cls):
        return Cls
    return decorator


class PrivateAttributeError(AttributeError):
    pass


class ProtectedAttributeError(AttributeError):
    pass
