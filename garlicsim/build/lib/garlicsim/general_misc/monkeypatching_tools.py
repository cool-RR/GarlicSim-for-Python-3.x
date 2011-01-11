# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Tools for monkeypatching.'''

import types


def monkeypatch_method(class_, name=None):
    '''
    Monkeypatch a method into a class.
    
    Example:
    
        class A(object):
            pass
    
        @monkeypatch_method(A)
        def my_method(a):
            return (a, 'woo!')
        
        a = A()
        
        assert a.my_method() == (a, 'woo!')
        
    You may use the `name` argument to specify a method name different from the
    function's name.
    '''
    def decorator(function):
        # Note that unlike most decorators, this decorator retuns the function
        # it was given without modifying it. It modifies the class only.
        name_ = name or function.__name__
        setattr(class_, name_, function)
        return function
    return decorator