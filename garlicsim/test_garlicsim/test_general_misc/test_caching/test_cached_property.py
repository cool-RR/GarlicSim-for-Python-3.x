# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing module for `garlicsim.general_misc.caching.CachedProperty`.
'''

import nose

from garlicsim.general_misc.caching import (cache, CachedType,
                                            CachedProperty)


def counting_func(self):
    '''Function that returns a bigger number every time.'''
    if not hasattr(counting_func, 'i'):
        counting_func.i = 0
    try:
        return counting_func.i
    finally:
        counting_func.i = (counting_func.i + 1)
    
        
def test():
    '''Test basic workings of `CachedProperty`.'''    
    class A(object):
        personality = CachedProperty(counting_func)
    
    assert isinstance(A.personality, CachedProperty)
        
    a1 = A()
    assert a1.personality == a1.personality == a1.personality
    
    a2 = A()
    assert a2.personality == a2.personality == a2.personality 
    
    assert a2.personality == a1.personality + 1        


def test_as_decorator():
    '''Test `CachedProperty` can work as a decorator.'''
    class B(object):
        @CachedProperty
        def personality(self):
            if not hasattr(B.personality, 'i'):
                B.personality.i = 0
            try:
                return B.personality.i
            finally:
                B.personality.i = (B.personality.i + 1)
    
    assert isinstance(B.personality, CachedProperty)                
                
    b1 = B()
    assert b1.personality == b1.personality == b1.personality

    
    b2 = B()
    assert b2.personality == b2.personality == b2.personality 
    
    assert b2.personality == b1.personality + 1
        
    
def test_with_name():
    '''Test `CachedProperty` works with correct name argument.'''
    class A(object):
        personality = CachedProperty(counting_func, name='personality')
    
    a1 = A()
    assert a1.personality == a1.personality == a1.personality
    
    a2 = A()
    assert a2.personality == a2.personality == a2.personality 
    
    assert a2.personality == a1.personality + 1
        
    
def test_with_wrong_name():
    '''Test `CachedProperty`'s behavior with wrong name argument.'''
        
    class A(object):
        personality = CachedProperty(counting_func, name='meow')
    
    a1 = A()
    assert a1.personality == a1.meow == a1.personality - 1 == \
           a1.personality - 2
    
    a2 = A()
    assert a2.personality == a2.meow == a2.personality - 1 == \
           a2.personality - 2
    
    
def test_on_false_object():
    '''Test `CachedProperty` on class that evaluates to `False`.'''
    
    class C(object):
        @CachedProperty
        def personality(self):
            if not hasattr(C.personality, 'i'):
                C.personality.i = 0
            try:
                return C.personality.i
            finally:
                C.personality.i = (C.personality.i + 1)
        
        def __bool__(self):
            return False
        
        __nonzero__ = __bool__
        
    assert isinstance(C.personality, CachedProperty)
                
    c1 = C()
    assert not c1
    assert c1.personality == c1.personality == c1.personality
    
    c2 = C()
    assert not c2
    assert c2.personality == c2.personality == c2.personality 
    
    assert c2.personality == c1.personality + 1