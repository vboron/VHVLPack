#!/usr/bin/env python3
"""
Function:   Compile the data from .log produced when dataset is run through machine learning model.
Description:
============
Program extracts lines of statistics from .log files produced using MLP through Weka framework and converts them into a
dataframe.
------------------------------------------------
"""
import argparse
import os
import pandas as pd
import subprocess
import utils

# *************************************************************************
def make_separate_files(directory, cols_4d, train_csv, test_csv, in_cols):
    """Create .csv files for each pdb

    17.05.2021  Original   By: VAB
    15.06.2021  Modified   By: VAB
    """

    arff_name = f'{directory}.arff'
    arff_path = os.path.join(directory, arff_name)
    with open(arff_path, 'w') as train_arff:
        cmd = ['csv2arff', '-v', '-ni', in_cols, 'angle', train_csv]
        print(f'Running command: {" ".join(cmd)}')
        subprocess.run(cmd, stdout=train_arff, stderr=subprocess.DEVNULL)

    cwd = os.getcwd()
    new_dir = 'testing_data'
    path = os.path.join(cwd, directory, new_dir)
    try:
        os.mkdir(path)
    except:
        print(f'Directory {path} already exists')

    col = [l.strip('\n') for l in open(cols_4d).readlines()]
    csv_files = []
    df_of_all_data = pd.read_csv(test_csv, usecols=col)
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
def run_weka(files, train_file, in_cols, dataset):

    classifier='weka.classifiers.functions.MultilayerPerceptron'
    env = {'WEKA': '/usr/local/apps/weka-3-8-3'}
    env['CLASSPATH'] = f'{env["WEKA"]}/weka.jar'

    with open(os.path.join(dataset, 'testing_data', f'{dataset}_train.log'), 'w') as f:
        cmd = ['java', classifier, '-v', '-x', 3, '-H', 20, '-t', train_file, '-d', f'{dataset}.model']
        utils.cmd_run(cmd, stdout=f, env=env)

    arff_files = []
    for file in files:
        arff_file = f'{file[:-4]}.arff'
        arff_files.append(arff_file)
        with open(arff_file, 'w') as f:
            try:
                cmd = ['csv2arff', '-ni', in_cols, 'angle', file]
                subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL)
            except:
                print('Error: file cannot be converted unto arff.')

        with open(os.path.join(dataset, 'testing_data', f'{file[:-4]}_test.log'), 'w') as f:
            cmd = ['java', classifier, '-v', '-T', arff_file, '-p', 0, '-l', f'{dataset}.model']
            utils.run_cmd(cmd, stdout=f, env=env)


# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
    parser.add_argument('--directory', help='Directory of datset', required=True)
    parser.add_argument('--columns_4d', help='Directory where .seq files are', required=True)
    parser.add_argument('--training_csv', help='.csv file used to train model for MLP', required=True)
    parser.add_argument('--testing_csv', help='.csv file which will be split for testing', required=True)
    parser.add_argument('--input_cols', help='Columns for .csv conversion', required=True)
    args = parser.parse_args()

    list_of_csv_files, training_file = make_separate_files(args.directory, args.columns_4d, args.train_csv,
                                                           args.testing_csv, args.input_cols)

    run_weka(list_of_csv_files, training_file, args.input_cols, args.directory)