#!/usr/bin/env python3
"""
Program:    extract_new_files
File:       extract_new_files.py

Version:    V1.0
Date:       28.09.2021
Function:   Make a directory with pdb files that were not in the previous set.

Description:
============
Program checks if .pdb file appears previously and if not, extracts it and copies it to a new directory.

------------------------------------------------
"""
# *************************************************************************
# Import libraries
import sys
import os
import shutil


# *************************************************************************
def find_files():

    new_dir = sys.argv[3]
    try:
        os.mkdir(new_dir)
    except OSError:
        print("Creation of the directory failed")


    od = sys.argv[1]
    nd = sys.argv[2]

    nd_list = []
    for file in os.listdir(nd):
        if str(file).endswith('.csv'):
            f_name = str(file)[:-4]
            f_name = f_name.upper()
            nd_list.append(f_name)
    #print(nd_list)

    od_list = []
    for file in os.listdir(od):
        if str(file).endswith('.pdb'):
            f_name = str(file)[:-4]
            od_list.append(f_name)
    #print(od_list)

    result = [i for i in nd_list if i not in od_list]
    cwd = os.getcwd()
    path = os.path.join(cwd, new_dir)
    for item in result:
        #print('point 1')
        item = str(item).lower() + '.csv'
        shutil.copy(os.path.join(sys.argv[2], item), path)
        print(item, path)
    return


# *************************************************************************
result = find_files()
