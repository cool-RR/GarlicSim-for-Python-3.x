# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `TempImportHookSetter` class.

See its documentation for more details.
'''

import builtins
import collections

from .temp_value_setter import TempValueSetter


class TempImportHookSetter(TempValueSetter):
    '''
    Context manager for temporarily setting a function as the import hook.
    '''
    def __init__(self, import_hook):
        '''
        Construct the `TempImportHookSetter`.
        
        `import_hook` is the function to be used as the import hook.
        '''
        assert isinstance(import_hook, collections.Callable)
        TempValueSetter.__init__(self,
                                 (builtins, '__import__'),
                                 value=import_hook)