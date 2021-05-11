#!/usr/bin/python3
"""
Program:    normalize_angles
File:       normalize_angles.py

Version:    V1.0
Date:       01.05.2021
Function:   Normalize all angles to be between -1 and 1

Description:
============
Program takes the .csv files containing encoded residues (in 4d physical parameters)
and angles and normalizes the angle to be between -1 and 1

------------------------------------------------
"""
# *************************************************************************
# Import libraries

import pandas as pd
import sys


# *************************************************************************
def read_file():
    """Read the .csv file containing encoded residues and angles

    Return: res_file      --- Dataframe containing encoded residues and angles for VHVL packing

    01.05.2021  Original   By: VAB
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
        normalized = (float(angle) / range_angle) - (min_angle / range_angle)
        norm_angle.append(normalized)

    data['angle'] = norm_angle

    return data


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

dataframe = read_file()

results = normalize(dataframe)
results.to_csv('norm_{}.csv'.format(sys.argv[3]), index=False)
