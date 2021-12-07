#!/usr/bin/env python3
"""
Program:    textlines2pdbdirectory
File:       textlines2pdbdirectory.py

Version:    V1.0
Date:       12.06.2021
Function:   Read text file and add pdb files with those name into a new directpry.

Description:
============
Program reads pdb file names from .txt, looks for these files in a directory and copies them into a new directory.

Commandline inputs: 1) .txt file
                    2)  directory where pdb files are
                    3) new_directory
                    4) directory for remaining files

------------------------------------------------
"""
# *************************************************************************
# Import libraries
import sys
import os
import shutil


# *************************************************************************
def find_files():

    file_with_names = sys.argv[1]
    list_of_names = open(file_with_names).readlines()
    list_of_names = [file.strip() for file in list_of_names]

    dir_with_pdbs = sys.argv[2]
    new_dir = sys.argv[3]
    remaining_dir = sys.argv[4]

    cwd = os.getcwd()
    try:
        os.mkdir(new_dir)
    except OSError:
        print("Creation of the directory failed")

    try:
        os.mkdir(remaining_dir)
    except OSError:
        print("Creation of the directory failed")

    postAF2 = []
    for name in list_of_names:
        for file in os.listdir(dir_with_pdbs):
            if file.endswith('pdb'):
                if str(name) in str(file):
                    src = os.path.join(cwd, dir_with_pdbs, file)
                    dst = os.path.join(cwd, new_dir, file)
                    shutil.copyfile(src, dst)
                    print('postAF2:', file)
                else:
                    src = os.path.join(cwd, dir_with_pdbs, file)
                    dst = os.path.join(cwd, remaining_dir, file)
                    shutil.copyfile(src, dst)
                    print('preAF2:', file)

# *************************************************************************
result = find_files()