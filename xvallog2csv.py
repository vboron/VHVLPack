#!/usr/bin/env python3
"""
Function:   Produce a table of statisics from crossvalidated MLP test data.
Description:
============
Program searches for the test log files and extracts the lines containing the statistics like error and RMSE. These
stats are then put into a pandas DataFrame and exported as a .csv file.
------------------------------------------------
"""
import argparse
import pandas as pd
import os
import re

def extract_xval_stats(directory, columns, output_name):

    all_data = []
    files = []

    # Open the directory and make a list of .log files that are in there
    for file in os.listdir(directory):
        if file.endswith("_test.log"):
            files.append(os.path.join(directory, file))

    stats_to_get = ['Correlation coefficient', 'Mean absolute error', 'Root mean squared error',
                    'Total Number of Instances']

    # Open each log file in the directory and find the relevant information
    all_data = []
    for log_file in files:
        with open(log_file) as f:
            stat_lines = []
            lines = f.readlines()
            name = log_file.split('_')[1]
            stat_lines.append(name)
            for line in lines:
                if str(line).strip().startswith(tuple(stats_to_get)):
                    line = re.split('[a-z\\s]+', line, flags=re.IGNORECASE)
                    line = line[1]
                    stat_lines.append(line)
            all_data.append(stat_lines)

    stat_cols = []
    for i in open(columns).readlines():
        i = i.strip('\n')
        stat_cols.append(i)

    df_a = pd.DataFrame(data=all_data, columns=stat_cols)
    path = os.path.join(directory, f'{output_name}.csv')
    df_a.to_csv(path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
    parser.add_argument('--directory', help='Directory where log files are', required=True)
    parser.add_argument('--xval_cols', help='.dat columns for processing xval MLP outputs', required=True)
    parser.add_argument('--out_csv', help='Name for the .csv output', required=True)
    args = parser.parse_args()

    extract_xval_stats(args.directory, args.xval_cols, args.out_csv)