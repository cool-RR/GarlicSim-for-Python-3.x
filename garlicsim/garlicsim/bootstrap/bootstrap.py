# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A bootstrap module for garlicsim.

It checks all prerequisites are installed.
'''

import sys


if sys.version_info[0] <= 2:
    raise Exception('This package requires Python 3.x. For Python 2.5+, use '
                    '`garlicsim`, which you can find on PyPI.')


def __check_prerequisites():
    '''
    Check that all modules required for `garlicsim` are installed.
    
    Returns a list of some imported modules: A reference to this list should be
    kept alive so to prevent the imported modules from being garbage-collected,
    which would cause Python to load them twice, which would needlessly
    increase startup time.
    '''
    
    modules = []
    
    class MissingModule(Exception):
        '''A required module is not found.'''
    
    def check_pkg_resources():
        try:
            import pkg_resources
            return [pkg_resources]
        except ImportError:
            raise MissingModule("`pkg_resources` is required, but it's not "
                                "currently installed on your system. It comes "
                                "with either `setuptools` or `distribute`, so "
                                "please find either one of these on the "
                                "internet and install it, then try again.")
    
    checkers = [check_pkg_resources]
    
    for checker in checkers:
        modules += checker()
    
    return modules


def __check_problematic_psyco_version():
    if 'psyco' in sys.modules:
        psyco = sys.modules['psyco']
        if psyco.version_info[0] >= 2:
            import warnings
            warnings.warn("You seem to have Psyco version 2 (or newer) "
                          "installed. It might conflict with `garlicsim`, so "
                          "you may want to avoid using it. Psyco version 1.6 "
                          "is fine and recommended.")

__modules_list = __check_prerequisites()

__check_problematic_psyco_version()

