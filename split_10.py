#!/usr/bin/python3
"""
Program:    split_10
File:       split_10.py

Version:    V1.0
Date:       17.05.2021
Function:   Split encoded VHVL residue and angle data into 10 train/test sets for 10-fold cross-validation

Description:
============
The program will take take the redundancy reduced .csv file that contains encoded sequence and angles, and split it
into test and train sets (where test sets contain a 10% of the data and the train file the other 90%).

Commandline input: 1) encoded .csv file
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
def calc_group_size(file):
    """Calculate the size of groups the data should be split into

    Input:  file        --- The data frame of encoded residues and angles
    Return: gp_size     --- The number of lines of data that will be in each test/train file

    17.05.2021  Original   By: VAB
    """

    gp_size = (float(len(file.index))/10)
    gp_size = int('{:.0f}'.format(gp_size)) + 1

    return gp_size


# *************************************************************************
def make_group(df, size):
    """Create test/train files with test files containing 10% segments of data and the train file the other 90%
    Input:  df        --- .csv file containing the encoded data read as a dataframe
            size        --- the number of data lines that will be

    17.05.2021  Original   By: VAB
    """
    try:
        os.mkdir(sys.argv[3])
    except:
        print('Directory not created.')
    cwd = os.getcwd()
    path = '{}/{}/'.format(cwd, sys.argv[3])
    i = 1
    for row in df:
        if i <= 10:
            n_test = 'test_{}'.format(i)
            n_train = 'train_{}'.format(i)

            test_df = df.iloc[(size*(i-1)):(size*i)]
            train_df = df[~df.isin(test_df)].dropna()
            train_df.to_csv('{}{}.csv'.format(path, n_train), index=False)
            test_df.to_csv('{}{}.csv'.format(path, n_test), index=False)
            i += 1
    return


# *************************************************************************
# Main
# *************************************************************************

read = read_csv()

groups = calc_group_size(read)

files = make_group(read, groups)
