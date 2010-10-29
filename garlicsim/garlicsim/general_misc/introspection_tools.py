from garlicsim.general_misc.third_party import inspect

from garlicsim.general_misc.third_party.ordered_dict import OrderedDict

# tododoc: test
def get_default_args_dict(function):
    arg_spec = inspect.getargspec(function)
    (s_args, s_star_args, s_star_kwargs, s_defaults) = arg_spec
        
    # `getargspec` has a weird policy, when inspecting a function with no
    # defaults, to give a `defaults` of `None` instead of the more consistent
    # `()`. We fix that here:
    if s_defaults is None:
        s_defaults = ()
    
    # The number of args which have default values:
    n_defaultful_args = len(s_defaults)
    
    defaultful_args = s_args[-n_defaultful_args:] if n_defaultful_args \
                       else []
    
    return OrderedDict(zip(defaultful_args, s_defaults))
    
    