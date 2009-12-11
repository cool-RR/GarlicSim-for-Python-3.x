# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This package provides a list of human names as `name_list`.
'''

import pkg_resources

(male_raw, female_raw) = \
    [
        pkg_resources.resource_string(__name__, file_name) for 
        file_name in ['male.txt', 'female.txt']
    ]

name_list = male_raw.split('\r\n') + female_raw.split('\r\n')
