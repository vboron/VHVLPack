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

def extract_xval_stats(directory, xval_columns, encoded_csv, csv_cols):

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
    for i in open(xval_columns).readlines():
        i = i.strip('\n')
        stat_cols.append(i)

    df_stats_for_each_fold = pd.DataFrame(data=all_data, columns=stat_cols)

    average_coeff=df_stats_for_each_fold['pearson_a'].mean()
    average_error=df_stats_for_each_fold['mean_abs_err_a'].mean()
    average_rmse=df_stats_for_each_fold['RMSE'].mean()
    relrmse=utils.calc_relemse(encoded_csv, csv_cols, str(average_rmse))

    return average_coeff, average_rmse, relrmse, average_error

def make_table_for_graphing(directory, input_csv, input_cols, error, output_name):
    cols = []
    for i in open(input_cols).readlines():
        i = i.strip('\n')
        cols.append(i)

    df=pd.read_csv(os.path.join(directory, input_csv), usecols=cols)
    df_all=df[['code', 'angle']].copy()
    df_all['predicted']=df_all['angle']+error
    df_all['error']=error

    path = os.path.join(directory, output_name)
    df_all.to_csv(path, index=False)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program extracts data from log files of MLP run with cross validation')
    parser.add_argument('--directory', help='Directory where log files are', required=True)
    parser.add_argument('--xval_cols', help='.dat columns for processing xval MLP outputs', required=True)
    parser.add_argument('--out_csv', help='Name for the .csv output', required=True)
    parser.add_argument('--input_csv', help='File that was the input to the method ', required=True)
    parser.add_argument('--cols_4d', help='.dat for 4d columns', required=True)
    args = parser.parse_args()

    mean_pearsons, mean_rmse, relrmse, mean_error= extract_xval_stats(args.directory, args.xval_cols, args.input_csv, args.cols_4d)

    make_table_for_graphing(args.directory, args.input_csv, args.cols_4d, mean_error, args.out_csv)