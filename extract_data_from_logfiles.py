#!/usr/bin/env python3
"""
Program:    extract_data_from_logfiles
File:       extract_data_from_logfiles.py
Version:    V2.0
Date:       11.23.2021
Function:   Compile the data from .log produced when dataset is run through machine learning model.
Description:
============
Program extracts lines of statistics from .log files produced using MLP through Weka framework and converts them into a
dataframe.

Commandline input: 1) Directory where the .log files are
                   2) .dat file for columns
                   3) Dataset name
------------------------------------------------
"""
import os
import sys
import pandas as pd
import numpy as np
import re
import math

# *************************************************************************
def stats_to_df():
    """ Read the directory and extract .log files. For each log file, extract the predicted angle, actual angle and 
        error, and put into dataframe. Export as a .csv file.

        11.23.2021  Original   By: VAB
    """

    # Take the directory where the .log files are from commandline
    direct = sys.argv[1]
    cwd = os.getcwd()
    # Specify column names for .csv file that will be made from the log files
    col = []
    for i in open(sys.argv[2]).readlines():
        i = i.strip('\n')
        col.append(i)

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
                    all = [code, angle, pred, error]
                    all_data.append(all)


    # Make .csv files for all of the data, splitting it into files that have all the data, only outliers, and only the
    # data withing the 'norm'
    df_a = pd.DataFrame(data=all_data, columns=col)
    path = os.path.join(cwd, direct,f'all_{sys.argv[3]}.csv')
    df_a.to_csv(path, index=False)

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

stats_to_df()