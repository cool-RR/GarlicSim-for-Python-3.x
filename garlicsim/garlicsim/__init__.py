# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
GarlicSim is a platform for writing, running and analyzing simulations. It can
handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.

Visit http://garlicsim.org for more info.

This package, called `garlicsim`, is the business logic. It is copyrighted to
Ram Rachum, 2009, and is distributed under the LGPL v2.1 License. The license
is included with this package as the file `lgpl2.1_license.txt`.

This fork of garlicsim is intended for Python 3.1.
'''


import garlicsim.bootstrap
import garlicsim.general_misc
import garlicsim.misc
from garlicsim.synchronous_crunching import simulate, list_simulate
from garlicsim.asynchronous_crunching import Project

__all__ = ["Project", "simulate", "list_simulate"]

__version__ = '0.2'

