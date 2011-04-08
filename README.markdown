`# Brief Video Introduction #

[![](http://garlicsim.org/images/video_thumbnail.jpg)](http://garlicsim.org/brief_introduction.html)


# Documentation #

[Main documentation site](http://docs.garlicsim.org)

[Installation](http://docs.garlicsim.org/intro/installation/developers/python-3.x.html)

[FAQ](http://docs.garlicsim.org/misc/faq.html)

[Mailing lists](http://docs.garlicsim.org/misc/mailing-lists.html)


# What is GarlicSim? #

GarlicSim is an ambitious open-source project in the field of scientific computing, specifically computer simulations. It attempts to redefine the way that people think about computer simulations, making a new standard for how simulations are created and used.

GarlicSim is a platform for writing, running and analyzing simulations. It is general enough to handle any kind of simulation: Physics, game theory, epidemic spread, electronics, etc.

When you're writing a simulation, about 90% of the code you write is boilerplate; code that isn't directly related to the phenomenon you're simulating, but is necessary for your simulation to work. The aim of GarlicSim is to write that 90% of the code once and for all, and to do it well, so you could concentrate on the important 10%.

GarlicSim defines a new format for simulations. It's called a **simulation package**, and often abbreviated as **simpack**. For example, say you are interested in simulating the interaction of hurricane storms. It is up to you to write a simpack for this type of simulation. The simpack is simply a Python package which defines a few special functions according to the GarlicSim simpack API, the most important function being the **step function**.

The beauty is that since so many simulation types can fit into this mold of a simpack, the tools that GarlicSim provides can be used across all of these different domains. Once you plug your own simpack into GarlicSim, you're ready to roll. All the tools that GarlicSim provides will work with your simulation.

Additionally, GarlicSim will eventually be shipped with a standard library of simpacks for common simulations, that the user may find useful to use as-is, or with his own modifications.

For a more thorough introduction to how GarlicSim works, check out the [documentation](http://docs.garlicsim.org).

GarlicSim itself is written in pure Python. The speed of simulations is mostly dependent on the simpack's performance - So it is possible to use C code in a simpack to make things faster.

GarlicSim is distributed under the **LGPL2.1 license**, and is copyright 2009-2010 Ram Rachum. 


# Mailing lists #

All general discussion happens at **[the GarlicSim Google Group](https://groups.google.com/forum/#!forum/garlicsim)**. If you need help with GarlicSim, you're welcome to post your question and we'll try to help you.

The development mailing list is **[GarlicSim-dev](https://groups.google.com/forum/#!forum/garlicsim-dev)**. This is where we discuss the development of GarlicSim itself.


# Looking for a gui? #

This is the fork of GarlicSim for Python version 3.x. If you are interested in a gui for GarlicSim, check out the [main GarlicSim fork](http://github.com/cool-RR/GarlicSim). (There is no gui on 3.x because the underlying wxPython does not support it yet.)


# Python versions #

This is a fork of GarlicSim which supports Python 3.x.

The [main GarlicSim fork](http://github.com/cool-RR/GarlicSim) supports Python versions 2.5 and up.


# Current state #

GarlicSim is at version 0.6.3, which is an alpha release. At this experimental stage of the project, backward compatibility will _not_ be maintained. However, I will be available to assist in issues related to backward compatibility.
