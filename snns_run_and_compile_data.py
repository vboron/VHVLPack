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
                   5) Which papa version is being called
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

    seq_files = []
    for file in os.listdir(directory):
        if file.endswith('.seq'):
            code = file[:-4]
            seq_files.append((code, os.path.join(directory, file)))

    df_ang = pd.read_csv(sys.argv[3], usecols=['code', 'angle'])

    p_col = ['code', 'predicted']
    file_data = []
    for code, seq_file in seq_files:
        pred = float(subprocess.check_output([sys.argv[5], '-q', seq_file]))
        data = [code, pred]
        file_data.append(data)

    df_pred = pd.DataFrame(data=file_data, columns=p_col)

    df_snns = pd.merge(df_ang, df_pred, how="right", on='code', sort=False)
    df_snns = df_snns.dropna()
    df_snns.reset_index()

    df_snns['error'] = df_snns['predicted'] - df_snns['angle']
    
    return df_snns

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
directory = sys.argv[1]

col = []
for i in open(sys.argv[2]).readlines():
    i = i.strip('\n')
    col.append(i)
path = os.path.join(directory, (sys.argv[4] + '.csv'))

result = build_snns_dataframe()
result.to_csv(path, index=False)