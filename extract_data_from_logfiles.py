#!/usr/bin/env python3
"""
Function:   Compile the data from .log produced when dataset is run through machine learning model.
Description:
============
Program extracts lines of statistics from .log files produced using MLP through Weka framework and converts them into a
dataframe.
------------------------------------------------
"""
import os
import pandas as pd
import re
import argparse

# *************************************************************************
def stats_to_df(direct, csv_out):
    """ Read the directory and extract .log files. For each log file, extract the predicted angle, actual angle and
        error, and put into dataframe. Export as a .csv file.

        11.23.2021  Original   By: VAB
    """

    all_data = []
    files = []

    # Open the directory and make a list of .log files that are in there
    for file in os.listdir(direct):
        if file.endswith("test.log"):
            files.append(os.path.join(direct, file))

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


    # Make .csv files for all of the data, splitting it into files that have all the data, only outliers, and only the
    # data withing the 'norm'
    df_a = pd.DataFrame(data=all_data)
    df_a.to_csv(f'{csv_out}.csv', index=False)

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
    parser.add_argument('--directory', help='Directory where log files are', required=True)
    parser.add_argument('--output_name', help='name for .csv file for data ', required=True)
    args = parser.parse_args()

    stats_to_df(args.directory, args.output_name)