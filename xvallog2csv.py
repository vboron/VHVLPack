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
import utils

def extract_xval_stats(directory, columns, output_name, encoded_csv, csv_cols, stat_output):

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
                    line = float(line[1])
                    stat_lines.append(line)
            all_data.append(stat_lines)

    stat_cols = []
    for i in open(columns).readlines():
        i = i.strip('\n')
        stat_cols.append(i)

    df_a = pd.DataFrame(data=all_data, columns=stat_cols)
    path = os.path.join(directory, f'{output_name}.csv')
    df_a.to_csv(path, index=False)

    average_coeff=df_a['pearson_a'].mean()
    average_rmse=df_a['RMSE'].mean()
    relrmse=utils.calc_relemse(encoded_csv, csv_cols, str(average_rmse))
    mean_stats=[average_coeff, average_rmse, relrmse]
    df_stats = pd.DataFrame(data=mean_stats, columns=['mean_pearsons', 'mean_rmse', 'relrmse'])
    path = os.path.join(directory, f'{stat_output}.csv')
    df_stats.to_csv(path, index=False)
    return average_coeff, average_rmse, relrmse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
    parser.add_argument('--directory', help='Directory where log files are', required=True)
    parser.add_argument('--xval_cols', help='.dat columns for processing xval MLP outputs', required=True)
    parser.add_argument('--out_csv', help='Name for the .csv output', required=True)
    parser.add_argument('--input_csv', help='File that was the input to the method ', required=True)
    parser.add_argument('--cols_4d', help='.dat for 4d columns', required=True)
    parser.add_argument('--stats_csv', help='Name for output with mean stats for run', required=True)
    args = parser.parse_args()

    mean_pearsons, mean_rmse, relrmse = extract_xval_stats(args.directory, args.xval_cols, args.out_csv,
                                                           args.input_csv, args.cols_4d, args.stats_csv)
