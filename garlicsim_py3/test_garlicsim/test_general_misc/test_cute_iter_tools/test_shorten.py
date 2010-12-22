# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.cute_iter_tools.shorten`.'''

import nose.tools

from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc.cute_iter_tools import shorten


def test():
    '''Test basic workings of `shorten`.'''
    my_range = [0, 1, 2, 3, 4]

    short_iterator = shorten(my_range, 3)
    assert short_iterator.__iter__() is short_iterator
    
    assert list(shorten(my_range, 0)) == []
    assert list(shorten(my_range, 1)) == list(range(1))
    assert list(shorten(my_range, 2)) == list(range(2))
    assert list(shorten(my_range, 3)) == list(range(3))
    assert list(shorten(my_range, 4)) == list(range(4))
    
    assert list(shorten(my_range, infinity)) == my_range
    assert list(shorten(iter(my_range), infinity)) == my_range

    
def test_dont_pull_extra_item():
    '''Test that `shorten` doesn't pull an extra member from the iterable.'''
    def generator():
        yield 1
        yield 2
        yield 3
        raise Exception

    nose.tools.assert_raises(Exception, lambda: list(generator()))
    
    iterator_1 = shorten(generator(), 4)
    nose.tools.assert_raises(Exception, lambda: list(iterator_1))
    
    iterator_2 = shorten(generator(), infinity)
    nose.tools.assert_raises(Exception, lambda: list(iterator_2))
    
    iterator_3 = shorten(generator(), 3)
    list(iterator_3) # Pulling exactly three so we avoid the exception.