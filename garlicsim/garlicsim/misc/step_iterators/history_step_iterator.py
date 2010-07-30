# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the HistoryStepIterator class.

See its documentation for more information.
'''


import copy

import garlicsim
from garlicsim.misc import BaseStepIterator, SimpackError, AutoClockGenerator


class HistoryStepIterator(BaseStepIterator):
    '''
    An iterator that uses a simpack's step to produce states.
    
    The StepIterator uses under the hood the simpack's step function, be it a
    simple step function or a step generator. Using a StepIterator instead of
    using the simpack's step has a few advantages:
    
    1. The StepIterator automatically adds clock readings if the states are
       missing them.
    2. It's possible to change the step profile while iterating.    
    3. Unless the step function raises `WorldEnd` to end the simulation, this
       iterator is guaranteed to be infinite, even if the simpack's iterator is
       finite.
    
    And possibly more.  
    '''
    # todo: make stuff private here?
    def __init__(self, history_browser, step_profile):

        self.history_step_function = step_profile.step_function
        
        self.raw_iterator = None
        
        self.step_profile = copy.deepcopy(step_profile)
        
        self.current_state = None
        self.history_browser = state_or_history_browser
            
        self.auto_clock_generator = AutoClockGenerator()
            
        self.step_profile_changed = False
        
        
    def __iter__(self): return self

    
    def next(self):
        '''Crunch the next state.'''
        self.current_state = self.history_step_function(
            self.history_browser,
            *self.step_profile.args,
            **self.step_profile.kwargs
        )
        self.auto_clock(self.current_state)
        return self.current_state
    
        
    def auto_clock(self, state):
        '''If the state has no clock reading, give it one automatically.'''
        state.clock = self.auto_clock_generator.make_clock(state)

    