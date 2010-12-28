# Copyright 2009-2011 Ram Rachum.
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


def round_to_int(x, up=False):
    '''
    Round a number to an `int`.
    
    This is mostly used for floating points. By default, it will round the
    number down, unless the `up` argument is set to `True` and then it will
    round up.
    
    If you want to round a number to the closest `int`, just use
    `int(round(x))`.
    '''
    rounded_down = int(x // 1)
    if up:
        return int(x) if (isinstance(x, float) and x.is_integer()) \
               else rounded_down + 1
    else:
        return rounded_down
