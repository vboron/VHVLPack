#!/usr/bin/env python3

import sys
import os
import shutil

def move_old_files_out():
    old_file_dir = os.listdir(sys.argv[1])
    clean_file_dir = os.listdir(sys.argv[2])

    cwd = os.getcwd()

    new_dir_for_old_files = sys.argv[3]
    new_dir_for_new_files = sys.argv[4]

    path_for_old = os.path.join(cwd, new_dir_for_old_files)
    path_for_new = os.path.join(cwd, new_dir_for_new_files)

    try:
        os.mkdir(path_for_old)
    except:
        print(new_dir_for_old_files, 'already exists')
    
    try:
        os.mkdir(path_for_new)
    except:
        print(new_dir_for_new_files, 'already exists')

    for file in clean_file_dir:
        if str(file).endswith('.pdb'):
            if file in old_file_dir:
                src = os.path.join(cwd, sys.argv[2], file)
                dst = os.path.join(path_for_old, file)
                shutil.copy2(src, dst)
                
            else:
                src = os.path.join(cwd, sys.argv[2], file)
                dst = os.path.join(path_for_new, file)
                shutil.copy2(src, dst)
    

test = move_old_files_out()
