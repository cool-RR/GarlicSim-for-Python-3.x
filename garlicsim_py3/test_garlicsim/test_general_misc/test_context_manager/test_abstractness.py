# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from __future__ import with_statement

import sys

import nose

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType,
                                                    SelfHook)

def test_abstractness():
    
    if sys.version_info[:2] <= (2, 5):
        raise nose.SkipTest("Python 2.5 doesn't enforce abstractness.")
    
    class EmptyContextManager(ContextManager):
        pass

    class EnterlessContextManager(ContextManager):
        def __exit__(self, type_, value, traceback):
            pass
        
    class ExitlessContextManager(ContextManager):
        def __enter__(self):
            pass
        
    def f():
        EmptyContextManager()
    
    def g():
        EnterlessContextManager()
    
    def h():
        ExitlessContextManager()
        
        
    nose.tools.assert_raises(TypeError, f)
    nose.tools.assert_raises(TypeError, g)
    nose.tools.assert_raises(TypeError, h)


def test_can_instantiate_when_defining_manage_context():
    class MyContextManager(ContextManager):
        def manage_context(self):
            yield self
    MyContextManager()


def test_can_instantiate_when_defining_enter_exit():
    class AnotherContextManager(ContextManager):
        def __enter__(self):
            pass
        def __exit__(self, type_, value, traceback):
            pass
    AnotherContextManager()
    