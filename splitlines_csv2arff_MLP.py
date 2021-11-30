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
                   3) Name for output .csv
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
    train_arff = '{}.arff'.format(sys.argv[5])
    subprocess.run(['csv2arff', '-v', '-ni', sys.argv[4], 'angle', sys.argv[3], '> {}'.format(train_arff)], 
    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    cwd = os.getcwd()
    new_dir = 'testing_data'
    path = os.path.join(cwd, directory, new_dir)
    try:
        os.mkdir(path)
    except:
        'Directory already exists'
    
    csv_files = []
    i = 0
    for row in df_of_all_data.iterrows():
        row_df = df_of_all_data.iloc[i:(i+1)]
        name = row_df['code'].values[0]
        csv_file = '{}.csv'.format(os.path.join(path, name))
        csv_files.append(csv_file)
        row_df.to_csv(csv_file, index=False)
        i += 1

    return csv_files, train_arff

# *************************************************************************
def run_weka(files, train_file):

    arff_files = []
    for file in files:
        arff_file = '{}.arff'.format(file[:-4])
        arff_files.append(arff_file)
        try:
            subprocess.run(['csv2arff', '-v', '-ni', sys.argv[4], 'angle', file, '> {}'.format(arff_file)], 
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except:
            print('Error: file cannot be converted unto arff. Check line 60')
            raise

    # edit lines in Weka script:
    # DATA=${BASEPATH}/
    # TRAIN=
    # INPUTS=
    name_for_scipt = 'MLP_for_{}.sh'.format(sys.argv[5])
    name_for_scipt = os.path.join(directory, name_for_scipt)
    print(f'Opening {sys.argv[6]}')
    with open(sys.argv[6], 'r+') as weka_script:
        lines = [line.rstrip('\n') for line in weka_script]
        print(f'Writing to {name_for_scipt}')
        with open(name_for_scipt, 'w') as script:
            for index, line in enumerate(lines):
                if line.startswith('DATA'):
                    lines[index] += directory
                elif line.startswith('TRAIN'):
                    lines[index] += train_file
                elif line.startswith('INPUTS'):
                    lines[index] += sys.argv[4]
                elif line.startswith('DATASET'):
                    lines[index] += sys.argv[5]

            lines = '\n'.join(lines)
            script.write(lines)
    os.chmod(name_for_scipt, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC | stat.S_IRGRP | stat.S_IXGRP | stat.S_IWGRP)
    subprocess.run(['bash', name_for_scipt], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    return
   
# *************************************************************************
# Main
# *************************************************************************

directory = sys.argv[1]

col = [ l.strip('\n') for l in open(sys.argv[2]).readlines() ]

list_of_csv_files, training_file = make_separate_files()

perform_MLP = run_weka(list_of_csv_files, training_file)

