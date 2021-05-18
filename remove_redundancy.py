#!/usr/bin/python3
"""
Program:    remove_redundancy
File:       remove_redundancy.py

Version:    V1.0
Date:       01.05.2021
Function:   Cluster all PDBs that contain the same sequence and the same angle

Description:
============
Program uses the encoded residues and angles in order to group all PDB files that are identical matches and returns
a table with the first column being a list of all of the PDB codes, followed by the encoded residues and the angle.

Commandline inputs: 1) .csv files of encoded residues with no duplicates
                    2) .dat file with column headers
------------------------------------------------
"""
# *************************************************************************
# Import libraries

import pandas as pd
import sys


# *************************************************************************
def remove_duplicates():
    """Read the .csv file containing encoded residues and angles and combine lines that have the same PDB code and
    the same encoded sequence into one line, averaging the angle

    Return: seq_df      --- Dataframe that contains the PDB codes of files that have the same VHVl sequences and
    angles.

    01.05.2021  Original   By: VAB
    """

    # The column names contained in the .csv file imported from a .dat file
    col1 = []
    for i in open(sys.argv[2]).readlines():
        i = i.strip('\n')
        col1.append(i)

    # Take the commandline input as encoded res file with angles, no duplicates
    if sys.argv[1] != '':
        res_file = pd.read_csv(sys.argv[1], usecols=col1)

    # remove lines that don't contain angles
    try:
        res_file = res_file[res_file['angle'].str.contains('Packing angle') == False]
    except:
        print('No missing angles.')

    # angle needs to be converted to a float
    res_file['angle'] = res_file['angle'].astype(float)
    res_file['angle'] = res_file['angle'].round()

    # make a list of all combined pdb names separated by commas and add them as a value
    agg_func = {'code': ', '.join}

    seq_df = res_file.groupby(col1[1:]).aggregate(agg_func)
    seq_df = seq_df.reset_index()

    # columns were re-ordered so that the PDB code would be first
    seq_df = seq_df[col1]
    seq_df = seq_df.sort_values('code')

    return seq_df


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

results = remove_duplicates()

# export dataframe as a .csv file and don't include the line indices
results.to_csv('no_red_{}.csv'.format(sys.argv[3]), index=False)
