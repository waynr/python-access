#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_method_decorators
----------------------

Tests for `access.private`, `access.protected`, and `access.public` decorators.
All tests in this module assume that the default behavior of an undecorated
method is to permit methods to be accessible on the object from any context.

"""

import testtools

import access


class Base:

    @access.private
    def do_a_private_thing(self):
        """Should raise AttributeError when called outside Base."""
        return "private response"

    @access.protected
    def do_a_protected_thing(self):
        """Should raise AttributeError when called outside Base or its sub
        classes."""
        return "protected response"

    def do_a_public_thing(self):
        """Should be, like, totally fine all the time."""
        return "public response"

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
        self.bbaseclassaseclassaseclass = Base()
        self.subclass = Sub()
        super(TestInstanceMethodAccessControl, self).setUp()

    def tearDown(self):
        super(TestInstanceMethodAccessControl, self).tearDown()

