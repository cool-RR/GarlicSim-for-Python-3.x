# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackMetadata` class.

See its documentation for more information.
'''

import collections

from garlicsim.general_misc import module_tasting
from garlicsim.general_misc import caching


_SimpackMetadataBase = collections.namedtuple(
                           '_SimpackMetadataBase',
                           'address name version description tags',
                       )


class SimpackMetadata(_SimpackMetadataBase):
    
    def __init__(self, *args, **kwargs):
        
        _SimpackMetadataBase.__init__(self, *args, **kwargs)
        
        assert isinstance(self.address, str) or self.address is None
        assert isinstance(self.name, str) or self.name is None
        assert isinstance(self.version, str) or self.version is None
        assert isinstance(self.description, str) or self.description is None
        assert isinstance(self.tags, tuple) or self.tags is None        
        
        
        if False: # This section gives us better source assistance in Wing IDE:
            self.address = self.address
            self.name = self.name
            self.version = self.version
            self.description = self.description
            self.tags = self.tags
        
    
    @staticmethod
    @caching.cache()
    def create_from_address(address):
        tasted_simpack = module_tasting.taste_module(address)
        name = getattr(tasted_simpack, 'name', address.rsplit('.')[-1])
        version = getattr(tasted_simpack, 'name', None)
        description = getattr(tasted_simpack, '__doc__', None)
        tags = getattr(tasted_simpack, 'tags', None)
        return SimpackMetadata(address=address,
                               name=name,
                               version=version,
                               description=description,
                               tags=tags)



