'''tododoc

todo: maybe class instead of func?
todo: make WarehouseError and fuck assert
'''

import os
import garlicsim.general_misc.import_tools as import_tools
import warnings

__all__ = ['create']


def create(package):
    '''
    tododoc
    Simply pass __file__ into this function.
    
    todo: works when frozen?
    '''
    
    things = {}
    modules = import_tools.import_all(package)
    for (module_name, module) in modules.items():
        assert hasattr(module, '__all__'), '''Module in warehouse must define \
__all__ which declares exactly which objects should be collected.'''
        for name in module.__all__:
            assert name not in things, 'Duplicity.'
            things[name] = getattr(module, name)
        
    return things
