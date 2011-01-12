# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `CutePickler` and `CuteUnpickler`.'''

import threading
from io import BytesIO 
import tempfile
import pickle

import nose

from garlicsim.general_misc import import_tools

from garlicsim.general_misc import pickle_tools
from garlicsim.general_misc.pickle_tools import CutePickler, CuteUnpickler

from .shared import PickleableObject, NonPickleableObject

    
class Object(object):
    pass


def test_totally_pickleable():
    '''Test cute-(un)pickling on totally pickleable objects.'''
    
    totally_pickleable_things = [
        [1, 2, (3, 4)],
        {1: 2, 3: set((1, 2, 3))},
        None, True, False,
        (1, 2, 'meow'),
        'qweqweqasd',
    ]
    
    for thing in totally_pickleable_things:
        stream = BytesIO() 
        pickler = CutePickler(stream)
        pickler.dump(thing) 
 
        stream.seek(0) 
        unpickler = CuteUnpickler(stream) 
        unpickled_thing = unpickler.load() 
        assert unpickled_thing == thing
        

        
def test_without_multiprocessing():
    '''
    Test cute-(un)pickling on various objects, not incl. `multiprocessing`.
    '''
    totally_pickleable_things = [
        [1, 2, (3, 4)],
        {1: 2, 3: set((1, 2, 3))},
        None, True, False,
        (1, 2, 'meow'),
        'qweqweqasd',
        PickleableObject()
    ]
    
    thing = Object()
    thing.a, thing.b, thing.c, thing.d, thing.e, thing.f, thing.g, thing.h = \
         totally_pickleable_things
    
    thing.x = threading.Lock()
    thing.z = NonPickleableObject()
    
    stream = BytesIO() 
    pickler = CutePickler(stream)
    pickler.dump(thing) 

    stream.seek(0) 
    unpickler = CuteUnpickler(stream) 
    unpickled_thing = unpickler.load() 
    
    assert thing.a == unpickled_thing.a
    assert thing.b == unpickled_thing.b
    assert thing.c == unpickled_thing.c
    assert thing.d == unpickled_thing.d
    assert thing.e == unpickled_thing.e
    assert thing.f == unpickled_thing.f
    assert thing.g == unpickled_thing.g
    # Regarding `.h`, we just check the type cause there's no `__eq__`:
    assert type(thing.h) == type(unpickled_thing.h)
    
    assert thing.x != unpickled_thing.x
    assert thing.z != unpickled_thing.z
    
    assert isinstance(unpickled_thing.x, pickle_tools.FilteredObject)
    assert isinstance(unpickled_thing.z, pickle_tools.FilteredObject)
    
    
def test():
    '''Test cute-(un)pickling on various objects.'''
    if not import_tools.exists('multiprocessing'):
        raise nose.SkipTest('`multiprocessing` is not installed.')
    
    import multiprocessing
    
    totally_pickleable_things = [
        [1, 2, (3, 4)],
        {1: 2, 3: set((1, 2, 3))},
        None, True, False,
        (1, 2, 'meow'),
        'qweqweqasd',
        PickleableObject()
    ]
    
    thing = Object()
    thing.a, thing.b, thing.c, thing.d, thing.e, thing.f, thing.g, thing.h = \
         totally_pickleable_things
    
    thing.x = threading.Lock()
    thing.y = multiprocessing.Lock()
    thing.z = NonPickleableObject()
    
    stream = BytesIO() 
    pickler = CutePickler(stream)
    pickler.dump(thing) 

    stream.seek(0) 
    unpickler = CuteUnpickler(stream) 
    unpickled_thing = unpickler.load() 
    
    assert thing.a == unpickled_thing.a
    assert thing.b == unpickled_thing.b
    assert thing.c == unpickled_thing.c
    assert thing.d == unpickled_thing.d
    assert thing.e == unpickled_thing.e
    assert thing.f == unpickled_thing.f
    assert thing.g == unpickled_thing.g
    # Regarding `.h`, we just check the type cause there's no `__eq__`:
    assert type(thing.h) == type(unpickled_thing.h)
    
    assert thing.x != unpickled_thing.x
    assert thing.y != unpickled_thing.y
    assert thing.z != unpickled_thing.z
    
    assert isinstance(unpickled_thing.x, pickle_tools.FilteredObject)
    assert isinstance(unpickled_thing.y, pickle_tools.FilteredObject)
    assert isinstance(unpickled_thing.z, pickle_tools.FilteredObject)
    
    
    
    
    