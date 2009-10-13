# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the `simulate` function. See its documentation for more
information.

# todo: should be something that fishes step_options_profile from *args.
"""

import garlicsim
import garlicsim.misc
import history_browser as history_browser_module # Avoiding name clash

__all__ = ["simulate"]

def simulate(simpack, state, iterations=1, *args, **kwargs):
    """
    Simulate from the given state for the given number of iterations.

    A simpack must be passed as the first parameter. Any extraneous parameters
    will be passed to the step function.
    
    Returns the final state of the simulation.
    """
    simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    if simpack_grokker.history_dependent:
        return __history_simulate(simpack_grokker, state, iterations,
                                  *args, **kwargs)
    else: # It's a non-history-dependent simpack
        return __non_history_simulate(simpack_grokker, state, iterations,
                                  *args, **kwargs)

    
def __history_simulate(simpack_grokker, state, iterations=1, *args, **kwargs):
    """
    For history-dependent simulations only:
    
    Simulate from the given state for the given number of iterations.

    A simpack must be passed as the first parameter. Any extraneous parameters
    will be passed to the step function.
    
    Returns the final state of the simulation.
    """
    tree = garlicsim.data_structures.Tree()
    root = tree.add_state(state, parent=None)
    path = root.make_containing_path()
    history_browser = history_browser_module.HistoryBrowser(path)
    
    iterator = simpack_grokker.step_generator(history_browser, *args, **kwargs)
    
    current_node = root
    for i in range(iterations):
        current_state = iterator.next()
        current_node = tree.add_state(current_state, parent=current_node)
        
    final_state = current_state
    # Which is still here as the last value from the for loop
    
    return final_state


def __non_history_simulate(simpack_grokker, state, iterations,
                           *args, **kwargs):
    """
    For non-history-dependent simulations only:
    
    Simulate from the given state for the given number of iterations.

    A simpack must be passed as the first parameter. Any extraneous parameters
    will be passed to the step function.
    
    Returns the final state of the simulation.
    """
    iterator = simpack_grokker.step_generator(state, *args, **kwargs)
    for i in range(iterations):
        current_state = iterator.next()
        
    final_state = current_state
    # Which is still here as the last value from the for loop
    
    return final_state