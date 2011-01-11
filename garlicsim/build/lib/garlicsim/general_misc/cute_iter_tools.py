# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines functions for manipulating iterators.'''
# todo: make something like `filter` except it returns first found, or raises
# exception

import itertools
import builtins

from garlicsim.general_misc.infinity import infinity


def consecutive_pairs(iterable, wrap_around=False):
    '''
    Iterate over successive pairs from the iterable.
    
    If `wrap_around=True`, will include a `(last_item, first_item)` pair at the
    end.
        
    Example: if the iterable is [0, 1, 2, 3], then its `consecutive_pairs`
    would be `[(0, 1), (1, 2), (2, 3)]`. (Except it would be an iterator and
    not an actual list.)
    '''
    iterator = iter(iterable)
    
    try:
        first_item = next(iterator)
    except StopIteration:
        raise StopIteration
    
    old = first_item
    
    for current in iterator:
        yield (old, current)
        old = current
        
    if wrap_around:
        yield (current, first_item)

        
def orderless_combinations(iterable, n, start=0):
    '''
    Iterate over combinations of items from the iterable.

    `n` specifies the number of items. `start` specifies the member number from
    which to start giving combinations. (Keep the default of 0 for doing the
    whole iterable.)
    
    Example:
    
    `orderless_combinations([1, 2, 3, 4], n=2)` would be, in list form:
    `[[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]`.
    '''
    # todo: optimize or find 3rd party tool
    
    if n == 1:
        for thing in itertools.islice(iterable, start, None):
            yield [thing]
    for (i, thing) in itertools.islice(enumerate(iterable), start, None):
        for sub_result in orderless_combinations(iterable, n-1, start=i+1):
            yield [thing] + sub_result
    
    
def shorten(iterable, n):
    '''
    Shorten an iterator to length `n`.
    
    Iterate over the given iterable, but stop after `n` iterations (Or when the
    iterable stops iteration by itself.)
    
    `n` may be infinite.
    '''

    if n == infinity:
        for thing in iterable:
            yield thing
        raise StopIteration
    
    assert isinstance(n, int)

    if n == 0:
        raise StopIteration
    
    for i, thing in enumerate(iterable):
        yield thing
        if i + 1 == n: # Checking `i + 1` to avoid pulling an extra item.
            raise StopIteration
        
        
def enumerate(reversable, reverse_index=False):
    '''
    Iterate over `(i, item)` pairs, where `i` is the index number of `item`.
    
    This is an extension of the builtin `enumerate`. What it allows is to get a
    reverse index, by specifying `reverse_index=True`. This causes `i` to count
    down to zero instead of up from zero, so the `i` of the last member will be
    zero.
    '''
    if reverse_index is False:
        return builtins.enumerate(reversable)
    else:
        my_list = list(builtins.enumerate(reversed(reversable)))
        my_list.reverse()
        return my_list

    
def is_iterable(thing):
    '''Return whether an object is iterable.'''
    return hasattr(thing, '__iter__')


def get_length(iterable):
    '''Get the length of an iterable.'''
    i = 0
    for thing in iterable:
        i += 1
    return i


def product(*args, **kwargs):
    '''
    Cartesian product of input iterables.

    Equivalent to nested for-loops in a generator expression. `product(A, B)`
    returns the same as `((x,y) for x in A for y in B)`.
    
    More examples:
    
        list(product('ABC', 'xy')) == ['Ax', 'Ay', 'Bx', 'By', 'Cx', 'Cy']
        
        list(product(range(2), repeat=2) == ['00', '01', '10', '11']
        
    '''
    # todo: revamp
    pools = list(map(tuple, args)) * kwargs.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def iter_with(iterable, context_manager):
    '''Iterate on `iterable`, `with`ing the context manager on every `next`.'''
    
    while True:
        
        with context_manager:
            next_item = next(iterable)
            # You may notice that we are not `except`ing a StopIteration here;
            # If we get one, it'll just get propagated and end *this* iterator.
            # todo: I just realized this will probably cause a bug where
            # `__exit__` will get the `StopIteration`! Make failing tests and
            # fix.
        
        yield next_item
        
        