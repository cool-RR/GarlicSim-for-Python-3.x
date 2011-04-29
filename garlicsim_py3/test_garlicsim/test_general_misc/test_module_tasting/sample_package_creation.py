# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

from __future__ import with_statement

import compileall
import shutil
import zipfile
import os.path

from garlicsim.general_misc import temp_file_tools 
from garlicsim.general_misc import zip_tools


formats = ('py', 'pyco', 'zip')


def create_sample_package(format, folder):
    assert format in formats
    
    assert not os.listdir(folder) # `folder` is empty
    
    package_path = os.path.join(folder, 'my_package')
    os.mkdir(package_path)
    
    init_file_path = os.path.join(package_path, '__init__.py')
    submodule_file_path = os.path.join(package_path, 'submodule.py')
    johnny_file_path = os.path.join(package_path, 'johnny.py')
    
    with open(init_file_path, 'w') as init_file:
        init_file.write(
            "'''The tasted module's docstring.'''\n"
            "\n"
            "from .submodule import woo\n"
            "from .submodule.rarrr.rrsadg.sdv import meow\n"
            "\n"
            "\n"
            "my_string = 'Just a string'\n"
            "\n"
            "my_list = ['A', 'list', 'of', 'stuff']\n"
        )
    
    with open(submodule_file_path, 'w') as submodule_file:
        submodule_file.write(
            "raise Exception('This module should never be imported.')"
        )
    
    with open(johnny_file_path, 'w') as johnny_file:
        johnny_file.write(
            "from . import submodule\n"
            "number_nine = 9\n"
        )
            
    if format == 'py':
        return folder
        
    if format == 'pyco':
        compileall.compile_dir(package_path, quiet=1)
            
        os.remove(init_file_path)
        os.remove(submodule_file_path)
        os.remove(johnny_file_path)
        
        assert len(os.listdir(package_path)) == 3
        assert all([file_path[-3:-1] == 'py' for file_path in
                    os.listdir(package_path)])
        
        return folder
    
    elif format == 'zip':
        with temp_file_tools.TemporaryFolder(prefix='test_garlicsim_') as \
                                                              temporary_folder:
            
            temp_zip_path = os.path.join(temporary_folder, '1.zip')
            final_zip_path = os.path.join(folder, '1.zip')
            
            zip_tools.zip_folder(
                package_path,
                temp_zip_path
            )            
            
            os.remove(init_file_path)
            os.remove(submodule_file_path)
            os.remove(johnny_file_path)
            
            shutil.move(
                temp_zip_path,
                final_zip_path
            )
            
            return final_zip_path