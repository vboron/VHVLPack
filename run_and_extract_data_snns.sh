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

Commandline input: 1) Directory where the .seq files are
                   2) .dat file for columns
                   3) File containing angles
                   4) Data tag
------------------------------------------------
"""
import os
import sys
import pandas as pd
import numpy as np
import math
import subprocess

# *************************************************************************
def build_snns_dataframe():

    directory = sys.argv[1]

    col = []
    for i in open(sys.argv[2]).readlines():
        i = i.strip('\n')
        col.append(i)

    seq_files = []
    for file in os.listdir(directory):
        if file.endswith('.seq'):
            code = file[:-4]
            seq_files.append((code, os.path.join(directory, file)))

    df_ang = pd.read_csv(sys.argv[3], usecols=['code', 'angle'])

    p_col = ['code', 'predicted']
    file_data = []
    for code, seq_file in seq_files:
        pred = float(subprocess.check_output(['papa', '-q', seq_file]))
        data = [code, pred]
        file_data.append(data)

    df_pred = pd.DataFrame(data=file_data, columns=p_col)

    df_snns = pd.merge(df_ang, df_pred, how="right", on=["code"], sort=True)
    df_snns = df_snns.dropna()
    df_snns.reset_index

    df_snns['error'] = df_snns['predicted'] - df_snns['angle']
    print(df_snns)
    

    return

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

result = build_snns_dataframe()
result.to_csv('{}.csv'.format(sys.argv[4]), index=False)