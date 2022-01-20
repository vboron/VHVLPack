#!/usr/bin/python3
"""
Function:   Split encoded VHVL residue and angle data into 10 train/test sets for 10-fold cross-validation

Description:
============
The program will take take the redundancy reduced .csv file that contains encoded sequence and angles, and split it
into test and train sets (where test sets contain a 10% of the data and the train file the other 90%).
--------------------------------------------------------------------------
"""
# *************************************************************************
# Import libraries

import argparse
import pandas as pd
import os

# *************************************************************************
def calc_group_size(input_csv, columns):
    """Calculate the size of groups the data should be split into

    Input:  file        --- The data frame of encoded residues and angles
    Return: gp_size     --- The number of lines of data that will be in each test/train file

    17.05.2021  Original   By: VAB
    """
    col1 = []
    for i in open(columns).readlines():
        i = i.strip('\n')
        col1.append(i)

    file = pd.read_csv(input_csv, usecols=col1)

    gp_size = (float(len(file.index))/10)
    gp_size = int('{:.0f}'.format(gp_size)) + 1

    return file, gp_size


# *************************************************************************
def make_group(directory, df, size, out_name):
    """Create test/train files with test files containing 10% segments of data and the train file the other 90%
    Input:  df        --- .csv file containing the encoded data read as a dataframe
            size        --- the number of data lines that will be

    17.05.2021  Original   By: VAB
    """
    i = 1
    for row in df:
        if i <= 10:
            n_test = f'{out_name}_test_{i}'
            n_train = f'{out_name}_train_{i}'

            test_df = df.iloc[(size*(i-1)):(size*i)]
            train_df = df[~df.isin(test_df)].dropna()
            train_df.to_csv(os.path.join(directory, f'{n_train}.csv'), index=False)
            test_df.to_csv(os.path.join(directory, f'{n_test}.csv'), index=False)
            i += 1
    return


# *************************************************************************
# Main
# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
    parser.add_argument('--input_csv', help='File with data to be split', required=True)
    parser.add_argument('--columns', help='Columns to read input file', required=True)
    parser.add_argument('--directory', help='Directory where files will go (dataset dir)', required=True)
    parser.add_argument('--output_tag', help='dataset tag that will come before Test/train_n.csv', required=True)
    args = parser.parse_args()

    data, groups = calc_group_size(args.input_csv, args.columns)

    files = make_group(args.directory, data, groups, args.output_tag)