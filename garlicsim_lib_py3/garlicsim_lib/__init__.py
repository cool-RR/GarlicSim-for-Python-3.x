# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''A collection of simulation packages to be used with garlicsim.'''

import sys

__version__ = '0.5'


if sys.version_info[0] <= 2:
    raise Exception('''This package requires Python 3.x. For Python 2.5+, use \
`garlicsim_lib`, which you can find on PyPI.''')