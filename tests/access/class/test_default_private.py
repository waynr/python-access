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


class TestDefaultPrivateClassDecorator(testtools.TestCase):

    def setUp(self):
        self.baseclassaseclass = PrivateBase()
        self.subclass = PrivateSub()
        super(TestDefaultPrivateClassDecorator, self).setUp()

    def tearDown(self):
        super(TestDefaultPrivateClassDecorator, self).tearDown()

    def test_methods_private_by_default(self):
        """ validate AttributeError raised by default whenever attempting to
        access methods that are not otherwise decorated.
        """
        with testtools.ExpectedException(AttributeError,
                                         ".*has no attribute.*"):
            self.baseclass.do_a_private_thing()

    def test_validate_explicitly_public_methods(self):
        """ validate that instances with default private behavior can still access
        methods explicitly marked as public.
        """
        self.assertEqual(self.subclass.do_a_public_thing(),
                         "do_a_public_thing response")

    def test_validate_explicitly_public_methods_from_subclass(self):
        """ validate that classes with default private behavior can still access
        methods explicitly marked as public.
        """
        self.assertEqual(self.subclass.do_a_public_thing(),
                         "do_a_public_thing response")

    def test_validate_explicitly_protected_methods(self):
        """ validate AttributeError raised whenever attempting to access an
        explicitly protected method from outer scope

        """
        self.assertEqual(self.baseclass.do_a_protected_thing(),
                         "do_a_protected_thing response")

    def test_default_private_baseclass_method_private_to_subclass(self):
        """ validate AttributeError raised by default whenever attempting to
        access a default-private method defined on baseclass from the subclass.
        """
        with testtools.ExpectedException(AttributeError,
                                         ".*has no attribute.*"):
            self.subclass.do_a_private_thing()

    def test_subclass_does_not_inherit_default_private_behavior(self):
        """ validate that subclass of a private class with default private
        method access behavior does not inherit that default private behavior
        from its base class.
        """
        self.assertEqual(self.subclass.do_another_public_thing(),
                         "do_another_public_thing response")

    def test_subclass_uses_private_method_decorator(self):
        """ validate that subclass of a private class with default private
        method access behavior can still have explicitly-labeled private
        methods.
        """
        self.assertEqual(self.subclass.do_another_public_thing(),
                         "do_another_private_thing response")

        with testtools.ExpectedException(AttributeError,
                                         ".*has no attribute.*"):
            self.subclass.do_a_private_thing()
