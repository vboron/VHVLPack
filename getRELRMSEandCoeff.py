#!/usr/bin/python3
"""
Function:

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

import os
import utils

# *************************************************************************
def find_data(testlog_dir, encoded_csv, csv_cols):
    """Look through test.log files and calculate the average correlation coefficient and RELRMSE

    Input:  direct       --- read directory


    09.06.2021  Original   By: VAB
    """
    # Creates an empty list, then iterates over all files in the directory called from the
    # commandline. Adds all these .pdb files to the list.
    files = []
    coeff = []
    RMSE = []

    for file in os.listdir(testlog_dir):
        if file.endswith('test.log'):
            files.append(os.path.join(testlog_dir, file))

    num_files = len(files)

    for log_file in files:
        if 'test.log' in log_file:
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

    relrmse=utils.calc_relemse(encoded_csv, csv_cols, str(sum(RMSE)/num_files))
    return relrmse


# *************************************************************************
# ******* Main ************************************************************
# *************************************************************************

values = find_data(directory)
