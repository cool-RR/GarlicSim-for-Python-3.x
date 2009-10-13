"""
This module defines the StepOptionsProfile class. See its documentation for
more information.
"""

import garlicsim.general_misc.arguments_profile

__all__ = ['StepOptionsProfile']

class StepOptionsProfile\
      (garlicsim.general_misc.arguments_profile.ArgumentsProfile):
    """
    A profile of *args and **kwargs to be used with a step function.
    
    Usage:
    
    step_options_profile = StepOptionsProfile(34, "meow", width=60)

    step(state, *arguments_profile.args, **arguments_profile.kwargs)
    # is equivalent to
    step(state, 34, "meow", width=60)
    
    """
    def __repr__(self):
        args_string = ', '.join([repr(thing) for thing in self.args])
        kwargs_string = ', '.join([str(key)+'='+repr(value) for \
                                   (key, value) in self.kwargs.items()])
        strings = [thing for thing in [args_string, kwargs_string] if \
                   thing]        
        big_string = ', '.join(strings)
        return 'StepOptionsProfile(%s)' % big_string