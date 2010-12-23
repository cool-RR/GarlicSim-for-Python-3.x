# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools related to file-system paths.'''

import os.path
import glob


def list_sub_folders(path, exclude=[]):
    '''List all the immediate sub-folders of the folder at `path`.tododoc'''
    
    if isinstance(exclude, str): # Allowing single `exclude` instead of set
        exclude = [exclude]
        
    assert os.path.isdir(path)
    files_and_folders = glob.glob(os.path.join(path, '*'))
    folders = [folder for folder in filter(os.path.isdir, files_and_folders)
               if folder not in exclude]
    
    return folders