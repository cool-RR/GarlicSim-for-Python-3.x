# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module monkey-patches the pickling dispatch table using `copy_reg`.'''

# todo: alters global state, yuck! Maybe check before if it's already set to
# something?

import copy_reg
import types
import builtins

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

copy_reg.pickle(types.ModuleType, reduce_module)

###############################################################################