#!/usr/bin/env python3
"""
Program:    column_sgpdb
File:       column_sgpdb.py

Version:    V1.0
Date:       08.06.2021
Function:   Keep one pdb code in column

Description:
============
Program uses .csv file and alters the column to clean up the pdb name

Commandline inputs: 1) .csv files of encoded residues with no duplicates
                    2) .dat file with column headers
                    3) final_no_red_{}.csv name of file
------------------------------------------------
"""
# *************************************************************************
# Import libraries

import pandas as pd
import sys


# *************************************************************************
def single_pdb_code():
    """Read the .csv file containing encoded residues and angles and combine lines that have the same PDB code and
    the same encoded sequence into one line, averaging the angle

    Return: res_file      --- Dataframe that contains the first PDB code of a cluster that have the same
    VHVl sequences and angles.

    08.06.2021  Original   By: VAB
    """

    # The column names contained in the .csv file imported from a .dat file
    col1 = []
    for i in open(sys.argv[2]).readlines():
        i = i.strip('\n')
        col1.append(i)

    # Take the commandline input as encoded res file with angles, no duplicates
    if sys.argv[1] != '':
        res_file = pd.read_csv(sys.argv[1], usecols=col1)

    res_file['code'] = res_file['code'].str[:4]

    return res_file


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

results = single_pdb_code()

# export dataframe as a .csv file and don't include the line indices
results.to_csv('final_{}.csv'.format(sys.argv[3]), index=False)
