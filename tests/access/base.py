#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
base
----

Define base classes for python-access testing.

"""
import testtools
from testscenarios.testcase import TestWithScenarios


class TestValidAccess(TestWithScenarios,
                      testtools.TestCase):
    def test_scenario(self):
        instance = self.fixture_class()
        method = getattr(instance, self.method_name)

        self.assertEqual(method(), self.returns)


class TestInvalidAccess(TestWithScenarios, testtools.TestCase):
    def test_scenario(self):
        instance = self.fixture_class()
        method = getattr(instance, self.method_name)

        with testtools.ExpectedException(self.exception,
                                         ".*has no attribute.*"):
            method()
