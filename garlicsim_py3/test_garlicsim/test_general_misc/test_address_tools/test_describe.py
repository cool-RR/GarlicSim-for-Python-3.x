# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.address_tools.describe`.'''

import nose

from garlicsim.general_misc import import_tools
from garlicsim.general_misc.temp_value_setters import TempValueSetter

import garlicsim
from garlicsim.general_misc.address_tools import (describe,
                                                  resolve)


prefix = __name__ + '.'



def test_locally_defined_class():
    
    ###########################################################################
    # Testing for locally defined class:
    
    
    if garlicsim.__version_info__ <= (0, 6, 3):
        raise nose.SkipTest("This test doesn't pass in `garlicsim` version "
                            "0.6.3 and below, because `describe` doesn't "
                            "support nested classes yet.")
    
    result = describe(A.B)
    assert result == prefix + 'A.B'
    assert resolve(result) is A.B
    
    result = describe(A.C.D.deeper_method)
    assert result == prefix + 'A.C.D.deeper_method'
    assert resolve(result) == A.C.D.deeper_method
    
    result = describe(A.C.D.deeper_method, root=A.C)
    assert result == 'C.D.deeper_method'
    assert resolve(result, root=A.C) == A.C.D.deeper_method
    
    result = describe(A.C.D.deeper_method, root='A.C.D')
    assert result == 'D.deeper_method'
    assert resolve(result, root='A.C.D') == A.C.D.deeper_method
    
    
def test_stdlib():
    '''Test `describe` for various stdlib modules.'''
    
    import email.encoders
    result = describe(email.encoders)
    assert result == 'email.encoders'
    assert resolve(result) is email.encoders
    
    result = describe(email.encoders, root=email.encoders)
    assert result == 'encoders'
    assert resolve(result, root=email.encoders) is email.encoders
    
    result = describe(email.encoders, namespace=email)
    assert result == 'encoders'
    assert resolve(result, namespace=email) is email.encoders
    
    result = describe(email.encoders, root=email.encoders, namespace=email)
    assert result == 'encoders'
    assert resolve(result, root=email.encoders, namespace=email) is \
           email.encoders
    
    
def test_garlicsim():
    '''Test `describe` for various `garlicsim` modules.'''
    
    import garlicsim
    result = describe(garlicsim.data_structures.state.State)
    assert result == 'garlicsim.data_structures.state.State'
    assert resolve(result) is garlicsim.data_structures.state.State
    
    result = describe(garlicsim.data_structures.state.State, shorten=True)
    assert result == 'garlicsim.data_structures.State'
    assert resolve(result) is garlicsim.data_structures.state.State
    
    result = describe(garlicsim.Project, shorten=True)
    assert result == 'garlicsim.Project'
    assert resolve(result) is garlicsim.Project
    
    # When a root or namespace is given, it's top priority to use it, even if
    # it prevents shorterning and results in an overall longer address:
    result = describe(garlicsim.Project, shorten=True,
                      root=garlicsim.asynchronous_crunching)
    assert result == 'asynchronous_crunching.Project'
    assert resolve(result, root=garlicsim.asynchronous_crunching) is \
           garlicsim.Project
    
    result = describe(garlicsim.Project, shorten=True,
                      namespace=garlicsim)
    assert result == 'Project'
    assert resolve(result, namespace=garlicsim) is garlicsim.Project
    
    result = describe(garlicsim.Project, shorten=True,
                         namespace=garlicsim.__dict__)
    assert result == 'Project'
    assert resolve(result, namespace=garlicsim.__dict__) is \
           garlicsim.Project
    
    result = describe(garlicsim.Project, shorten=True,
                      namespace='garlicsim')
    assert result == 'Project'
    assert resolve(result, namespace='garlicsim') is garlicsim.Project
    
    result = describe(garlicsim.Project, shorten=True,
                      namespace='garlicsim.__dict__')
    assert result == 'Project'
    assert resolve(result, namespace='garlicsim.__dict__') is \
           garlicsim.Project
    
    result = describe(garlicsim.data_structures.state.State, root=garlicsim)
    assert result == 'garlicsim.data_structures.state.State'
    assert resolve(result, root=garlicsim) is \
           garlicsim.data_structures.state.State
    

def test_garlicsim_method():
    
    raise nose.SkipTest("Can't handle methods yet.")

    import garlicsim_lib.simpacks.life
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step)
    assert result == 'garlicsim_lib.simpacks.life.state.State.step'
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step,
                      shorten=True)
    assert result == 'garlicsim_lib.simpacks.life.State.step'
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step,
                      root=garlicsim_lib.simpacks.life)
    assert result == 'life.state.State.step'
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step,
                      namespace=garlicsim_lib.simpacks)
    assert result == 'life.state.State.step'
    
    result = describe(garlicsim_lib.simpacks.life.state.State.step,
                      root=garlicsim_lib.simpacks.life, shorten=True)
    assert result == 'life.State.step'
    
    
