# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `FunctionAnchoringType` class.

See its documentation for more details.
'''

import sys
import types

from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import address_tools


class FunctionAnchoringType(type):
    '''
    Metaclass for working around Python's problems with pickling functions.
    
    Python has a hard time pickling functions that are not at module level,
    because when unpickling them, Python looks for them only on the module
    level.
    
    What we do in this function is create a reference to each of the class's
    functions on the module level. We call this "anchoring." Note that we're
    only anchoring the *functions*, not the *methods*. Methods *can* be pickled
    by Python, but plain functions, like those created by `staticmethod`,
    cannot.
    
    This workaround is hacky, yes, but it seems like the best solution until
    Python learns how to pickle non-module-level functions.
    '''
    def __new__(mcls, name, bases, namespace_dict):
        my_type = super(FunctionAnchoringType, mcls).__new__(mcls,
                                                             name,
                                                             bases,
                                                             namespace_dict)
        
        # We want the type's `vars`, but we want them "getted," and not in a
        # `dict`, so we'll get method objects instead of plain functions.
        my_getted_vars = misc_tools.getted_vars(my_type)
        # Repeat after me: "Getted, not dict."
        
        functions_to_anchor = [value for value in my_getted_vars.itervalues()
                               if isinstance(value, types.FunctionType)]
        for function in functions_to_anchor:
            module_name = function.__module__
            module = sys.modules[module_name]
            function_name = function.__name__
            anchor_address = '.'.join((module_name, function_name))
            
            # Since this metaclass is a hacky solution as it is, let's be
            # careful and ensure no object is already defined by the same name
            # in the module level:
            try:
                already_defined_object = address_tools.resolve(anchor_address)
            except AttributeError:
                # Good, there is no object defined under our anchor address.
                # This is the normal case.
                setattr(module, function_name, function)
            else:
                # Something already exists at the anchor address; let's be
                # careful.
                if already_defined_object is not function:
                    raise Exception("An object `%s.%s` already exists! Can't "
                                    "anchor function." % \
                                    (module_name, function_name))
        return my_type
                    
    