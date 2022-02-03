#!/usr/bin/env python3
"""
Function:   Produce a table of statisics from crossvalidated MLP test data.
Description:
============
Program searches for the test log files and extracts the lines containing the statistics like error and RMSE. These
stats are then put into a pandas DataFrame and exported as a .csv file.
------------------------------------------------
"""
import os
import pandas as pd
import re
import argparse

# *************************************************************************
def stats_to_df(direct, columns, csv_out):
    """ Read the directory and extract .log files. For each log file, extract the predicted angle, actual angle and
        error, and put into dataframe. Export as a .csv file.

        11.23.2021  Original   By: VAB
    """

    # Specify column names for .csv file that will be made from the log files
    col = []
    for i in open(columns).readlines():
        i = i.strip('\n')
        col.append(i)

    all_data = []
    files = []

    # Open the directory and make a list of .log files that are in there
    for i in range (1, 11):
        test_dir = f'test_files_{i}'
        test_dir_path = os.path.join(direct, test_dir)
        for file in os.listdir(test_dir_path):
            if file.endswith(".log"):
                files.append(os.path.join(test_dir_path, file))

    # Open each log file in the directory and find the relevant information
    for log_file in files:
        with open(log_file) as text_file:
            for line in text_file:
                if str(line).strip().startswith('1'):
                    line = re.sub(' +', ' ', line)
                    line = line.strip()
                    line_list = line.split(' ')
                    name = log_file.split('/')
                    name = name[-1]
                    code = name[:6]
                    pred = float(line_list[2])
                    angle = float(line_list[1])
                    error = float(line_list[3])
                    _all_ = [code, angle, pred, error]
                    all_data.append(_all_)

    df_a = pd.DataFrame(data=all_data, columns=col)
    df_a.to_csv(f'{csv_out}.csv', index=False)

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
    parser.add_argument('--directory', help='Directory where log files are', required=True)
    parser.add_argument('--columns_postprocessing', help='Columns for postprocessing', required=True)
    parser.add_argument('--output_name', help='name for .csv file for data ', required=True)
    args = parser.parse_args()

    stats_to_df(args.directory, args.columns_postprocessing, args.output_name)