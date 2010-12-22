# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `BaseStepIterator` class.

See its documentation for more information.
'''

import copy
import abc

from collections import Iterator

import garlicsim


class BaseStepIterator(Iterator, metaclass=abc.ABCMeta):
    '''
    An iterator that uses a simpack's step function to produce states.
    
    A step iterator uses the simpack's original step function (or generator)
    under the hood.
    
    The step iterator automatically adds `.clock` readings if the states
    produced by the step function are missing them.
    
    This is an abstract base class; The `garlicsim.misc.step_iterators` package
    contains a collection of step iterators, one for each step type.
    '''

    
    @abc.abstractmethod
    def __init__(self, state_or_history_browser, step_profile):
        pass

    
    @abc.abstractmethod
    def __next__(self):
        '''Crunch the next state.'''
        