# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Tests for `garlicsim.general_misc.temp_value_setters.TempRecursionLimitSetter`.
'''

from __future__ import with_statement

import sys

from garlicsim.general_misc.temp_value_setters import TempRecursionLimitSetter


def test():
    '''Test basic workings of `TempRecursionLimitSetter`.'''
    old_recursion_limit = sys.getrecursionlimit()
    assert sys.getrecursionlimit() == old_recursion_limit
    with TempRecursionLimitSetter(old_recursion_limit + 3):
        assert sys.getrecursionlimit() == old_recursion_limit + 3
    assert sys.getrecursionlimit() == old_recursion_limit
    