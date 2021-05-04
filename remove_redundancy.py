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

------------------------------------------------
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

    Return: seq_df      --- Dataframe that contains the PDB codes of files that have the same VHVl sequences and
    angles.

    01.05.2021  Original   By: VAB
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

    # remove lines that don't contain angles
    res_file = res_file[res_file['angle'].str.contains('Packing angle') == False]

    # angle needs to be converted to a float
    res_file['angle'] = res_file['angle'].astype(float)
    res_file['angle'] = res_file['angle'].round()

    # make a list of all combined pdb names separated by commas and add them as a value
    agg_func = {'code': ', '.join}

    seq_df = res_file.groupby(['L38a', 'L38b', 'L38c', 'L38d', 'L38e', 'L40a', 'L40b', 'L40c', 'L40d', 'L40e',
                               'L41a', 'L41b', 'L41c', 'L41d', 'L41e', 'L44a', 'L44b', 'L44c', 'L44d', 'L44e',
                               'L46a', 'L46b', 'L46c', 'L46d', 'L46e', 'L87a', 'L87b', 'L87c', 'L87d', 'L87e',
                               'H33a', 'H33b', 'H33c', 'H33d', 'H33e', 'H42a', 'H42b', 'H42c', 'H42d', 'H42e',
                               'H45a', 'H45b', 'H45c', 'H45d', 'H45e', 'H60a', 'H60b', 'H60c', 'H60d', 'H60e',
                               'H62a', 'H62b', 'H62c', 'H62d', 'H62e', 'H91a', 'H91b', 'H91c', 'H91d', 'H91e',
                               'H105a', 'H105b', 'H105c', 'H105d', 'H105e', 'angle']).aggregate(agg_func)
    seq_df = seq_df.reset_index()

    # columns were re-ordered so that the PDB code would be first
    reorder_col = ['code', 'L38a', 'L38b', 'L38c', 'L38d', 'L38e', 'L40a', 'L40b', 'L40c', 'L40d', 'L40e',
                   'L41a', 'L41b', 'L41c', 'L41d', 'L41e', 'L44a', 'L44b', 'L44c', 'L44d', 'L44e',
                   'L46a', 'L46b', 'L46c', 'L46d', 'L46e', 'L87a', 'L87b', 'L87c', 'L87d', 'L87e',
                   'H33a', 'H33b', 'H33c', 'H33d', 'H33e', 'H42a', 'H42b', 'H42c', 'H42d', 'H42e',
                   'H45a', 'H45b', 'H45c', 'H45d', 'H45e', 'H60a', 'H60b', 'H60c', 'H60d', 'H60e',
                   'H62a', 'H62b', 'H62c', 'H62d', 'H62e', 'H91a', 'H91b', 'H91c', 'H91d', 'H91e',
                   'H105a', 'H105b', 'H105c', 'H105d', 'H105e', 'angle']
    seq_df = seq_df[reorder_col]
    seq_df = seq_df.sort_values('code')

    return seq_df


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

results = remove_duplicates()

# export dataframe as a .csv file and don't include the line indices
results.to_csv('no_red_ts.csv', index=False)
