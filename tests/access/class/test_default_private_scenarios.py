#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_default_private
--------------------------

Tests for `access.default(access.PRIVATE)` class decorator.
"""

import inspect

import testtools
from testscenarios.testcase import TestWithScenarios

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

    @access.public
    def do_a_private_thing_publicly(self):
        """Should be, like, totally fine all the time."""
        return self.do_a_private_thing()


class PrivateSub(PrivateBase):
    def do_another_public_thing():
        """Should be, like, totally fine all the time."""
        return "%s response" % get_current_function_name()

    @access.private
    def do_another_private_thing():
        """Should raise AttributeError when called outside Base or its sub
        classes."""
        return "%s response" % get_current_function_name()

    def do_another_private_thing_publicly(self):
        """Should raise AttributeError when called outside Base or its sub
        classes."""
        return self.do_another_private_thing()

    def do_a_protected_thing_publicly(self):
        """Should be, like, totally fine all the time."""
        return self.do_a_protected_thing()


class DefaultPrivateClassDecoratorBase(TestWithScenarios,
                                       testtools.TestCase):
    pass


class TestDPCDExceptions(DefaultPrivateClassDecoratorBase):

    scenarios = [
        ("methods_private_by_default",
         {"method_name": "do_a_private_thing",
          "fixture_class": PrivateBase,
          "exception": access.PrivateAttributeError,
          }
         ),
        ("methods_private_by_default_from_subclass",
         {"method_name": "do_a_private_thing",
          "fixture_class": PrivateSub,
          "exception": access.PrivateAttributeError,
          }
         ),
        ("subclass_can_use_explicit_private_method_decorator",
         {"method_name": "do_another_private_thing",
          "fixture_class": PrivateSub,
          "exception": access.PrivateAttributeError,
          }
         ),
        ("explicitly_public_method_call_private_method_from_subclass",
         {"method_name": "do_another_private_thing_publicly",
          "fixture_class": PrivateSub,
          "exception": access.PrivateAttributeError,
          }
         ),

        ("explicitly_protected_method_inaccessible",
         {"method_name": "do_a_protected_thing",
          "fixture_class": PrivateBase,
          "exception": access.ProtectedAttributeError,
          }
         ),
        ("explicitly_protected_method_inaccessible_from_subclass",
         {"method_name": "do_a_protected_thing",
          "fixture_class": PrivateSub,
          "exception": access.ProtectedAttributeError,
          }
         ),
        ]

    def test_scenario(self):
        instance = self.fixture_class()
        method = getattr(instance, self.method_name)

        with testtools.ExpectedException(self.exception,
                                         ".*has no attribute.*"):
            method()


class TestDPCDValid(DefaultPrivateClassDecoratorBase):

    scenarios = [
        ("validate_explicitly_public_method",
         {"method_name": "do_a_public_thing",
          "fixture_class": PrivateBase,
          "returns": "do_a_public_thing response",
          }
         ),
        ("validate_explicitly_public_method_from_subclass",
         {"method_name": "do_a_public_thing",
          "fixture_class": PrivateSub,
          "returns": "do_a_public_thing response",
          }
         ),

        ("validate_explicitly_public_method_call_private_method",
         {"method_name": "do_a_private_thing_publicly",
          "fixture_class": PrivateBase,
          "returns": "do_a_private_thing response",
          }
         ),
        ("validate_public_method_call_protected_method_from_subclass",
         {"method_name": "do_a_protected_thing_publicly",
          "fixture_class": PrivateSub,
          "returns": "do_a_protected_thing response",
          }
         ),

        ("subclass_should_not_inherit_default_private_behavior",
         {"method_name": "do_another_public_thing",
          "fixture_class": PrivateSub,
          "returns": "do_another_public_thing response",
          }
         ),
        ]

    def test_scenario(self):
        instance = self.fixture_class()
        method = getattr(instance, self.method_name)

        self.assertEqual(method(), self.returns)