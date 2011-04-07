# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `OrderedDict` class.

See its documentation for more information.
'''

from collections import MutableMapping
from weakref import proxy as _proxy

class _Link(object):
    __slots__ = 'prev', 'next', 'key', '__weakref__'


class OrderedDict(dict, MutableMapping):
    '''Dict that maintains order of items.'''

    def __init__(self, *args, **kwds):
        '''Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.

        '''
        self.__in_repr = False
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__hardroot = _Link()
            self.__root = root = _proxy(self.__hardroot)
            root.prev = root.next = root
            self.__map = {}
        self.update(*args, **kwds)

        
    def __setitem__(self, key, value,
                    dict_setitem=dict.__setitem__, proxy=_proxy, Link=_Link):
        '''od.__setitem__(i, y) <==> od[i]=y'''
        # Setting a new item creates a new link which goes at the end of the linked
        # list, and the inherited dictionary is updated with the new key/value pair.
        if key not in self:
            self.__map[key] = link = Link()
            root = self.__root
            last = root.prev
            link.prev, link.next, link.key = last, root, key
            last.next = link
            root.prev = proxy(link)
        dict_setitem(self, key, value)

        
    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        '''od.__delitem__(y) <==> del od[y]'''
        # Deleting an existing item uses self.__map to find the link which is
        # then removed by updating the links in the predecessor and successor nodes.
        dict_delitem(self, key)
        link = self.__map.pop(key)
        link_prev = link.prev
        link_next = link.next
        link_prev.next = link_next
        link_next.prev = link_prev
        
        
    def __iter__(self):
        '''od.__iter__() <==> iter(od)'''
        # Traverse the linked list in order.
        root = self.__root
        curr = root.next
        while curr is not root:
            yield curr.key
            curr = curr.next

            
    def __reversed__(self):
        '''od.__reversed__() <==> reversed(od)'''
        # Traverse the linked list in reverse order.
        root = self.__root
        curr = root.prev
        while curr is not root:
            yield curr.key
            curr = curr.prev

    def clear(self):
        '''D.clear() -> None.  Remove all items from D.'''
        root = self.__root
        root.prev = root.next = root
        self.__map.clear()
        dict.clear(self)

            
    def popitem(self, last=True):
        '''
        od.popitem() -> (k, v), return and remove a (key, value) pair.
        
        Pairs are returned in LIFO order if last is true or FIFO order if false.
        '''
        if not self:
            raise KeyError('dictionary is empty')
        root = self.__root
        if last:
            link = root.prev
            link_prev = link.prev
            link_prev.next = root
            root.prev = link_prev
        else:
            link = root.next
            link_next = link.next
            root.next = link_next
            link_next.prev = root
        key = link.key
        del self.__map[key]
        value = dict.pop(self, key)
        return key, value

    
    def move_to_end(self, key, last=True):
        '''Move an existing element to the end (or beginning if last==False).

        Raises KeyError if the element does not exist.
        When last=True, acts like a fast version of self[key]=self.pop(key).

        '''
        link = self.__map[key]
        link_prev = link.prev
        link_next = link.next
        link_prev.next = link_next
        link_next.prev = link_prev
        root = self.__root
        if last:
            last = root.prev
            link.prev = last
            link.next = root
            last.next = root.prev = link
        else:
            first = root.next
            link.prev = root
            link.next = first
            root.next = first.prev = link


    def __reduce__(self):
        items = [[k, self[k]] for k in self]
        tmp = self.__map, self.__root, self.__hardroot
        del self.__map, self.__root, self.__hardroot
        inst_dict = vars(self).copy()
        self.__map, self.__root, self.__hardroot = tmp
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)


    def __sizeof__(self):
        sizeof = _sys.getsizeof
        n = len(self) + 1                       # number of links including root
        size = sizeof(self.__dict__)            # instance dictionary
        size += sizeof(self.__map) * 2          # internal dict and inherited dict
        size += sizeof(self.__hardroot) * n     # link objects
        size += sizeof(self.__root) * n         # proxy objects
        return size

    setdefault = MutableMapping.setdefault
    update = MutableMapping.update
    pop = MutableMapping.pop
    keys = MutableMapping.keys
    values = MutableMapping.values
    items = MutableMapping.items
    __ne__ = MutableMapping.__ne__

    
    def __repr__(self):
        '''od.__repr__() <==> repr(od)'''
        if self.__in_repr:
            return '...'
        if not self:
            return '%s()' % (self.__class__.__name__,)
        self.__in_repr = True
        try:
            result = '%s(%r)' % (self.__class__.__name__, list(self.items()))
        finally:
            self.__in_repr = False
        return result

    
    def copy(self):
        '''od.copy() -> a shallow copy of od'''
        return self.__class__(self)

    
    @classmethod
    def fromkeys(cls, iterable, value=None):
        '''OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).

        '''
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    
    def __eq__(self, other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        '''
        if isinstance(other, OrderedDict):
            return len(self)==len(other) and \
                   all(p==q for p, q in zip(list(self.items()), list(other.items())))
        return dict.__eq__(self, other)

    
    def sort(self, key=None):
        '''
        Sort the items according to their keys, changing the order in-place.
        
        The optional `key` argument, (not to be confused with the dictionary
        keys,) will be passed to the `sorted` function as a key function.
        '''
        sorted_keys = sorted(self.keys(), key=key)
        for key in sorted_keys[1:]:
            self.move_to_end(key)
        
            
    def index(self, key):
        '''Get the index number of `key`.'''
        if key not in self:
            raise KeyError
        for i, key_ in enumerate(self):
            if key_ == key:
                return i
        raise RuntimeError
