# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `BaseHistoryBrowser` class.

See its documentation for more info.
'''

import abc
from garlicsim.general_misc import binary_search


__all__ = ['BaseHistoryBrowser']


get_state_clock = lambda state: state.clock

class BaseHistoryBrowser(object, metaclass=abc.ABCMeta):
    '''
    A device for requesting information about the history of the simulation.

    With a `HistoryBrowser` one can request states from the simulation's
    timeline. States can be requested by clock time or position in the timeline
    or by other measures; see documentation for this class's methods.
    
    This is an abstract base class from which all history browsers should
    subclass.
    '''
    
    @abc.abstractmethod
    def get_last_state(self):
        '''
        Get the last state in the timeline.
        
        Identical to `.__getitem__(-1).`
        '''

        
    @abc.abstractmethod
    def __getitem__(self, i):
        '''Get a state by its position in the timeline.'''

                
    @abc.abstractmethod
    def get_state_by_monotonic_function(self, function, value, rounding):
        '''
        Get a state by specifying a measure function and a desired value.
        
        The function must be a monotonic rising function on the timeline.
        
        See documentation of `garlicsim.general_misc.binary_search.roundings`
        for details about rounding options.
        '''
        
        
    @abc.abstractmethod
    def __len__(self):
        '''Get the length of the timeline in nodes.'''
    
        
    def get_state_by_clock(self, clock, rounding=binary_search.CLOSEST):
        '''
        Get a state by specifying desired clock time.
        
        See documentation of `garlicsim.general_misc.binary_search.roundings`
        for details about rounding options.
        '''
        assert issubclass(rounding, binary_search.Rounding)
        return self.get_state_by_monotonic_function\
               (function=get_state_clock, value=clock, rounding=rounding)
    
    
