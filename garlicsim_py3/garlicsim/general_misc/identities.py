# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `HasIdentity` class.

See its documentation for more information.
'''

from garlicsim.general_misc import caching
from garlicsim.general_misc.persistent import CrossProcessPersistent


class HasIdentity(object):
    '''
    An object that has a persistent identity.
    
    When you make deepcopies of this object using `DontCopyPersistent()`, the
    new copies will have the same "identity" as the original object:
    
        >>> class A(HasIdentity):
        ...     pass
        >>> a0 = A()
        >>> a1 = copy.deepcopy(a0, DontCopyPersistent)
        >>> a0.has_same_identity_as(a1)
        True
        >>> a0 & a1 # Shortcut for `has_same_identity_as`
        True
        
    (`DontCopyPersistent` is available as
    `garlicsim.general_misc.persistent.DontCopyPersistent`)    
    '''
    def __init__(self):
        self.__identity = CrossProcessPersistent()
        '''The object's persistent identity.'''

        
    def has_same_identity_as(self, other):
        '''Does `other` have the same identity as us?'''
        if not isinstance(other, HasIdentity):
            return NotImplemented
        return self.__identity.has_same_uuid_as(other.__identity)
    
    __and__ = has_same_identity_as
    
    
    @caching.CachedProperty
    def personality(self):
        '''Personality containing a human name and two colors.'''
        return self.__identity.personality
        
        