# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CachedProperty` class.

See its documentation for more details.
'''


class CachedProperty(object):
    '''
    A property that is calculated (a) lazily and (b) only once for an object.
    
    Usage:
    
        class MyObject(object):
        
            # ... Regular definitions here
        
            def _get_personality(self):
                print('Calculating personality...')
                time.sleep(5) # Time consuming process that creates personality
                return 'Nice person'
        
            personality = CachedProperty(_get_personality)
    
    '''
    def __init__(self, getter, doc=None, name=None):
        '''
        Construct the cached property.
        
        You may optionally pass in the name that this property has in the
        class; this will save a bit of processing later.
        '''
        self.getter = getter
        self.our_name = name
        self.__doc__ = doc or getattr(getter, '__doc__', None)
        
        
    def __get__(self, obj, our_type=None):

        if obj is None:
            # We're being accessed from the class itself, not from an object
            return self
        
        value = self.getter(obj)
        
        if not self.our_name:
            if not our_type:
                our_type = type(obj)
            (self.our_name,) = (name for name in dir(our_type) if
                                getattr(our_type, name, None) is self)
        
        setattr(obj, self.our_name, value)
        
        return value

    
