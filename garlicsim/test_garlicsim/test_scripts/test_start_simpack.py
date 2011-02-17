# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.



import tempfile
import shutil
import glob

from garlicsim.general_misc import sys_tools
from garlicsim.general_misc.temp_value_setters import \
     TempWorkingDirectorySetter

import garlicsim.scripts


_help_text = '''
Script for starting a new simpack.

This is a script for creating a skeleton for a `garlicsim` simpack. Use this
when you want to make a new simpack to have the basic folders and files created
for you.

Usage:

    start_simpack.py my_simpack_name

The simpack will be created in the current path, in a directory with the name
of the simpack.
'''
        

def test_implicit_help():
    '''Test help text comes up when giving no arguments.'''
    temp_dir = tempfile.mkdtemp(prefix='temp_test_garlicsim_')
    try:
        with TempWorkingDirectorySetter(temp_dir):
            with sys_tools.OutputCapturer() as output_capturer:
                garlicsim.scripts.start_simpack.start(
                    argv=['start_simpack.py']
                )
            assert output_capturer.output == _help_text + '\n'
            assert glob.glob('*') == []
            
    finally:
        shutil.rmtree(temp_dir)
        

def test_explicit_help():
    '''Test help text comes up when '--help' argument.'''
    temp_dir = tempfile.mkdtemp(prefix='temp_test_garlicsim_')
    try:
        with TempWorkingDirectorySetter(temp_dir):
            with sys_tools.OutputCapturer() as output_capturer:
                garlicsim.scripts.start_simpack.start(
                    argv=['start_simpack.py', '--help']
                )
            assert output_capturer.output == _help_text + '\n'
            assert glob.glob('*') == []
            
    finally:
        shutil.rmtree(temp_dir)