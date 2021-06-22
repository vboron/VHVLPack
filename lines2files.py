#!/usr/bin/env python3
"""
Program:    lines2files
File:       lines2files.py

Version:    V1.0
Date:       15.06.2021
Function:   Split .csv file containing all encoded residues and angles by line into separate .csv files

Description:
============
The program will take take the redundancy reduced .csv file that contains encoded sequence and angles, and
make each row a new .csv file.

Commandline input: 1) encoded and redundancy reduced.csv file
                   2) .dat file with column names
                   3) name of directory where split files will go
--------------------------------------------------------------------------
"""
# *************************************************************************
# Import libraries

import pandas as pd
import sys
import os

# *************************************************************************
def read_csv():
    """Take the .csv file from and the commandline and open it as a datafrane

    Return: file   --- Dataframe of the encoded seq and angles

    17.04.2021  Original   By: VAB
    """
    # The column names contained in the .csv file imported from a .dat file
    col1 = []
    for i in open(sys.argv[2]).readlines():
        i = i.strip('\n')
        col1.append(i)

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        file = pd.read_csv(sys.argv[1], usecols=col1)
    return file


# *************************************************************************
def make_files(df):
    """Create .csv files for each pdb
    Input:  df        --- .csv file containing the encoded data read as a dataframe

    17.05.2021  Original   By: VAB
    15.06.2021  Modified   By: VAB
    """
    try:
        os.mkdir(sys.argv[3])
    except:
        print('Directory not created.')
    cwd = os.getcwd()
    path = '{}/{}/'.format(cwd, sys.argv[3])

    i = 0
    for row in df.iterrows():
        row_df = df.iloc[i:(i+1)]
        name = row_df['code'].values[0]
        row_df.to_csv('{}{}_{}.csv'.format(path, name, i), index=False)
        i += 1
    return


# *************************************************************************
# Main
# *************************************************************************

read = read_csv()

files = make_files(read)
