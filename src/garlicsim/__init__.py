# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
GarlicSim is a platform for writing, running and analyzing simulations. It can
handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.

Visit http://garlicsim.com for more info.

This package, called `garlicsim`, is the business logic. It is copyrighted to
Ram Rachum, 2009, and is distributed under the LGPL v2.1 License. The license
is included with this package as the file `lgpl2.1_license.txt`.

This licensing does not apply to `garlicsim_wx`, which is the associated GUI
package.

todo: maybe do the "with tree_lock" in Project instead of in CrunchingManager?

todo: organize all namespaces

todo: decide policies regaring import (whether from, as, or regular)
"""

from asynchronous_crunching import Project
from synchronous_crunching import simulate, list_simulate

__all__ = ["Project", "simulate", "list_simulate"]