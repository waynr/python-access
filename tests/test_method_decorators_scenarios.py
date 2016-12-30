#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_method_decorators
----------------------

Tests for `access.private`, `access.protected`, and `access.public` decorators.
All tests in this module assume that the default behavior of an undecorated
method is to permit methods to be accessible on the object from any context.

"""

import inspect

import access

from tests.base import TestValidAccess, TestInvalidAccess


def get_current_function_name():
    outer_frame = inspect.stack[1]
    return outer_frame.__name__


class Base:

    @access.private
    def do_a_private_thing(self):
        """Should raise AttributeError when called outside Base."""
        return "%s response" % get_current_function_name()

    @access.protected
    def do_a_protected_thing(self):
        """Should raise AttributeError when called outside Base or its sub
        classes."""
        return "%s response" % get_current_function_name()

    def do_a_public_thing(self):
        """Should be, like, totally fine all the time."""
        return "%s response" % get_current_function_name()

    def do_a_private_thing_publicly(self):
        """Should be, like, totally fine all the time."""
        return self.do_a_private_thing()

    def do_a_protected_thing_publicly(self):
        """Should be, like, totally fine all the time."""
        return self.do_a_protected_thing()


class Sub(Base):

    def do_another_private_thing_publicly(self):
        """Should raise AttributeError."""
        return self.do_a_private_thing()

    def do_another_protected_thing_publicly(self):
        """Should be, like, totally fine all the time."""
        return self.do_a_protected_thing()


class SubTwo(Base):

    def do_a_private_thing(self):
        """Should be, like, totally fine all the time."""
        return "%s response" % get_current_function_name()


class TestValidBaseClassAccess(TestValidAccess):

    scenarios = [
        ("validate_explicitly_public_method",
         {"method_name": "do_a_public_thing",
          "fixture_class": Base,
          "returns": "do_a_public_thing response",
          }
         ),
        ("validate_public_method_call_private_method",
         {"method_name": "do_a_private_thing_publicly",
          "fixture_class": Base,
          "returns": "do_a_private_thing response",
          }
         ),
        ("validate_explicitly_public_method_call_private_method",
         {"method_name": "do_a_protected_thing_publicly",
          "fixture_class": Base,
          "returns": "do_a_protected_thing response",
          }
         ),
        ]


class TestInvalidBaseClassAccess(TestInvalidAccess):

    scenarios = [
        ("private_method_inaccessible",
         {"method_name": "do_a_private_thing",
          "fixture_class": Base,
          "exception": access.PrivateAttributeError,
          }
         ),
        ("protected_method_inaccessible",
         {"method_name": "do_a_protected_thing",
          "fixture_class": Base,
          "exception": access.ProtectedAttributeError,
          }
         ),
        ]


class TestValidSubClassAccess(TestValidAccess):

    scenarios = [
        ("validate_public_method_call_private_method",
         {"method_name": "do_a_private_thing_publicly",
          "fixture_class": Sub,
          "returns": "do_a_private_thing response",
          }
         ),
        ("base_protected_method_accessible_from_inside_subclass",
         {"method_name": "do_another_protected_thing_publicly",
          "fixture_class": Sub,
          "returns": "do_a_protected_thing response",
          }
         ),
        ("public_subclass_method_overrides_private_baseclass_method",
         {"method_name": "do_a_private_thing",
          "fixture_class": SubTwo,
          "returns": "do_a_private_thing response",
          }
         ),
        ]


class TestInvalidSubClassAccess(TestInvalidAccess):

    scenarios = [
        ("base_private_method_inaccessible_from_outside_subclass",
         {"method_name": "do_a_private_thing",
          "fixture_class": Sub,
          "exception": access.PrivateAttributeError,
          }
         ),
        ("base_private_method_inaccessible_from_inside_subclass",
         {"method_name": "do_another_private_thing_publicly",
          "fixture_class": Sub,
          "exception": access.PrivateAttributeError,
          }
         ),
        ("base_protected_method_inaccessible_from_outside_subclass",
         {"method_name": "do_a_protected_thing",
          "fixture_class": Sub,
          "exception": access.ProtectedAttributeError,
          }
         ),
        ]
