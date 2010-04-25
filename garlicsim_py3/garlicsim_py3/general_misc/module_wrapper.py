# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import types

discardables = ['__builtins__']

wrapped_modules = {}

def module_wrapper_factory(module):
    '''
    Given a module, returns a ModuleWrapper which is almost identical to the
    module, with the difference being that it can be pickled.
    '''
    if module in wrapped_modules:
        return wrapped_modules[module]
    else:
        module_wrapper = ModuleWrapper(module)
        return module_wrapper

class ModuleWrapper(object):
    def __init__(self, module):
        wrapped_modules[module] = self
        self.__dict__ = dict(module.__dict__)
        for name, thing in list(self.__dict__.items()):
            '''
            Note this is a weak form of recursive scanning
            '''
            if name in discardables:
                self.__dict__[name] = "Missing item, string representation:" +\
                                      str(thing)
                continue
            if isinstance(thing, types.ModuleType):
                self.__dict__[name] = "Missing module " + thing.__name__
                continue
                
                
if __name__ == "__main__":
    import pickle
    def test(module):
        try:
            pickle.dumps(ModuleWrapper(module))
            return True
        except Exception:
            return False
        
    import garlicsim_wx.simulation_packages.life as life
    print((test(life)))
    pickle.dumps(ModuleWrapper(life))