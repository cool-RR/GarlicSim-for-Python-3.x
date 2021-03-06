# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Module for manipulating Python addresses.

Use `resolve` to turn a string description into an object, and `describe` to
turn an object into a string.

For example:

    >>> address_tools.describe(list)
    'list'
    >>> address_tools.resolve('list')
    <class 'list'>
    >>> address_tools.describe([1, 2, {3: 4}])
    '[1, 2, {3: 4}]'
    >>> address_tools.resolve('{email.encoders: 1}')
    {<module 'email.encoders' from 'c:\Python27\lib\email\encoders.pyc'>: 1}
    
'''


from .string_to_object import resolve
from .object_to_string import describe