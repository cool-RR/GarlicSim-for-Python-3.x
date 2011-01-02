# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Test the `garlicsim.general_misc.context_manager` module.'''

from __future__ import with_statement

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType,
                                                    SelfHook)

flag = None
exception_type_caught = None


def test_generator():
    '''Test a context manager made from a generator.'''
    @ContextManagerType
    def MyContextManager(value):
        global flag, exception_type_caught
        former_value = flag
        flag = value
        try:
            yield
        finally:
            flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=False)
    

def test_error_catching_generator():
    '''Test an error-catching context manager made from a generator.'''
    
    @ContextManagerType
    def MyContextManager(value):
        global flag, exception_type_caught
        former_value = flag
        flag = value
        try:
            yield
        except Exception, exception:
            exception_type_caught = type(exception)
        finally:
            flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=True)


def test_self_returning_generator():
    '''Test a self-returning context manager made from a generator.'''
    @ContextManagerType
    def MyContextManager(value):
        global flag, exception_type_caught
        former_value = flag
        flag = value
        try:
            yield SelfHook
        finally:
            flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=False)
    

def test_self_returning_error_catching_generator():
    '''
    Test a self-returning error-catching context manager made from a generator.
    '''
    @ContextManagerType
    def MyContextManager(value):
        global flag, exception_type_caught
        former_value = flag
        flag = value
        try:
            yield SelfHook
        except Exception, exception:
            exception_type_caught = type(exception)
        finally:
            flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)
    
    
def test_manage_context():
    '''Test a context manager that uses a `manage_context` method.'''
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag, exception_type_caught
            former_value = flag
            flag = self.value
            try:
                yield
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=False)
        
    
def test_error_catching_manage_context():
    '''Test an error-catching `manage_context`-powered context manager.'''
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag, exception_type_caught
            former_value = flag
            flag = self.value
            try:
                yield
            except Exception, exception:
                exception_type_caught = type(exception)
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=True)
    
    
def test_self_returning_manage_context():
    '''Test a self-returning `manage_context`-powered context manager.'''
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag
            former_value = flag
            flag = self.value
            try:
                yield self
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=False)
    
    
def test_self_returning_error_catching_manage_context():
    '''
    Test a self-returning error-catching `manage_context` context manager.
    '''
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag, exception_type_caught
            former_value = flag
            flag = self.value
            try:
                yield self
            except Exception, exception:
                exception_type_caught = type(exception)
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)

    
def test_manage_context_overriding_generator():
    '''
    Test a `manage_context` context manager overriding one made from generator.
    '''
    @ContextManagerType
    def MyBaseContextManager(value):
        raise Exception('This code is supposed to be overridden.')
        yield
    
    class MyContextManager(MyBaseContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag, exception_type_caught
            former_value = flag
            flag = self.value
            try:
                yield self
            except Exception, exception:
                exception_type_caught = type(exception)
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)
    
    
def test_manage_context_overriding_manage_context():
    '''
    Test a `manage_context`-powered context manager overriding another one.
    '''    
    class MyBaseContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            raise Exception('This code is supposed to be overridden.')
            yield
            
    class MyContextManager(MyBaseContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag, exception_type_caught
            former_value = flag
            flag = self.value
            try:
                yield self
            except Exception, exception:
                exception_type_caught = type(exception)
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)
    
    
def test_manage_context_overriding_enter_exit():
    '''
    Test `manage_context` context manager overriding one made from enter/exit.
    '''
    
    class MyBaseContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
            self._former_values = []
        
        def __enter__(self):
            raise Exception('This code is supposed to be overridden.')
            
        def __exit__(self, type_=None, value=None, traceback=None):
            raise Exception('This code is supposed to be overridden.')

            
    class MyContextManager(MyBaseContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag, exception_type_caught
            former_value = flag
            flag = self.value
            try:
                yield self
            except Exception, exception:
                exception_type_caught = type(exception)
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)
    
    
def test_enter_exit():
    '''Test an enter/exit context manager.'''
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
            self._former_values = []
        
        def __enter__(self):
            global flag
            self._former_values.append(flag)
            flag = self.value
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag
            flag = self._former_values.pop()
    
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=False)

    
def test_error_catching_enter_exit():
    '''Test an error-catching enter/exit context manager.'''
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
            self._former_values = []
        
        def __enter__(self):
            global flag
            self._former_values.append(flag)
            flag = self.value
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag, exception_type_caught
            flag = self._former_values.pop()
            if type_:
                exception_type_caught = type_
                return True
    
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=True)

    
def test_self_returning_enter_exit():
    '''Test a self-returning enter/exit context manager.'''
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
            self._former_values = []
        
        def __enter__(self):
            global flag
            self._former_values.append(flag)
            flag = self.value
            return self
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag
            flag = self._former_values.pop()
    
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=False)

    
def test_error_catching_self_returning_enter_exit():
    '''Test an error-catching self-returning enter/exit context manager.'''
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
            self._former_values = []
        
        def __enter__(self):
            global flag
            self._former_values.append(flag)
            flag = self.value
            return self
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag, exception_type_caught
            flag = self._former_values.pop()
            if type_:
                exception_type_caught = type_
                return True
    
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)
    
    
def test_enter_exit_overriding_generator():
    '''
    Test an enter/exit context manager overriding one made from generator.
    '''
    @ContextManagerType
    def MyBaseContextManager(value):
        raise Exception('This code is supposed to be overridden.')
        yield
        
    class MyContextManager(MyBaseContextManager):
        def __init__(self, value):
            self.value = value
            self._former_values = []
        
        def __enter__(self):
            global flag
            self._former_values.append(flag)
            flag = self.value
            return self
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag, exception_type_caught
            flag = self._former_values.pop()
            if type_:
                exception_type_caught = type_
                return True
    
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)


