#!/usr/bin/python3
"""
Program:    filter_dup_ts
File:       filter_dup_ts.py

Version:    V1.0
Date:       17.04.2021
Function:   Combine duplicate pdb files and average angles.

Description:
============
The program will take take the output .csv file that contains encoded sequence and angles and if the sequence of
residues is the same for a pdb, it'll average the angle to produce one angle per sequence.

--------------------------------------------------------------------------
"""

# *************************************************************************
# Import libraries

import pandas as pd
import sys
sys.path.append('/serv/www/html_lilian/libs')
sys.path.append('./CDRH3lib')
sys.path.append('~/sync_project/WWW/CDRH3loop')


# *************************************************************************
def remove_duplicates():
    """Read the .csv file containing encoded residues and angles and combine lines that have the same PDB code and
    the same encoded sequence into one line, averaging the angle

    Return: seq_df      --- Dataframe that contains a single angle for all PDB files with unique sequences

    17.04.2021  Original   By: VAB
    """

    # The column names contained in the .csv file
    col1 = ['code', 'L38a', 'L38b', 'L38c', 'L38d', 'L38e', 'L40a', 'L40b', 'L40c', 'L40d', 'L40e', 'L41a', 'L41b',
            'L41c', 'L41d', 'L41e', 'L44a', 'L44b', 'L44c', 'L44d', 'L44e',
            'L46a', 'L46b', 'L46c', 'L46d', 'L46e', 'L87a', 'L87b', 'L87c', 'L87d', 'L87e',
            'H33a', 'H33b', 'H33c', 'H33d', 'H33e', 'H42a', 'H42b', 'H42c', 'H42d', 'H42e',
            'H45a', 'H45b', 'H45c', 'H45d', 'H45e', 'H60a', 'H60b', 'H60c', 'H60d', 'H60e',
            'H62a', 'H62b', 'H62c', 'H62d', 'H62e', 'H91a', 'H91b', 'H91c', 'H91d', 'H91e',
            'H105a', 'H105b', 'H105c', 'H105d', 'H105e', 'angle']

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        res_file = pd.read_csv(sys.argv[1], usecols=col1)

    # removes any lines that don't contain angles
    res_file = res_file[res_file['angle'].str.contains('Packing angle') == False]

    # makes the code column just the pdb code, so that all versions can be combined
    res_file['code'] = res_file['code'].str[:5]

    # angle needs to be converted to a float to be averaged
    res_file['angle'] = res_file['angle'].astype(float)
    aggregation_func = {'angle': 'mean'}

    seq_df = res_file.groupby(['code', 'L38a', 'L38b', 'L38c', 'L38d', 'L38e', 'L40a', 'L40b', 'L40c', 'L40d', 'L40e',
                               'L41a', 'L41b', 'L41c', 'L41d', 'L41e', 'L44a', 'L44b', 'L44c', 'L44d', 'L44e',
                               'L46a', 'L46b', 'L46c', 'L46d', 'L46e', 'L87a', 'L87b', 'L87c', 'L87d', 'L87e',
                               'H33a', 'H33b', 'H33c', 'H33d', 'H33e', 'H42a', 'H42b', 'H42c', 'H42d', 'H42e',
                               'H45a', 'H45b', 'H45c', 'H45d', 'H45e', 'H60a', 'H60b', 'H60c', 'H60d', 'H60e',
                               'H62a', 'H62b', 'H62c', 'H62d', 'H62e', 'H91a', 'H91b', 'H91c', 'H91d', 'H91e',
                               'H105a', 'H105b', 'H105c', 'H105d', 'H105e']).aggregate(aggregation_func)
    seq_df = seq_df.reset_index()
    seq_df['code'] = seq_df['code'].str[:4]
    return seq_df


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

results = remove_duplicates()

results.to_csv('no_duplicates_TScaleData.csv', index=False)
