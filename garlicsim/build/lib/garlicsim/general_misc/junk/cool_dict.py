# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the CoolDict class. See its documentation for more
information.
'''

# remove has_key from all places

import copy

class CoolDict(dict):
    '''
    A class derived from dict which defines some extra methods.
    '''
    def raise_to(self, key, value):
        '''
        Same as `cool_dict[key] = value`, except if the cool dict already has
        `key`, and its value is higher than `value`.
        '''
        has_key = key in self
        if not has_key:
            self[key] = value
        else:
            self[key] = max(value, self[key])
            
    def lower_to(self, key, value):
        '''
        Same as `cool_dict[key] = value`, except if the cool dict already has
        `key`, and its value is lower than `value`.
        '''
        has_key = key in self
        if not has_key:
            self[key] = value
        else:
            self[key] = min(value, self[key])
            
    def copy(self):
        return CoolDict(self)
    
    def __copy__(self):
        return CoolDict(self)
    
    def __deepcopy__(self, memo):
        raise NotImplementedError # todo
    
    def transfer_value(self, key, new_key):
        assert key in self
        assert new_key not in self
        
        value = self[key]
        self[new_key] = value
        del self[key]
        
        return value