def test_enter_exit_overriding_manage_context():
    '''
    Test enter/exit context manager overriding one made from `manage_context`.
    '''
    class MyBaseContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            raise Exception('This code is supposed to be overridden.')
            yield
    
    class MyContextManager(MyBaseContextManager):
        def __init__(self, value):
            self.value = value
            self._former_values = []
        
        def __enter__(self):
            global flag
            self._former_values.append(flag)
            flag = self.value
            return self
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag, exception_type_caught
            flag = self._former_values.pop()
            if type_:
                exception_type_caught = type_
                return True
    
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)


def test_enter_exit_overriding_enter_exit():
    '''Test an enter/exit context manager overriding another one.'''
    
    class MyBaseContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
            self._former_values = []
        
        def __enter__(self):
            raise Exception('This code is supposed to be overridden.')
            
        def __exit__(self, type_=None, value=None, traceback=None):
            raise Exception('This code is supposed to be overridden.')
        
    
    class MyContextManager(MyBaseContextManager):
        def __init__(self, value):
            self.value = value
            self._former_values = []
        
        def __enter__(self):
            global flag
            self._former_values.append(flag)
            flag = self.value
            return self
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag, exception_type_caught
            flag = self._former_values.pop()
            if type_:
                exception_type_caught = type_
                return True
    
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)


