# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing `garlicsim.general_misc.temp_value_setters.TempWorkingDirectorySetter`.
'''



import os
import shutil
import tempfile

from garlicsim.general_misc import cute_testing
from garlicsim.general_misc import temp_file_tools

from garlicsim.general_misc.temp_value_setters import \
     TempWorkingDirectorySetter

class MyException(Exception):
    pass

def test():
    '''Test basic workings of `TempWorkingDirectorySetter`.'''
    with temp_file_tools.TemporaryFolder(prefix='temp_test_garlicsim_') \
                                                          as temp_folder:
        old_cwd = os.getcwd()
        with TempWorkingDirectorySetter(temp_folder):
            
            # Note that on Mac OS, the working dir will be phrased differently,
            # so we can't do `assert os.getcwd() == temp_dir`. Instead we'll
            # create a small file and check we can access it:
            
            with open('just_a_file', 'w') as my_file:
                my_file.write('One two three.')
            
            with open('just_a_file', 'r') as my_file:
                assert my_file.read() == 'One two three.'
        
        with open(os.path.join(temp_folder, 'just_a_file'), 'r') as my_file:
            assert my_file.read() == 'One two three.'
        
        assert os.getcwd() == old_cwd
    
    
def test_exception():
    '''Test `TempWorkingDirectorySetter` recovering from exception in suite.'''
    # Not using `assert_raises` here because getting the `with` suite in there
    # would be tricky.
    with temp_file_tools.TemporaryFolder(prefix='temp_test_garlicsim_') \
                                                          as temp_folder:
        old_cwd = os.getcwd()
        try:
            with TempWorkingDirectorySetter(temp_folder):
                
                # Note that on Mac OS, the working dir will be phrased
                # differently, so we can't do `assert os.getcwd() ==
                # temp_folder`. Instead we'll create a small file and check we
                # can access it:
                
                with open('just_a_file', 'w') as my_file:
                    my_file.write('One two three.')
                
                with open('just_a_file', 'r') as my_file:
                    assert my_file.read() == 'One two three.'
                
                raise MyException
            
        except MyException:

            with open(os.path.join(temp_folder, 'just_a_file'), 'r') \
                                                           as my_file:
                assert my_file.read() == 'One two three.'
                
        else:
            raise Exception
        
        with open(os.path.join(temp_folder, 'just_a_file'), 'r') as my_file:
            assert my_file.read() == 'One two three.'

        
def test_as_decorator():
    '''Test `TempWorkingDirectorySetter` used as a decorator.'''
    with temp_file_tools.TemporaryFolder(prefix='temp_test_garlicsim_') \
                                                          as temp_folder:
        old_cwd = os.getcwd()
        @TempWorkingDirectorySetter(temp_folder)
        def f():
            # Note that on Mac OS, the working dir will be phrased differently,
            # so we can't do `assert os.getcwd() == temp_folder`. Instead we'll
            # create a small file and check we can access it:
            
            with open('just_a_file', 'w') as my_file:
                my_file.write('One two three.')
            
            with open('just_a_file', 'r') as my_file:
                assert my_file.read() == 'One two three.'
                
        f()
        
        cute_testing.assert_polite_wrapper(f)
        
        with open(os.path.join(temp_folder, 'just_a_file'), 'r') as my_file:
            assert my_file.read() == 'One two three.'
        
        assert os.getcwd() == old_cwd
