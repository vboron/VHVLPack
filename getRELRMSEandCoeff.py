#!/usr/bin/python3
"""
Program:    column_sgpdb
File:       column_sgpdb.py

Version:    V1.0
Date:       08.06.2021
Function:   Keep one pdb code in column

Description:
============
This program find and averages the RELRMSE and Correlation coefficients across test.log files
for cross-validation.

Commandline inputs: 1) directory
                    2) .csv file with encoded residues
                    3) .dat file with column headers
------------------------------------------------
"""
# *************************************************************************
# Import libraries

import pandas as pd
import sys
import os
import glob
import subprocess

# *************************************************************************
def get_directory():
    """Read the directory name from the commandline argument

    Return: direct      --- Directory of .log files that will be processed

    15.03.2021  Original   By: VAB
    """

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        direct = sys.argv[1]

    return direct


# *************************************************************************
def find_data(direct):
    """Look through test.log files and calculate the average correlation coefficient and RELRMSE

    Input:  direct       --- read directory


    09.06.2021  Original   By: VAB
    """

    # Creates an empty list, then iterates over all files in the directory called from the
    # commandline. Adds all these .pdb files to the list.
    files = []
    coeff = []
    RMSE = []

    for file in os.listdir(direct):
        if file.endswith('test.log'):
            files.append('{}/{}'.format(direct, file))
            num_files = len(files)

    for log_file in files:
        with open(log_file) as text_file:

            # Splits each file into lines by splitting at a newline character
            for line in text_file.read().split('\n'):

                # Search for lines that contain 'Correlation coefficient' and add to list
                if str(line).strip().startswith('Correlation coefficient'):
                    line = line.replace(' ', '')
                    line = line.split('ent')
                    cc = float(line[1])
                    coeff.append(cc)

                # Search for lines that contain 'Root mean squared error' and add to list
                if str(line).strip().startswith('Root mean squared error'):
                    line = line.replace(' ', '')
                    line = line.split('error')
                    rmse_value = float(line[1])
                    RMSE.append(rmse_value)

    print('average correlation coefficient:', sum(coeff)/num_files)
    print('average RMSE:', sum(RMSE)/num_files)

    # Call the python script that calculates RELRMSE from RMSE
    try:
        RELRMSE=subprocess.check_output(['python3', 'RELRMSE.py', sys.argv[2], sys.argv[3], str(sum(RMSE)/num_files)])
        print('RELRMSE:', RELRMSE.strip())

    except subprocess.CalledProcessError:
        print('error: cannot calculate RELRMSE')


    return


# *************************************************************************
# ******* Main ************************************************************
# *************************************************************************

directory = get_directory()

values = find_data(directory)