def check_context_manager_type(context_manager_type,
                               self_returning,
                               error_catching):
    '''
    Run checks on a context manager.
    
    `self_returning` is a flag saying whether the context manager's `__enter__`
    method returns itself. (For the `as` keyword after `with`.)
    
    `error_catching` says whether the context manager catches exceptions it
    gets and updates the `exception_type_caught` global.
    '''
    
    global flag, exception_type_caught
    
    assert flag is None
    assert exception_type_caught is None
    
    with context_manager_type(7) as return_value:
        assert flag == 7
        if self_returning:
            assert isinstance(return_value, context_manager_type)
        else: # self_returning is False
            assert return_value is None
        
    assert flag is None
    assert exception_type_caught is None
    
    my_context_manager = context_manager_type(1.1)
    assert isinstance(my_context_manager, context_manager_type)
    with my_context_manager as return_value:
        assert flag == 1.1
        if self_returning:
            assert return_value is my_context_manager
        else: # self_returning is False
            assert return_value is None
    
    assert flag is None
    assert exception_type_caught is None

    @context_manager_type('meow')
    def f():
        assert flag == 'meow'
        
    f()
    assert flag is None
    assert exception_type_caught is None
    
    my_context_manager = context_manager_type(123)
    assert flag is None
    with my_context_manager:
        assert flag == 123
        with my_context_manager:
            assert flag == 123
            with my_context_manager:
                assert flag == 123
                with my_context_manager:
                    assert flag == 123
                    with my_context_manager:
                        assert flag == 123
                    assert flag == 123
                assert flag == 123
            assert flag == 123
        assert flag == 123
    assert flag is None
    
    with context_manager_type(1) as return_value_1:
        assert flag == 1
        with context_manager_type(2) as return_value_2:
            assert flag == 2
            with return_value_1 or context_manager_type(1):
                assert flag == 1
            assert flag == 2
        assert flag == 1
    assert flag is None
    
    # Now while raising exceptions:
    
    try:
        
        with context_manager_type(7) as return_value:
            assert flag == 7
            if self_returning:
                assert isinstance(return_value, context_manager_type)
            else: # self_returning is False
                assert return_value is None
            raise TypeError('ooga booga')
        
    except Exception, exception:
        assert not error_catching
        assert type(exception) is TypeError
        
    else:
        assert error_catching
        assert exception_type_caught is TypeError
        exception_type_caught = None
        
    assert flag is None
    
    my_context_manager = context_manager_type(1.1)
    assert isinstance(my_context_manager, context_manager_type) 
    try:
        with my_context_manager as return_value:
            assert flag == 1.1
            if self_returning:
                assert return_value is my_context_manager
            else: # self_returning is False
                assert return_value is None
            {}[3]
    
    except Exception, exception:
        assert not error_catching
        assert exception_type_caught is None
        assert type(exception) is KeyError
        
    else:
        assert error_catching
        assert exception_type_caught is KeyError
        exception_type_caught = None
        
    
    assert flag is None
    assert exception_type_caught is None

    @context_manager_type('meow')
    def f():
        assert flag == 'meow'
        1/0
        
    
    try:
        f()
    except Exception, exception:
        assert not error_catching
        assert exception_type_caught is None
        assert type(exception) is ZeroDivisionError
        
    else:
        assert error_catching
        assert exception_type_caught is ZeroDivisionError
        exception_type_caught = None
        
    assert flag is None
    
    exception_type_caught = None
    
    
    my_context_manager = context_manager_type(123)
    assert flag is None
    try:
        with my_context_manager:
            assert flag == 123
            with my_context_manager:
                assert flag == 123
                with my_context_manager:
                    assert flag == 123
                    with my_context_manager:
                        assert flag == 123
                        with my_context_manager:
                            assert flag == 123
                            raise StopIteration
                        assert flag == 123
                    assert flag == 123
                assert flag == 123
            assert flag == 123
            
    except Exception, exception:
        assert not error_catching
        assert exception_type_caught is None
        assert type(exception) is StopIteration
        
    else:
        assert error_catching
        assert exception_type_caught is StopIteration
        exception_type_caught = None
        
    assert flag is None

    
    try:
        with context_manager_type(1) as return_value_1:
            assert flag == 1
            with context_manager_type(2) as return_value_2:
                assert flag == 2
                with return_value_1 or context_manager_type(1):
                    assert flag == 1
                    raise NotImplementedError
                assert flag == 2
            assert flag == 1
            
    except Exception, exception:
        assert not error_catching
        assert exception_type_caught is None
        assert type(exception) is NotImplementedError
        
    else:
        assert error_catching
        assert exception_type_caught is NotImplementedError
        exception_type_caught = None
        
    assert flag is None
    