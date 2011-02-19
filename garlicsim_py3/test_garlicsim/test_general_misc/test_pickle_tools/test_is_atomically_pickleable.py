# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `is_atomically_pickleable`.'''



import threading
import io
import pickle

import nose

from garlicsim.general_misc import import_tools

import garlicsim
from garlicsim.general_misc import pickle_tools

from .shared import PickleableObject, NonPickleableObject


def is_pickle_successful(thing):
    '''`try` to pickle `thing` and return whether it worked.'''
    try:
        string = pickle.dumps(thing)
        unpickled_thing = pickle.loads(string)
    except Exception:
        return False
    else:
        return True

    
def test_simple_atomically_pickleables():
    '''Test `is_atomically_pickleable` on atomically pickleable objects.'''
    pickleables = [
        None, True, False,
        1, 1.1, -3, 3+4.5j,
        'roar', 'Meow!',
        {1: 3, 'frr': 'meow'},
        ['one', 'two', (3, 4)],
        set([1, 2, 3, 1]),
        frozenset((1, 2, 3, 1, 'meow', frozenset())),
        sum, slice, type
    ]
    
    atomically_pickleables = [
        set([threading.Lock()]),
        [threading.Lock()],
    ]
    
    for thing in pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        assert is_pickle_successful(thing)
        
    for thing in atomically_pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        

def test_string_io():
    '''Test `StringIO` is considered pickleable.'''
    if garlicsim.__version_info__ <= (0, 6, 2):
        raise nose.SkipTest("Can't handle `StringIO` yet.")
    string_io = io.StringIO()
    assert is_pickle_successful(string_io)
    assert pickle_tools.is_atomically_pickleable(string_io)
        
        
def test_non_atomically_pickleables_multiprocessing():
    '''
    Test `is_atomically_pickleable` on non-atomically pickleable objects.
    
    Not including `multiprocessing` objects.
    '''
    
    if not import_tools.exists('multiprocessing'):
        raise nose.SkipTest('`multiprocessing` is not installed.')
    
    import multiprocessing

    non_pickleables = [
        multiprocessing.Lock(),
        multiprocessing.BoundedSemaphore(),
        multiprocessing.Condition(),
        multiprocessing.JoinableQueue(),
        multiprocessing.Pool(),
        multiprocessing.Queue(),
        multiprocessing.RLock(),
        multiprocessing.Semaphore(),
    ]
        
    for thing in non_pickleables:
        assert not pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)
    
    assert not pickle_tools.is_atomically_pickleable(NonPickleableObject())
    # Not trying to actually pickle this test object, cause it will actually
    # work.

    
def test_partially_pickleables_multiprocessing():
    '''
    "Partially-pickleable" means an object which is atomically pickleable but
    not pickleable.
    '''

    if not import_tools.exists('multiprocessing'):
        raise nose.SkipTest('`multiprocessing` is not installed.')
    
    import multiprocessing
    
    x = PickleableObject()
    x.lock = threading.Lock()
    
    partially_pickleables = [
        x,
        [multiprocessing.BoundedSemaphore()],
        {1: multiprocessing.Lock(), 2: 3},
        set([multiprocessing.Queue(), x])
    ]
    
    for thing in partially_pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)
        
        
def test_non_atomically_pickleables():
    '''Test `is_atomically_pickleable` on non-atomically pickleable objects.'''

    non_pickleables = [
        threading.Lock(),
    ]
        
    for thing in non_pickleables:
        assert not pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)
    
    assert not pickle_tools.is_atomically_pickleable(NonPickleableObject())
    # Not trying to actually pickle this test object, cause it will actually
    # work.

    
def test_partially_pickleables():
    '''
    Test `is_atomically_pickleable` on partially pickleable objects.
    
    "Partially-pickleable" means an object which is atomically pickleable but
    not pickleable.
    '''
    
    x = PickleableObject()
    x.lock = threading.Lock()
    
    partially_pickleables = [
        x,
        [threading.Lock()],
        {1: threading.Lock(), 2: 3},
        set([threading.Lock(), x])
    ]
    
    for thing in partially_pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)

### Testing old-style classes: ################################################
#                                                                             #
        
class A: # Ooh, look at me! I'm not inheriting from `object`!
    pass

class AtomicallyNonpickleable:
    _is_atomically_pickleable = False
    
class AtomicallyPickleable:
    _is_atomically_pickleable = True
        
        
        
def test_old_style_classes():
    '''Test `is_atomically_pickleable` on old style classes objects.'''
    
    # I hate old-style classes. I hope they'll die soon.
    
    assert pickle_tools.is_atomically_pickleable(A()) is True
    assert pickle_tools.is_atomically_pickleable(
        AtomicallyNonpickleable()
        ) is False
    assert pickle_tools.is_atomically_pickleable(
        AtomicallyPickleable()
        ) is True
    
    # The classes themselves are all pickleable:
    assert pickle_tools.is_atomically_pickleable(A) is True
    assert pickle_tools.is_atomically_pickleable(
        AtomicallyNonpickleable
        ) is True
    assert pickle_tools.is_atomically_pickleable(
        AtomicallyPickleable
        ) is True
    
    
#                                                                             #
### Finished testing old-style classes. #######################################
