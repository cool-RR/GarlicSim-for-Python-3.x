# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Module for testing the abstract methods of `ContextManager`.'''

import sys

import nose

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType,
                                                    SelfHook)

def test_abstractness():
    '''
    A non-abstract-overriding `ContextManager` subclass can't be instantiated.
    '''
    
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
    '''
    A `manage_context`-defining `ContextManager` subclass can be instantiated.
    '''
    class MyContextManager(ContextManager):
        def manage_context(self):
            yield self
    MyContextManager()


def test_can_instantiate_when_defining_enter_exit():
    '''
    An enter/exit -defining `ContextManager` subclass can be instantiated.
    '''
    class AnotherContextManager(ContextManager):
        def __enter__(self):
            pass
        def __exit__(self, type_, value, traceback):
            pass
    AnotherContextManager()
    