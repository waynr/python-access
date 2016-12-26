#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_instance_method_access
----------------------------------

Tests for `access.private`, `access.protected`, and `access.public`.
"""

import testtools

import access


class Base:

    @access.private
    def do_a_private_thing(self):
        """Should raise AttributeError when called outside Base."""
        return "teehee"

    @access.protected
    def do_a_protected_thing(self):
        """Should raise AttributeError when called outside Base or its sub
        classes."""
        return "oh hello"

    def do_a_public_thing(self):
        """Should be, like, totally fine all the time."""
        return "meow"

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


class TestInstanceMethodAccessControl(testtools.TestCase):

    def setUp(self):
        self.baseclassaseclass = Base()
        self.subclass = Sub()
        super(TestInstanceMethodAccessControl, self).setUp()

    def tearDown(self):
        super(TestInstanceMethodAccessControl, self).tearDown()

    def test_public_default(self):
        """ validate implementation doesn't somehow break default public access
        """
        self.assertEqual(self.baseclass.do_a_public_thing(), "meow")


class TestPrivateInstanceMethodAccess(TestInstanceMethodAccessControl):

    def test_raises_from_outside_class_scope(self):
        """ validate AttributeError raised when attempting to access a private
        method from outside class scope
        """
        with testtools.ExpectedException(AttributeError,
                                         ".*has no attribute.*"):
            self.baseclass.do_a_private_thing()

        with testtools.ExpectedException(AttributeError,
                                         ".*has no attribute.*"):
            self.subclass.do_a_private_thing()

    def test_raises_from_subclass(self):
        """ validate AttributeError raised when attempting to access a private
        method from subclass scope
        """
        with testtools.ExpectedException(AttributeError,
                                         ".*has no attribute.*"):
            self.subclass.do_another_private_thing_publicly()

    def test_valid_from_within_class(self):
        """ validate implementation doesn't somehow break base class access to
        its own private methods
        """
        self.assertEqual(self.baseclass.do_a_private_thing_publicly(),
                         "teehee")

    def test_valid_from_public_method_called_by_subclass(self):
        """ validate implementation doesn't somehow break access to base class
        private method when called from within public method in turn called by
        sub class public method.
        """
        self.assertEqual(self.subclass.do_a_private_thing_publicly(), "teehee")


class TestProtectedInstanceMethodAccess(TestInstanceMethodAccessControl):

    def test_raises_from_outside_class_scope(self):
        """ validate AttributeError raised when attempting to access a
        protected method directly from outside class scope
        """
        with testtools.ExpectedException(AttributeError,
                                         ".*has no attribute.*"):
            self.baseclass.do_a_protected_thing()

    def test_raises_from_subclass(self):
        """ validate AttributeError raised when attempting to access a
        protected method directly from subclass scope
        """
        with testtools.ExpectedException(AttributeError,
                                         ".*has no attribute.*"):
            self.subclass.do_a_protected_thing()

    def test_valid_from_within_class(self):
        """ validate implementation doesn't somehow break base class access to
        its own protected methods
        """
        self.assertEqual(self.baseclass.do_a_protected_thing_publicly(),
                         "oh hello")

    def test_valid_from_public_method_called_by_subclass(self):
        """ validate implementation doesn't somehow break access to base class
        protected method when called from within public method in turn called
        by sub class public method.
        """
        self.assertEqual(self.subclass.do_a_protected_thing_publicly(),
                         "oh hello")

    def test_valid_from_protected_method_called_by_subclass(self):
        """ validate implementation doesn't somehow break access to base class
        protected method when called from within public method in turn called
        by sub class public method.
        """
        self.assertEqual(self.subclass.do_another_protected_thing_publicly(),
                         "oh hello")
