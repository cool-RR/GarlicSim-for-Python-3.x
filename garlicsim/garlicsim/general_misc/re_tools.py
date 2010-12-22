# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines miscellaneous tools.'''

import re


def searchall(pattern, string, flags=0):
    '''
    Return all the substrings of `string` that match `pattern`.
    
    Note: Currently returns only non-overlapping matches.
    '''
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern, flags=flags)
    matches = []
    start = 0
    end = len(string)
    
    while True:
        match = pattern.search(string, start, end)
        if match:
            matches.append(match)
            start = match.end()
        else:
            break
    
    return matches
        