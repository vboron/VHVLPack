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
def run_csv2arff():
    directory = sys.argv[1]
    cwd = os.getcwd()
    path = os.path.join(cwd, directory)
    for file in os.listdir(directory):
        f_path = os.path.join(path, file)
        print(f_path)
        arff_path = os.path.join(path, (file[:-4] + '.arff'))
        with open(arff_path, 'w') as arff_out:
            try:
                args = ['csv2arff', '-ni', sys.argv[2], 'angle', f_path]
                subprocess.run(args, stdout=arff_out, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print(f'{file} cannot be converted.')


# *************************************************************************
# Main
# *************************************************************************

result = run_csv2arff()
