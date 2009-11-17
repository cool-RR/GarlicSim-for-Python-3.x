# Installation #

[**Binary installers** are available here.](http://github.com/cool-RR/GarlicSim-for-Python-3.1/downloads)

For a source installation: Download the repo, then run `setup.py install` in the `garlicsim` folder.

Requirements:

* [Python 3.1](http://www.python.org/download/releases/3.1.1/) (Scroll down to the "Python versions" section for other versions.)
* [Distribute](http://pypi.python.org/pypi/distribute), version 0.6.8 or later

Recommended, but not mandatory:

* on Windows only: [Python for Windows Extensions](http://sourceforge.net/projects/pywin32/)

# What is GarlicSim? #

GarlicSim is an ambitious open-source project in the field of scientific computing, specifically computer simulations. It attempts to redefine the way that people think about computer simulations, making a new standard for how simulations are created and used.

GarlicSim is a platform for writing, running and analyzing simulations. It is general enough to handle any kind of simulation: Physics, game theory, epidemic spread, electronics, etc.

When you're writing a simulation, about 90% of the code you write is boilerplate; Code that isn't directly related to the phenomenon you're simulating, but is necessary for your simulation to work. The aim of GarlicSim is to write that 90% of the code once and for all, and to do it well, so you could concentrate on the important 10%.

GarlicSim defines a new format for simulations. It's called a **simulation package**, and often abbreviated as **simpack**. For example, say you are interested in simulating the interaction of hurricane storms. It is up to you to write a simpack for this type of simulation. The simpack is simply a Python package which defines a few special functions according to the GarlicSim simpack API, the most important function being the **step function**.

The beauty is that since so many simulation types can fit into this mold of a simpack, the tools that GarlicSim provides can be used across all of these different domains. Once you plug your own simpack into GarlicSim, you're ready to roll. All the tools that GarlicSim provides will work with your simulation.

Additionally, GarlicSim will eventually be shipped with a standard library of simpacks for common simulations, that the user may find useful to use as-is, or with his own modifications.

For a more thorough introduction to how GarlicSim works, check out the ** [Introduction to GarlicSim](http://dl.getdropbox.com/u/1927707/Introduction%20to%20GarlicSim.doc) ** - Though not yet complete, it goes deep into the principles of GarlicSim and how to work with it.

GarlicSim itself is written in pure Python. The speed of simulations is mostly dependent on the simpack's performance - So it is possible to use C code in a simpack to make things faster.

The `garlicsim` package is distributed under the **LGPL2.1 license**, and is copyright 2009 Ram Rachum. 

# Community and Support #

If you need help with anything related to GarlicSim, mail me at [cool-rr@cool-rr.com](mailto:cool-rr@cool-rr.com). Soon there will be an official collaboration medium for GarlicSim.

# Looking for a gui? #

This is the fork of GarlicSim for Python version 3.1. If you are interested in a gui for GarlicSim, check out the forks for the 2.x versions below. (There is no gui on 3.1 because the underlying wxPython does not support it yet.)

# Python versions #

GarlicSim has official support for 4 different versions of Python. For each of these versions there is a separate fork. The fork for Python 2.6 is the main fork, on which most development is done. Some of the other forks have slightly reduced functionality, described here:

[GarlicSim for Python 2.4](http://github.com/cool-RR/GarlicSim-for-Python-2.4) - Does not support multiprocessing, only multithreading.

[GarlicSim for Python 2.5](http://github.com/cool-RR/GarlicSim-for-Python-2.5) - Requires [backported multiprocessing package](http://code.google.com/p/python-multiprocessing/) to be installed in order to use multiprocessing.

[GarlicSim for Python 2.6](http://github.com/cool-RR/GarlicSim-for-Python-2.6) - Main fork, contains all the functionality.

[GarlicSim for Python 3.1](http://github.com/cool-RR/GarlicSim-for-Python-3.1) - Does not contain gui package, since wxPython doesn't yet support Python 3.x.

# Current state #

Garlicsim is at version 0.1, which is an alpha release. It is still very experimental, and there are probably many bugs. If you run into any trouble, [drop me a mail](mailto:cool-rr@cool-rr.com).

At this experimental stage of the project, backward compatibility will _not_ be maintained. However, I will be available to assist in issues related to backward compatibility.

# Frequently asked questions: #

## What kind of simulations will I be able to do with GarlicSim? ##

People often ask this; probably because they do not fully believe it when they read GarlicSim's description saying that it can handle any kind of simulation. Well, it can. It is very general.

Then people ask, if it is so general, how is it useful? There are two answers to that:

1.  It is very useful. There are many many features that are common to all kinds of simulations, and which you really don't want to spend time writing. A few examples of such features: Saving the simulation to file. Browsing the timeline of a simulation like a movie clip while it is still crunching in the background. The option to make manual changes to the simulation world, observe their effects on how the simulation unfolds, and then to be able to revert to the timeline in which the changes were not applied. Changing the arguments to the step function on the fly, etc.

2.  If you are interested in only a specific subset of simulations -- say, simulations of solid bodies in Physics -- Then it will be the wisest to write a framework for that within the framework of GarlicSim. Indeed, part of the work on GarlicSim will include writing these kind of sub-frameworks for the common categories of simulations (e.g., a framework for physics, a framework for game theory, etcetera.)

## Does GarlicSim give mathematical tools for simulations? ##

**No.** GarlicSim doesn't contain any mathematical tools, or any algorithms to be used in simulations. These things are related to the **content** of the simulation, which is none of GarlicSim's business. GarlicSim handles the organization, or "bureaucracy" of the simulation, so you can concentrate on the content. If you need mathematical tools for your simulation there are many Python projects that provide them, and you may use them in your simpack that you run with GarlicSim.

