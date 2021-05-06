#!/usr/bin/python3
"""
Program:    norm_ts
File:       norm_ts.py

Version:    V1.0
Date:       01.05.2021
Function:   Normalize all angles to be between -1 and 1

Description:
============
Program takes the .csv files containing T-Scale encoded residues and angles and normalizes
the angle to be between -1 and 1

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
def read_file():
    """Read the .csv file containing encoded residues and angles

    Return: res_file      --- Dataframe containing encoded residues and angles for VHVL packing

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

    res_file = res_file[res_file['angle'].str.contains('Packing angle') == False]
    return res_file

# *************************************************************************
def normalize(data):
    """Normalize the angles to be betwween -1 and 1

    Return: data      --- Dataframe containing encoded residues and with the normalized angle

    01.05.2021  Original   By: VAB
    """


    norm_angle = []
    max_angle = (data['angle']).astype(float).max()
    min_angle = (data['angle']).astype(float).min()
    print(min_angle)
    range_angle = max_angle - min_angle
    print(range_angle)

    for angle in data['angle']:
        normalized = (float(angle)/range_angle) - (min_angle/range_angle)
        norm_angle.append(normalized)

    data['angle'] = norm_angle

    return data

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

dataframe = read_file()

results = normalize(dataframe)
results.to_csv('norm_angles_ts.csv', index=False)

