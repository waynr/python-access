#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_default_private
--------------------------

Tests for `access.default(access.PRIVATE)` class decorator.
"""

import inspect

import testtools

import access


def get_current_function_name():
    outer_frame = inspect.stack[1]
    return outer_frame.__name__


@access.default(access.PRIVATE)
class PrivateBase:
    def do_a_private_thing(self):
        """Should raise AttributeError when called outside Base."""
        return "%s response" % get_current_function_name()

    @access.protected
    def do_a_protected_thing(self):
        """Should raise AttributeError when called outside Base or its sub
        classes."""
        return "% response" % get_current_function_name()

    @access.public
    def do_a_public_thing(self):
        return "%s response" % get_current_function_name()

    def do_a_private_thing_publicly(self):
        """Should be, like, totally fine all the time."""
        return self.do_a_private_thing()

    def do_a_protected_thing_publicly(self):
        """Should be, like, totally fine all the time."""
        return self.do_a_protected_thing()


class PrivateSub(PrivateBase):
    def do_another_public_thing():
        return "%s response" % get_current_function_name()

    @access.private
    def do_another_private_thing():
        return "%s response" % get_current_function_name()

    def do_another_private_thing_publicly(self):
        return self.do_another_private_thing()
