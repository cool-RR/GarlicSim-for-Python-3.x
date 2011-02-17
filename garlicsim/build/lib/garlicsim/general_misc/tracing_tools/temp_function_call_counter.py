# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `TempFunctionCallCounter` context manager.

See its documentation for more details.
'''

import sys
import collections

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import address_tools

from garlicsim.general_misc.temp_value_setters import TempValueSetter
from .count_calls import count_calls


class TempFunctionCallCounter(TempValueSetter):
    '''
    Temporarily counts the number of calls made to a function.
    
    Example:
    
        f()
        with TempFunctionCallCounter(f) as counter:
            f()
            f()
        assert counter.call_count == 2
        
    '''
    
    def __init__(self, function):
        '''
        Construct the `TempFunctionCallCounter`.
        
        For `function`, you may pass in either a function object, or a
        `(parent_object, function_name)` pair, or a `(getter, setter)` pair.
        '''
        
        if isinstance(function, collections.Iterable):
            first, second = function
            if isinstance(second, str):
                actual_function = getattr(first, second)
            else:
                assert isinstance(first, collections.Callable) and \
                       isinstance(second, collections.Callable)
                actual_function = first() # `first` is the getter in this case.
                
        else: # not isinstance(function, collections.Iterable)
            assert isinstance(function, collections.Callable)
            actual_function = function
            try:
                address = address_tools.object_to_string.get_address(function)
                parent_object_address, function_name = address.rsplit('.', 1)
                parent_object = address_tools.resolve(parent_object_address)
            except Exception:
                raise Exception("Couldn't obtain parent/name pair from "
                                "function; Supply one manually or "
                                "alternatively supply a getter/setter pair.")
            first, second = parent_object, function_name
            
        self.call_counting_function = count_calls(actual_function)
        
        TempValueSetter.__init__(
            self,
            (first, second),
            value=self.call_counting_function
        )
        
        
    call_count = property(
        lambda self: getattr(self.call_counting_function, 'call_count', 0)
    )
    '''The number of calls that were made to the function.'''
    
    