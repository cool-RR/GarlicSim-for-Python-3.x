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

from garlicsim.general_misc import import_tools

###############################################################################

def reduce_method(method):
    '''Reducer for methods.'''
    # todo: On Python 2.x this also works for unbound methods for some
    # mysterious reason. Unbound methods are still of the type `MethodType`, and
    # their `.im_self`/`.__self__` is None, so how does it work? Possibly
    # `pickle` in Python 2.x actually knows how to pickle unbound methods, and
    # doesn't really use this?
    #
    # In any case, in Python 3.x this works only for bound methods, and unbound
    # methods can't be pickled, which is an issue.
    return (getattr, (method.__self__, method.__func__.__name__))
    

copyreg.pickle(types.MethodType, reduce_method)

###############################################################################

def reduce_module(module):
    '''Reducer for modules.'''
    return (import_tools.normal_import, (module.__name__,))

copyreg.pickle(types.ModuleType, reduce_module)
