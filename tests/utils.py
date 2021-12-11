#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect


def get_current_function_name():
    return inspect.stack()[1][3]
