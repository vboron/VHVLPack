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

Commandline input: 1) Directory
                   2) .dat file for columns
                   3) .csv file with data
                   4) .dat file with csv2arff inputs
                   5) Name of dataset
------------------------------------------------
"""
import os
import sys
import pandas as pd
import numpy as np
import re
import math
import stat
import subprocess

# *************************************************************************
def make_separate_files():
    """Create .csv files for each pdb
    Input:  df        --- .csv file containing the encoded data read as a dataframe

    17.05.2021  Original   By: VAB
    15.06.2021  Modified   By: VAB
    """

    df_of_all_data = pd.read_csv(sys.argv[3], usecols=col)
    arff_name = '{}.arff'.format(sys.argv[5])
    arff_path = os.path.join(directory, arff_name)
    with open(arff_path, 'w') as train_arff:
        args = ['csv2arff', '-v', '-ni', sys.argv[4], 'angle', sys.argv[3]]
        print(f'Running command: {" ".join(args)}')
        subprocess.run(args, stdout=train_arff, stderr=subprocess.DEVNULL)

    cwd = os.getcwd()
    new_dir = 'testing_data'
    path = os.path.join(cwd, directory, new_dir)
    try:
        os.mkdir(path)
    except:
        print(f'Directory {path} already exists')

    csv_files = []
    i = 0
    for row in df_of_all_data.iterrows():
        row_df = df_of_all_data.iloc[i:(i+1)]
        name = row_df['code'].values[0]
        csv_file = '{}.csv'.format(os.path.join(path, name))
        csv_files.append(csv_file)
        row_df.to_csv(csv_file, index=False)
        i += 1

    return csv_files, arff_path

# *************************************************************************
def run_weka(files, train_file):

    arff_files = []
    for file in files:
        arff_file = f'{file[:-4]}.arff'
        arff_files.append(arff_file)
        with open(arff_file, 'w') as arff_out:
            try:
                args = ['csv2arff', '-ni', sys.argv[4], 'angle', file]
                subprocess.run(args, stdout=arff_out, stderr=subprocess.DEVNULL)
            except:
                print('Error: file cannot be converted unto arff. Check line 60')

    # edit lines in Weka script:
    # DATA=${BASEPATH}/
    # TRAIN=
    # INPUTS=
    name_for_script = 'MLP_for_{}.sh'.format(sys.argv[5])
    name_for_script = os.path.join(directory, name_for_script)
    print(f'Opening {sys.argv[6]}')
    with open(sys.argv[6], 'r+') as weka_script:
        lines = [line.rstrip('\n') for line in weka_script]
        print(f'Writing to {name_for_script}')
        with open(name_for_script, 'w') as script:
            for index, line in enumerate(lines):
                if line.startswith('DATA'):
                    lines[index] += directory
                elif line.startswith('TRAIN'):
                    lines[index] += train_file
                elif line.startswith('INPUTS'):
                    lines[index] += sys.argv[4]
                elif line.startswith('DATASET'):
                    lines[index] += sys.argv[5]
                elif line.startswith('MODEL'):
                    lines[index] += sys.argv[5]

            lines = '\n'.join(lines)
            script.write(lines)
    os.chmod(name_for_script, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC | stat.S_IRGRP | stat.S_IXGRP | stat.S_IWGRP)
    args = ['bash', name_for_script]
    print(f'Running {" ".join(args)}')
    subprocess.run(args)
   
# *************************************************************************
# Main
# *************************************************************************

directory = sys.argv[1]

col = [ l.strip('\n') for l in open(sys.argv[2]).readlines() ]

list_of_csv_files, training_file = make_separate_files()

perform_MLP = run_weka(list_of_csv_files, training_file)

