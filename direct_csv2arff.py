#!/usr/bin/python3
"""
Program:    direct_csv2arff
File:       direct_csv2arff.py

Version:    V1.1
Date:       18.05.2021
Function:   Run csv2arff on multiple files

Description:
============
Program will run csv2arff program on all files in the inputted directory

Commandline inputs: 1) directory which contains test/train csv files
                    2) .dat file with inputs
--------------------------------------------------------------------------
"""
# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, subprocess for running external program, pandas
# for making dataframes
import os
import subprocess
import sys
import pandas as pd


# *************************************************************************
def get_pdbdirectory():
    """Read the directory name from the commandline argument

    Return: pdb_direct      --- Directory of PBD files that will be processed for VH-VL packing angles

    15.03.2021  Original   By: VAB
    """

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        pdb_direct = sys.argv[1]
    else:
        pdb_direct = '.'
    return pdb_direct


# *************************************************************************
def run_csv2arff(directory):
    cwd = os.getcwd()
    path = '{}/{}'.format(cwd, sys.argv[1])
    print(path)
    for file in os.listdir(directory):

        # Uses the subprocess module to call abpackingangle and inputs the headers/.pdb lists
        # into the program as arguments
        try:
            arff_file = subprocess.check_output(['csv2arff', '-ni', sys.argv[2], 'angle', file, '>',
                                                 '{}/{}.arff'.format(path, file[:-4])])
            
            print('{} converted.'.format(file))
        except subprocess.CalledProcessError:
            print('{} cannot be converted.'.format(file))
            continue


# *************************************************************************
# Main
# *************************************************************************

pdb_directory = get_pdbdirectory()

result = run_csv2arff(pdb_directory)

