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
import math

# *************************************************************************
def make_group(directory, input_csv, columns, out_name, arff_cols):
    """Create test/train files with test files containing 10% segments of data and the train file the other 90%
    Input:  df          --- .csv file containing the encoded data read as a dataframe
            size        --- the number of data lines that will be
    """
    col1 = [l.strip('\n') for l in open(columns).readlines()]
    df = pd.read_csv(os.path.join(directory, input_csv), usecols=col1)
    size = math.ceil(len(df.index)/10)

    for i, _ in enumerate(df, start=1):
        if i <= 10:
            n_train = f'{out_name}_{i}_train'
            start = size * (i - 1)
            end = start + size + 1
            test_df = df.iloc[start: end]
            train_df = df[~df.isin(test_df)].dropna()
            print(len(train_df.index))
            print(len(test_df.index))
            train_df.to_csv(os.path.join(
                directory, f'{n_train}.csv'), index=False)
            with open(os.path.join(directory, f'{n_train}.arff'), 'w') as f:
                cmd = ['csv2arff', '-v', '-ni', arff_cols, 'angle',
                       os.path.join(directory, f'{n_train}.csv')]
                utils.run_cmd(cmd, False, stdout=f)
            path = os.path.join(directory, f'test_files_{i}')
            os.makedirs(path, exist_ok=True)

            for j, _ in enumerate(test_df.iterrows()):
                row_df = test_df.iloc[j:(j+1)]
                name = row_df['code'].values[0]
                csv_file = os.path.join(path, (name + '.csv'))
                row_df.to_csv(csv_file, index=False)

                with open(os.path.join(path, f'{name}.arff'), 'w') as f:
                    cmd = ['csv2arff', '-v', '-ni',
                           arff_cols, 'angle', csv_file]
                    utils.run_cmd(cmd, False, stdout=f)


# *************************************************************************
# Main
# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for extracting VH/VL relevant residues')
    parser.add_argument(
        '--input_csv', help='File with data to be split', required=True)
    parser.add_argument(
        '--columns', help='Columns to read input file', required=True)
    parser.add_argument(
        '--directory', help='Directory where files will go (dataset dir)', required=True)
    parser.add_argument(
        '--output_tag', help='dataset tag that will come before Test/train_n.csv', required=True)
    parser.add_argument(
        '--csv2arff_cols', help='Input cols for arff conversion', required=True)
    args = parser.parse_args()

    make_group(args.directory, args.input_csv, args.columns, args.output_tag, args.csv2arff_cols)