# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines tools for testing.'''

import re

from garlicsim.general_misc.third_party import unittest2

from garlicsim.general_misc import cute_inspect
from garlicsim.general_misc.context_manager import ContextManager
from garlicsim.general_misc.exceptions import CuteException
from garlicsim.general_misc import logic_tools


class Failure(CuteException, AssertionError):
    '''A test has failed.'''


class RaiseAssertor(ContextManager):
    '''
    Asserts that a certain exception was raised in the suite. You may use a
    snippet of text that must appear in the exception message or a regex that
    the exception message must match.
    
    Example:
    
        with RaiseAssertor(ZeroDivisionError, 'modulo by zero'):
            1/0
    
    '''
    
    def __init__(self, exception_type=Exception, text='',
                 assert_exact_type=False):
        '''
        Construct the `RaiseAssertor`.
        
        `exception_type` is an exception type that the exception must be of;
        `text` may be either a snippet of text that must appear in the
        exception's message, or a regex pattern that the exception message must
        match. Specify `assert_exact_type=False` if you want to assert that the
        exception is of the exact `exception_type` specified, and not a
        subclass of it.
        '''
        
        self.exception_type = exception_type
        '''The type of exception that should be raised.'''
        
        self.text = text
        '''The snippet or regex that the exception message must match.'''
        
        self.exception = None
        '''The exception that was caught.'''
        
        self.assert_exact_type = assert_exact_type
        '''
        Flag saying whether we require an exact match to `exception_type`.
        
        If set to `False`, a subclass of `exception_type` will also be
        acceptable.
        '''
        
        
    def manage_context(self):
        '''Manage the `RaiseAssertor'`s context.'''
        try:
            yield self
        except self.exception_type as exception:
            self.exception = exception
            if self.assert_exact_type:
                if self.exception_type is not type(exception):
                    assert issubclass(type(exception), self.exception_type)
                    raise Failure(
                        "The exception `%s` was raised, and it *is* an "
                        "instance of the `%s` we were expecting; but its type "
                        "is not `%s`, it's `%s`, which is a subclass of `%s`, "
                        "but you specified `assert_exact_type=True`, so "
                        "subclasses aren't acceptable." % (repr(exception),
                        self.exception_type.__name__,
                        self.exception_type.__name__, type(exception).__name__,
                        self.exception_type.__name__)
                    )
            if self.text:
                message = exception.args[0]
                if isinstance(self.text, str):
                    if self.text not in message:
                        raise Failure("A `%s` was raised but %s wasn't in its "
                                      "message." % (self.exception_type,
                                      repr(self.text)))
                else:
                    # It's a regex pattern
                    if not self.text.match(message):
                        raise Failure("A `%s` was raised but it didn't match "
                                      "the given regex." % self.exception_type)
        except BaseException as different_exception:
            raise Failure(
                "%s was excpected, but a different exception %s was raised "
                "instead." % (self.exception_type, type(different_exception))
            )
        else:
            raise Failure("%s wasn't raised." % self.exception_type)

                    
def assert_same_signature(*callables):
    '''Assert that all the `callables` have the same function signature.'''
    arg_specs = [cute_inspect.getargspec(callable_) for callable_ in callables]
    if not logic_tools.all_equal(arg_specs, exhaustive=True):
        raise Failure('Not all the callables have the same signature.')
    
    
class _MissingAttribute(object):
    '''Object signifying that an attribute was not found.'''
    # todo: make uninstanciable

    
def assert_polite_wrapper(wrapper, wrapped=None, same_signature=True):
    '''
    Assert that `wrapper` is a polite function wrapper around `wrapped`.
    
    A function wrapper (usually created by a decorator) has a few
    responsibilties; maintain the same name, signature, documentation etc. of
    the original function, and a few others. Here we check that the wrapper did
    all of those things.
    '''
    # todo: in all decorators, should be examining the wrapped function's dict
    # and update the new one with it. can't test for this here though, cause
    # the decorator has the right to change them.
    if wrapped is None:
        wrapped = wrapper.__wrapped__
    if same_signature:
        assert_same_signature(wrapper, wrapped)
    for attribute in ('__module__', '__name__', '__doc__', '__annotations__'):
        assert getattr(wrapper, attribute, _MissingAttribute) == \
               getattr(wrapped, attribute, _MissingAttribute)
    assert wrapper.__wrapped__ == wrapped
    