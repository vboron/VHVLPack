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

import utils

# *************************************************************************
def calc_group_size(directory, input_csv, columns):
    """Calculate the size of groups the data should be split into

    Input:  file        --- The data frame of encoded residues and angles
    Return: gp_size     --- The number of lines of data that will be in each test/train file
    """
    col1 = [l.strip('\n') for l in open(columns).readlines()]
    file = pd.read_csv(os.path.join(directory, input_csv), usecols=col1)

    gp_size = len(file.index)//10
    return file, gp_size

# *************************************************************************
def make_group(directory, df, size, out_name, arff_cols):
    """Create test/train files with test files containing 10% segments of data and the train file the other 90%
    Input:  df          --- .csv file containing the encoded data read as a dataframe
            size        --- the number of data lines that will be
    """
    i = 1
    for _ in df:
        if i <= 10:
            n_test = f'{out_name}_{i}_test'
            n_train = f'{out_name}_{i}_train'

            test_df = df.iloc[(size * (i - 1)):(size * i)]
            train_df = df[~df.isin(test_df)].dropna()
            train_df.to_csv(os.path.join(directory, f'{n_train}.csv'), index=False)
            with open(os.path.join(directory, f'{n_train}.arff'), 'w') as f:
                cmd = ['csv2arff', '-v', '-ni', arff_cols, 'angle', os.path.join(directory, f'{n_train}.csv')]
                utils.run_cmd(cmd, False, stdout=f)

            test_df.to_csv(os.path.join(directory, f'{n_test}.csv'), index=False)
            with open(os.path.join(directory, f'{n_test}.arff'), 'w') as f:
                cmd = ['csv2arff', '-v', '-ni', arff_cols, 'angle', os.path.join(directory, f'{n_test}.csv')]
                utils.run_cmd(cmd, False, stdout=f)
            i += 1


# *************************************************************************
# Main
# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
    parser.add_argument('--input_csv', help='File with data to be split', required=True)
    parser.add_argument('--columns', help='Columns to read input file', required=True)
    parser.add_argument('--directory', help='Directory where files will go (dataset dir)', required=True)
    parser.add_argument('--output_tag', help='dataset tag that will come before Test/train_n.csv', required=True)
    parser.add_argument('--csv2arff_cols', help='Input cols for arff conversion', required=True)
    args = parser.parse_args()

    data, groups = calc_group_size(args.directory, args.input_csv, args.columns)
    make_group(args.directory, data, groups, args.output_tag, args.csv2arff_cols)