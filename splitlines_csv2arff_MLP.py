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
                   3) .csv for training
                   4) .csv file with data to be split for testing
                   5) .dat file with csv2arff inputs
                   6) Name of dataset
------------------------------------------------
"""
import os
import sys
import pandas as pd
import stat
import subprocess
import utils

# *************************************************************************
def make_separate_files():
    """Create .csv files for each pdb
    Input:  df        --- .csv file containing the encoded data read as a dataframe

    17.05.2021  Original   By: VAB
    15.06.2021  Modified   By: VAB
    """

    arff_name = f'{sys.argv[6]}.arff'
    arff_path = os.path.join(directory, arff_name)
    with open(arff_path, 'w') as train_arff:
        args = ['csv2arff', '-v', '-ni', sys.argv[5], 'angle', sys.argv[3]]
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
    df_of_all_data = pd.read_csv(sys.argv[4], usecols=col)
    i = 0
    for row in df_of_all_data.iterrows():
        row_df = df_of_all_data.iloc[i:(i+1)]
        name = row_df['code'].values[0]
        csv_file = os.path.join(path, (name + '.csv'))
        csv_files.append(csv_file)
        row_df.to_csv(csv_file, index=False)
        i += 1

    return csv_files, arff_path

# *************************************************************************
def run_weka(files, train_file):

    classifier='weka.classifiers.functions.MultilayerPerceptron'
    env = {'WEKA': '/usr/local/apps/weka-3-8-3'}
    env['CLASSPATH'] = f'{env["WEKA"]}/weka.jar'

    with open(os.path.join(sys.argv[6], 'testing_data', f'{sys.argv[6]}_train.log'), 'w') as f:
        cmd = ['java', classifier, '-v', '-x', 3, '-H', 20, '-t', train_file, '-d', f'{sys.argv[6]}.model']
        utils.cmd_run(cmd, stdout=f, env=env)

    arff_files = []
    for file in files:
        arff_file = f'{file[:-4]}.arff'
        arff_files.append(arff_file)
        with open(arff_file, 'w') as f:
            try:
                args = ['csv2arff', '-ni', sys.argv[5], 'angle', file]
                subprocess.run(args, stdout=f, stderr=subprocess.DEVNULL)
            except:
                print('Error: file cannot be converted unto arff.')

        with open(os.path.join(sys.argv[6], 'testing_data', f'{file[:-4]}_test.log'), 'w') as f:
            cmd = ['java', classifier, '-v', '-T', arff_file, '-p', 0, '-l', f'{sys.argv[6]}.model']
            utils.run_cmd(cmd, stdout=f, env=env)

# *************************************************************************
# Main
# *************************************************************************

directory = sys.argv[1]

col = [ l.strip('\n') for l in open(sys.argv[2]).readlines() ]

list_of_csv_files, training_file = make_separate_files()

run_weka(list_of_csv_files, training_file)

