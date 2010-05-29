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
