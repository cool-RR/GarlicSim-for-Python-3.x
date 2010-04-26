# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the StepCopy class.

See its documentation for more information.
'''

from garlicsim_py3.general_misc.copy_mode import CopyMode
from garlicsim_py3.misc.persistent import DontCopyPersistent

class StepCopy(DontCopyPersistent, CopyMode):
    '''
    A copy mode used in step function to generate the next state.
    
    A popular design pattern in step functions is to deepcopy the old state,
    modify it, and then return it as the new state. When this is done, you
    should pass StepCopy() into the deepcopy function as a memo. This assures
    that certain objects get copied in the right way for this context.
    '''