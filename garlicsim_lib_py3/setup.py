#!/usr/bin/env python3

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Setuptools setup file for garlicsim_lib.'''

import os
import sys
import setuptools


### Ensuring correct Python version: ##########################################
#                                                                             #
if sys.version_info[0] <= 2:
    raise Exception('This package requires Python 3.x. For Python 2.5+, use '
                    '`garlicsim_lib`, which you can find on PyPI.')

#                                                                             #
### Finished ensuring correct Python version. #################################


def get_garlicsim_lib_packages():
    '''
    Get all the packages in `garlicsim_lib`.
    
    Returns something like:
    
        ['garlicsim_lib', 'garlicsim_lib.simpacks',
        'garlicsim_lib.simpacks.life', ... ]
        
    '''
    return ['garlicsim_lib.' + p for p in
            setuptools.find_packages('./garlicsim_lib')] + \
           ['garlicsim_lib']


def get_test_garlicsim_lib_packages():
    '''
    Get all the packages in `test_garlicsim_lib`.
    
    Returns something like:
    
        ['test_garlicsim_lib', 'test_garlicsim_lib.test_simpacks', ...]
        
    '''
    return ['test_garlicsim_lib.' + p for p in
            setuptools.find_packages('./test_garlicsim_lib')] + \
           ['test_garlicsim_lib']


def get_packages():
    '''
    Get all the packages in `garlicsim_lib` and `test_garlicsim_lib`.
    
    Returns something like:
    
        ['test_garlicsim_lib', 'garlicsim_lib', 'garlicsim_lib.simpacks',
        'test_garlicsim_lib.test_simpacks', ... ]
        
    '''
    return get_garlicsim_lib_packages() + get_test_garlicsim_lib_packages()


my_long_description = \
'''\
Collection of GarlicSim simulation packages, for various scientific fields.

To be used with `garlicsim`.

Visit http://garlicsim.org for more info.
'''

my_classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    ('License :: OSI Approved :: GNU Library or Lesser General '
     'Public License (LGPL)'),
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Topic :: Scientific/Engineering',
]


setuptools.setup(
    name='garlicsim_lib_py3',
    version='0.6.2',
    requires=['garlicsim_py3 (== 0.6.2)'],
    install_requires=['garlicsim_py3 == 0.6.2'],
    tests_require=['nose>=1.0.0'],
    description='Collection of GarlicSim simulation packages',
    author='Ram Rachum',
    author_email='cool-rr@cool-rr.com',
    url='http://garlicsim.org',
    packages=get_packages(),
    scripts=['test_garlicsim_lib/scripts/_test_garlicsim_lib_py3.py'],
    license='LGPL v2.1',
    long_description=my_long_description,
    classifiers=my_classifiers,
    include_package_data=True,
    zip_safe=False,
)

