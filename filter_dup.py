#!/usr/bin/env python3
"""
Program:    filter_dup
File:       filter_dup.py

Version:    V4.0
Date:       11.05.2021
Function:   Combine duplicate pdb files and average angles.

Description:
============
The program will take take the output .csv file that contains encoded sequence and angles and if the sequence of
residues are the same for a pdb, it'll average the angle to produce one angle per sequence.

Commandline input: 1) encoded .csv file
                   2) .dat file with column names
                   3) outtput name for no_dup_{}.csv
--------------------------------------------------------------------------
"""

# *************************************************************************
# Import libraries

import pandas as pd
import sys


# *************************************************************************
def remove_duplicates():
    """Read the .csv file containing encoded residues and angles and combine lines that have the same PDB code and
    the same encoded sequence into one line, averaging the angle

    Return: seq_df      --- Dataframe that contains a single angle for all PDB files with unique sequences

    17.04.2021  Original   By: VAB
    """

    # The column names contained in the .csv file imported from a .dat file
    col1 = []
    for i in open(sys.argv[2]).readlines():
        i = i.strip('\n')
        col1.append(i)

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        res_file = pd.read_csv(sys.argv[1], usecols=col1)

    # remove lines that don't contain angles
    try:
        res_file = res_file[res_file['angle'].str.contains('Packing angle') == False]
    except:
        print('No missing angles.')

    # makes the code column just the pdb code, so that all versions can be combined
    res_file['code'] = res_file['code'].str[:5]

    # angle needs to be converted to a float to be averaged
    res_file['angle'] = res_file['angle'].astype(float)
    aggregation_func = {'angle': 'mean'}

    # remove 'angle' from columns header list, since program is not grouping by angle
    col1.remove('angle')

    seq_df = res_file.groupby(col1).aggregate(aggregation_func)
    seq_df = seq_df.reset_index()
    seq_df['code'] = seq_df['code'].str[:4]
    return seq_df


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

results = remove_duplicates()

results.to_csv('no_dup_{}.csv'.format(sys.argv[3]), index=False)
