# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ContextManager` class.

See its documentation for more information.
'''


import sys
import types
import abc

from garlicsim.general_misc import decorator_tools

from .context_manager_type import ContextManagerType
from .self_hook import SelfHook


class ContextManager(object, metaclass=ContextManagerType):
    '''
    Allows running preparation code before a given suite and cleanup after.
    
    To make a context manager, use `ContextManager` as a base class and either
    (a) define `__enter__` and `__exit__` methods or (b) define a
    `manage_context` method that returns a generator. An alternative way to
    create a context manager is to define a generator function and decorate it
    with `ContextManagerType`.
    
    In any case, the resulting context manager could be called either with the
    `with` keyword or by using it as a decorator to a function.
                
    For more details, see documentation of the containing module,
    `garlicsim.general_misc.context_manager`.
    '''
    
    def __call__(self, function):
        '''Decorate `function` to use this context manager when it's called.'''
        def inner(function_, *args, **kwargs):
            with self:
                return function_(*args, **kwargs)
        return decorator_tools.decorator(inner, function)
    
    
    @abc.abstractmethod
    def __enter__(self):
        '''Prepare for suite execution.'''

    
    @abc.abstractmethod
    def __exit__(self, type_=None, value=None, traceback=None):
        '''Cleanup after suite execution.'''
    

    def __init_lone_manage_context(self, *args, **kwargs):
        '''
        Initialize a `ContextManager` made from a lone generator function.
        '''
        self._ContextManager__args = args
        self._ContextManager__kwargs = kwargs
        self._ContextManager__generators = []
    
    
    def __enter_using_manage_context(self):
        '''
        Prepare for suite execution.
        
        This is used as `__enter__` for context managers that use a
        `manage_context` function.
        '''
        if not hasattr(self, '_ContextManager__generators'):
            self._ContextManager__generators = []
        
        new_generator = self.manage_context(
            *getattr(self, '_ContextManager__args', ()),
            **getattr(self, '_ContextManager__kwargs', {})
        )
        assert isinstance(new_generator, types.GeneratorType)
        self._ContextManager__generators.append(new_generator)
        
        
        try:
            generator_return_value = next(new_generator)
            return self if (generator_return_value is SelfHook) else \
                   generator_return_value
        
        except StopIteration:
            raise RuntimeError("The generator didn't yield even one time; it "
                               "must yield one time exactly.")
    
        
    def __exit_using_manage_context(self, type_, value, traceback):
        '''
        Cleanup after suite execution.
        
        This is used as `__exit__` for context managers that use a
        `manage_context` function.
        '''
        generator = self._ContextManager__generators.pop()
        assert isinstance(generator, types.GeneratorType)
        
        if type_ is None:
            try:
                next(generator)
            except StopIteration:
                return
            else:
                raise RuntimeError(
                    "The generator didn't stop after the yield; possibly you "
                    "have more than one `yield` in the generator function? "
                    "The generator function must yield exactly one time.")
        else:
            if value is None:
                # Need to force instantiation so we can reliably
                # tell if we get the same exception back
                value = type_()
            try:
                generator.throw(type_, value, traceback)
            except StopIteration as exc:
                # Suppress the exception *unless* it's the same exception that
                # was passed to throw().  This prevents a StopIteration
                # raised inside the "with" statement from being suppressed
                return exc is not value
            except:
                # only re-raise if it's *not* the exception that was
                # passed to throw(), because __exit__() must not raise
                # an exception unless __exit__() itself failed.  But throw()
                # has to raise the exception to signal propagation, so this
                # fixes the impedance mismatch between the throw() protocol
                # and the __exit__() protocol.
                #
                if sys.exc_info()[1] is not value:
                    raise
            else:
                raise RuntimeError(
                    "The generator didn't stop after calling its `.throw()`; "
                    "Possibly you have more than one `yield` in the generator "
                    "function? The generator function must yield exactly one "
                    "time."
                )