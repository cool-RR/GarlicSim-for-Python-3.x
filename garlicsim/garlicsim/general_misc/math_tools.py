# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines math-related tools.'''

def sign(x):
    '''Get the sign of a number.'''
    if x > 0:
        return 1
    if x == 0:
        return 0
    assert x < 0
    return -1

def cmp(a, b):
    '''
    Compare two objects.
    
    Returns 1 if a > b, returns -1 if b > a, returns 0 if they're equal.
    '''
    return (a > b) - (a < b)