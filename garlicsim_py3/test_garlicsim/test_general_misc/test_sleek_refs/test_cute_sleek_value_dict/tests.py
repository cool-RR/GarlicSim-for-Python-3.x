# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing module for `garlicsim.general_misc.sleek_refs.CuteSleekValueDict`.
'''

import gc
import weakref

from garlicsim.general_misc import sequence_tools

from garlicsim.general_misc.sleek_refs import (SleekCallArgs,
                                               SleekRef,
                                               CuteSleekValueDict)

from ..shared import _is_weakreffable, A, counter
        
        
def test():
    '''Test the basic workings of `CuteSleekValueDict`.'''
    volatile_things = [A(), 1, 4.5, 'meow', 'woof', [1, 2], (1, 2), {1: 2},
                       set([1, 2, 3])]
    unvolatile_things = [A.s, __builtins__, list, type,  list.append, str.join,
                         sum]
    
    # Using len(csvd) as our key; Just to guarantee we're not running over an
    # existing key.
        
    csvd = CuteSleekValueDict(counter)
    
    while volatile_things:
        volatile_thing = volatile_things.pop()
        if _is_weakreffable(volatile_thing):
            csvd[len(csvd)] = volatile_thing
            count = counter()
            del volatile_thing
            gc.collect()
            assert counter() == count + 2
        else:
            csvd[len(csvd)] = volatile_thing
            count = counter()
            del volatile_thing
            gc.collect()
            assert counter() == count + 1

            
    while unvolatile_things:
        unvolatile_thing = unvolatile_things.pop()
        csvd = CuteSleekValueDict(counter)
        
        csvd[len(csvd)] = unvolatile_thing
        count = counter()
        del unvolatile_thing
        gc.collect()
        assert counter() == count + 1
        
        
def test_one_by_one():
    volatile_things = [A(), 1, 4.5, 'meow', 'woof', [1, 2], (1, 2), {1: 2},
                       set([1, 2, 3])]
    unvolatile_things = [A.s, __builtins__, list, type,  list.append, str.join,
                         sum]
    
    # Using len(csvd) as our key; Just to guarantee we're not running over an
    # existing key.
        
    while volatile_things:
        volatile_thing = volatile_things.pop()
        csvd = CuteSleekValueDict(counter)
        if _is_weakreffable(volatile_thing):
            csvd[len(csvd)] = volatile_thing
            count = counter()
            del volatile_thing
            gc.collect()
            assert counter() == count + 2
        else:
            csvd[len(csvd)] = volatile_thing
            count = counter()
            del volatile_thing
            gc.collect()
            assert counter() == count + 1
            
    while unvolatile_things:
        unvolatile_thing = unvolatile_things.pop()
        csvd = CuteSleekValueDict(counter)
        
        csvd[len(csvd)] = unvolatile_thing
        count = counter()
        del unvolatile_thing
        gc.collect()
        assert counter() == count + 1
        
        
def test_none():
    '''Test that `CuteSleekValueDict` can handle a value of `None`.'''

    d = {
        1: None,
        2: None,
        (1,): None,
        (1, (1,)): None,
        sum: None,
        None: None
    }
    
    csvd = CuteSleekValueDict(
        counter,
        d
    )
    

    assert sequence_tools.are_equal_regardless_of_order(list(csvd.keys()),
                                                        list(d.keys()))
    
    assert sequence_tools.are_equal_regardless_of_order(list(csvd.values()),
                                                        list(d.values()))
    
    assert sequence_tools.are_equal_regardless_of_order(list(csvd.items()),
                                                        list(d.items()))
    

    for key in csvd.keys():
        assert key in csvd
        assert csvd[key] is None
    
    
        