def test_local_modules():
    '''Test `describe` on local, relatively-imported modules.'''
    import garlicsim
    
    from .sample_module_tree import w
    
    z = resolve('w.x.y.z', root=w)

    result = describe(z, root=w)
    assert result == 'w.x.y.z'
    
    result = describe(z, shorten=True, root=w)
    assert result == 'w.y.z'
    
    result = describe(z, shorten=True, root=w)
    assert result == 'w.y.z'
    
    result = describe(z, shorten=True, root=w, namespace='email')
    assert result == 'w.y.z'
    
    result = describe(z, shorten=True, root=garlicsim, namespace=w)
    assert result == 'y.z'
    
    result = describe(z, shorten=True, root=w.x)
    assert result == 'x.y.z'
    
    
def test_ignore_confusing_namespace():
    '''Test that `describe` doesn't use a confusing namespace item.'''
    import email.encoders
    import marshal
    
    result = describe(
        email,
        shorten=True,
        namespace={'e': email}
    )
    assert result == 'email' # Not shortening to 'e', that would be confusing.
    
    result = describe(
        email.encoders,
        namespace={'e': email, 'email': email}
    )
    assert result == 'email.encoders'
    
    result = describe(
        email.encoders,
        root=marshal,
        namespace={'e': email, 'email': email}
    )
    assert result == 'email.encoders'
    
    
    
def test_address_in_expression():
    '''Test `describe` works for an address inside an expression.'''
    
    import email.encoders
    import marshal
    
    assert describe([object, email.encoders, marshal]) == \
           '[object, email.encoders, marshal]'
    
    assert describe([email.encoders, 7, (1, 3), marshal]) == \
           '[email.encoders, 7, (1, 3), marshal]'
    

def test_multiprocessing_lock():
    '''Test `describe` works for `multiprocessing.Lock()`.'''
    if not import_tools.exists('multiprocessing'):
        raise nose.SkipTest('`multiprocessing` not installed')
    import multiprocessing
    lock = multiprocessing.Lock()
    describe(lock)
    
    
def test_bad_module_name():
    '''
    Test `describe` works for objects with bad `__module__` attribute.
    
    The `__module__` attribute usually says where an object can be reached. But
    in some cases, like when working in a shell, you can't really access the
    objects from that non-existant module. So `describe` must not fail for
    these cases.
    '''
    
    import email

    non_sensical_module_name = '__whoop_dee_doo___rrrar'
    
    my_locals = locals().copy()
    my_locals['__name__'] = non_sensical_module_name
    
    exec('def f(): pass', my_locals)
    exec(('class A(object):\n'
          '    def m(self): pass\n'), my_locals)
    
    f, A = my_locals['f'], my_locals['A']
    
    assert describe(f) == \
        '.'.join((non_sensical_module_name, 'f'))
    assert describe(f, shorten=True, root=email, namespace={}) == \
        '.'.join((non_sensical_module_name, 'f'))
    
    assert describe(A) == \
        '.'.join((non_sensical_module_name, 'A'))
    assert describe(A, shorten=True, root=email, namespace={}) == \
        '.'.join((non_sensical_module_name, 'A'))

    
def test_bad_module_name():
    '''
    Test `describe` works for methods with bad `__module__` attribute.
    
    The `__module__` attribute usually says where an object can be reached. But
    in some cases, like when working in a shell, you can't really access the
    objects from that non-existant module. So `describe` must not fail for
    these cases.
    '''
    
    raise nose.SkipTest("Can't handle methods yet.")
    
    non_sensical_module_name = '__whoop_dee_doo___rrrar'
    
    my_locals = locals().copy()
    my_locals['__name__'] = non_sensical_module_name
    
    exec('def f(): pass', my_locals)
    exec(('class A(object):\n'
          '    def m(self): pass'), my_locals)
    
    assert describe(A.m) == \
        '.'.join((non_sensical_module_name, 'A.m'))
    assert describe(A.m, shorten=True, root=email, namespace={}) == \
        '.'.join((non_sensical_module_name, 'A.m'))
    

def test_function_in_something():
    '''Test `describe` doesn't fail when describing `{1: sum}`.'''
    if garlicsim.__version_info__ <= (0, 6, 3):
        raise nose.SkipTest("This test doesn't pass in `garlicsim` version "
                            "0.6.3 and below.")
    assert describe({1: sum}) == '{1: sum}'
    assert describe((sum, sum, list, chr)) == '(sum, sum, list, chr)'
    

def test_function_in_main():
    '''Test that a function defined in `__main__` is well-described.'''

    ###########################################################################
    # We can't really define a function in `__main__` in this test, so we
    # emulate it:
    with TempValueSetter((globals(), '__name__'), '__main__'):
        def f(x):
            pass
    assert f.__module__ == '__main__'
    import __main__
    __main__.f = f
    del __main__
    #
    ###########################################################################
    
    assert describe(f) == '__main__.f'
    assert resolve(describe(f)) is f
    
    
