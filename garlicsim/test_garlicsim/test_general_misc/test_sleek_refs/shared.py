# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Tools for testing `garlicsim.general_misc.sleek_refs`.'''

import weakref

def _is_weakreffable(thing):
    '''Return whether a weakref can be created to `thing`.'''
    try:
        weakref.ref(thing)
    except TypeError:
        return False
    else:
        return True

    
class A(object):
    '''A class with a static method.'''
    @staticmethod
    def s():
        pass

    
def counter(*args, **kwargs):
    '''Function that returns a higher number every time it's called.'''
    if not hasattr(counter, 'count'):
        counter.count = 0
    result = counter.count
    counter.count += 1
    return result
