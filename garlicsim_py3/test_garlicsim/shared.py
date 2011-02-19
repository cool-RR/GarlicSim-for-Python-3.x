# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Tools for testing `garlicsim`.'''


from garlicsim.general_misc import import_tools

import garlicsim
import collections


def verify_simpack_settings(sample_simpack):
    '''
    Verfiy that `sample_simpack` has all the testing flags with valid values.
    '''
    import_tools.normal_import(
        sample_simpack.__name__ + '.x'
    )
    x = sample_simpack.x
    assert isinstance(x.ENDABLE, bool)
    bool(x.VALID)
    assert (x.PROBLEM is None) or \
           issubclass(x.PROBLEM, Exception)
    assert isinstance(x.HISTORY_DEPENDENT, bool)
    assert isinstance(x.N_STEP_FUNCTIONS, int)
    if x.DEFAULT_STEP_FUNCTION is not None:
        assert isinstance(x.DEFAULT_STEP_FUNCTION,
                          collections.Callable)
    if x.DEFAULT_STEP_FUNCTION_TYPE is not None:
        assert issubclass(
            x.DEFAULT_STEP_FUNCTION_TYPE,
            garlicsim.misc.simpack_grokker.step_type.BaseStep
        )
    assert isinstance(x.CONSTANT_CLOCK_INTERVAL, int) or \
           x.CONSTANT_CLOCK_INTERVAL is None
    assert isinstance(x.CRUNCHERS_LIST, list)
    for cruncher_type in x.CRUNCHERS_LIST:
        assert issubclass(cruncher_type,
                          garlicsim.asynchronous_crunching.BaseCruncher)
        
    # Making sure there aren't any extraneous settings, so we'll know we
    # checked everything:
    settings_names = [name for name in dir(x) if name.isupper()]
    assert len(settings_names) == 9
