# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines miscellaneous tools.'''

import math


def frange(start, finish=None, step=1.):
    '''
    Make a list containing an arithmetic progression of numbers.

    This is an extension of the builtin `range`; It allows using floating point
    numbers.
    '''
    if finish is None:
        finish, start = start, 0.
    else:
        start = float(start)

    count = int(math.ceil(finish - start)/step)
    return (start + n*step for n in range(count))


def shorten_class_address(module_name, class_name):
    '''
    Shorten the address of a class.
    
    This is mostly used in `__repr__` methods of various classes to shorten the
    text and make the final output more conscise. For example, if you have a
    class `garlicsim.asynchronous_crunching.project.Project`, but which is also
    available as `garlicsim.Project`, this function will return
    'garlicsim.Project'.    
    '''
    get_module = lambda module_name: __import__(module_name, fromlist=[''])
    original_module = get_module(module_name)
    original_class = getattr(original_module, class_name)
    
    current_module_name = module_name
    
    last_successful_module_name = current_module_name
    
    while True:
        # Removing the last submodule from the module name:
        current_module_name = '.'.join(current_module_name.split('.')[:-1]) 
        
        if not current_module_name:
            # We've reached the top module and it's successful, can break now.
            break
        
        current_module = get_module(current_module_name)
        
        candidate_class = getattr(current_module, class_name, None)
        
        if candidate_class is original_class:
            last_successful_module_name = current_module_name
        else:
            break
        
    return '.'.join((last_successful_module_name, class_name))


class LazilyEvaluatedConstantProperty(object):
    '''
    A property that is calculated (a) lazily and (b) only once for an object.
    
    Usage:
    
        class MyObject(object):
        
            # ... Regular definitions here
        
            def _get_personality(self):
                print('Calculating personality...')
                time.sleep(5) # Time consuming process that creates personality
                return 'Nice person'
        
            personality = LazilyEvaluatedConstantProperty(_get_personality)
    
    '''
    def __init__(self, getter, name=None):
        '''
        Construct the LEC-property.
        
        You may optionally pass in the name the this property has in the class;
        This will save a bit of processing later.
        '''
        self.getter = getter
        self.our_name = name
        
        
    def __get__(self, obj, our_type=None):

        value = self.getter(obj)
        
        if not self.our_name:
            if not our_type:
                our_type = type(obj)
            (self.our_name,) = (key for (key, value) in 
                                vars(our_type).iteritems()
                                if value is self)
        
        setattr(obj, self.our_name, value)
        
        return value
        
        
if __name__ == '__main__': # todo: move to test suite
    import random
    class A(object):
        def _get_personality(self):
            print(
                "Calculating personality for %s. (Should happen only once.)" % self
            )
            return random.choice(['Angry', 'Happy', 'Sad', 'Excited'])
        personality = LazilyEvaluatedConstantProperty(_get_personality)
    a = A()
    print(a.personality)
    print(a.personality)
    print(a.personality)
    
    a2 = A()
    print(a2.personality)
    print(a2.personality)
    print(a2.personality)
    