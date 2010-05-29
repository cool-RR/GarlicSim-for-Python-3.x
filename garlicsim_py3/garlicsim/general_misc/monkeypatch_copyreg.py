# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module monkeypatches the pickling dispatch table using `copyreg`.'''

# todo: alters global state, yuck! Maybe check before if it's already set to
# something?

import sys
import copyreg
import types
import builtins
import pickle

###############################################################################

def reduce_method(method):
    '''Reducer for methods.'''
    return (getattr, (method.__self__, method.__func__.__name__))

copyreg.pickle(types.MethodType, reduce_method)

###############################################################################

def __import__(*args, **kwargs):
    '''Wrapper for the builtin `__import__`'''
    # todo: This is needed when debugging in Wing, cause Wing replaces
    # `__import__` with its own. This feels bad.
    return builtins.__import__(*args, **kwargs)

def reduce_module(module):
    '''Reducer for modules.'''
    return (__import__, (module.__name__, {}, {}, [''])) # fromlist cruft

copyreg.pickle(types.ModuleType, reduce_module)

###############################################################################


def find_containing_object_of_function(function):
    # todo: cache?
    function_name = function.__name__
    module = sys.modules[function.__module__]
    objects_to_check = [module]
    while objects_to_check:
        object_to_check = objects_to_check.pop()
        if getattr(object_to_check, function_name, None) is function:
            return object_to_check
        try:
            sub_objects = vars(object_to_check)
        except TypeError: # The object doesn't have a vars/__dict__
            pass
        for sub_object in sub_objects.values():
            if isinstance(sub_object, type):
                objects_to_check.append(sub_object)
        
    raise LookupError('''Couldn't find the %s function for pickling/deepcopying \
it. I tried looking around in the %s module, but it either wasn't there or \
was in a non-obvious place.''' % (function, module))
    
    
def reduce_function(function):
    '''
    Reducer for functions.
    
    This is needed only for methods, which in Python 3 are functions. But it
    gets called for plain functions too, and it tries not to fuck it up in that
    case.
    
    This is hackish and would probably fail sometimes. I had to do it because
    there's a problem with finding a method's class in Python 3.
    '''
    containing_object = find_containing_object_of_function(function)
    return (getattr, (containing_object, function.__name__))

copyreg.pickle(types.FunctionType, reduce_function)

del pickle._Pickler.dispatch[types.FunctionType]
# This is a screamingly ugly hack. I'm sorry from the bottom of my heart. But
# `pickle` would just not agree to use the reducer we defined as long as it
# finds its own in its `.dispatch` dict.

###############################################################################