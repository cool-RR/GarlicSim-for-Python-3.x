# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for comparisons.'''

import sys


def underscore_hating_cmp(a, b):
    '''Compare two strings, counting the "_" character as highest.'''
    assert isinstance(a, str) and isinstance(b, str)
    return cmp(
        str(a).replace('_', unichr(sys.maxunicode)),
        str(b).replace('_', unichr(sys.maxunicode))
    )
