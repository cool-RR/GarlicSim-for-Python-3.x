# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import copy
import math
from math import pi
import random
random.seed()

from garlicsim.misc import StepCopy
import garlicsim.data_structures

def make_plain_state(*args, **kwargs):
    state=garlicsim.data_structures.State()
    state.left = 0
    state.left_vel = 0
    state.right = 0
    return state

def make_random_state(*args, **kwargs):
    state=garlicsim.data_structures.State()
    state.left = random.random() * 2 * pi
    state.left_vel = 0
    state.right = random.random() * 2 * pi
    return state


def history_step(history_browser, t=0.1, *args, **kwargs):

    last_state = history_browser.get_last_state()
    new_state = copy.deepcopy(last_state, StepCopy())
    new_state.clock += t
    
    useless_state = history_browser.get_state_by_clock(10000000)
    assert useless_state.clock == last_state.clock    
    
    new_state.left_vel += random.random() * 0.2 - 0.1
    new_state.left += new_state.left_vel * t
    
    past_state = history_browser.get_state_by_clock(new_state.clock - 20)
    if past_state is not None:
        new_state.right = past_state.left
        
    return new_state
