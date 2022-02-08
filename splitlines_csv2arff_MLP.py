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
import subprocess
import pandas as pd
import utils

# *************************************************************************


def make_separate_files(train_dir, test_dir, cols_4d, train_csv, test_csv, in_cols, trainset, testset):
    """Create .csv files for each pdb
    """

    arff_name = f'{trainset}.arff'
    arff_path = os.path.join(train_dir, arff_name)
    with open(arff_path, 'w') as train_arff:
        cmd = ['csv2arff', '-v', '-ni', in_cols,
               'angle', os.path.join(train_dir, train_csv)]
        utils.run_cmd(cmd, False, stdout=train_arff)

    new_dir = f'{testset}_testing_data'
    path = os.path.join(test_dir, new_dir)
    try:
        os.mkdir(path)
    except:
        print(f'Directory {path} already exists')

    col = [l.strip('\n') for l in open(cols_4d).readlines()]
    csv_files = []
    df_of_all_data = pd.read_csv(os.path.join(test_dir, test_csv), usecols=col)
    i = 0
    for _ in df_of_all_data.iterrows():
        row_df = df_of_all_data.iloc[i:(i+1)]
        name = row_df['code'].values[0]
        csv_file = os.path.join(path, (name + '.csv'))
        csv_files.append(csv_file)
        row_df.to_csv(csv_file, index=False)
        i += 1

    return csv_files, arff_path

# *************************************************************************


def run_weka(files, train_file, in_cols, test_dir, trainset, testset):

    classifier = 'weka.classifiers.functions.MultilayerPerceptron'
    env = {'WEKA': '/usr/local/apps/weka-3-8-3'}
    env['CLASSPATH'] = f'{env["WEKA"]}/weka.jar'

    with open(os.path.join(test_dir, f'{testset}_testing_data', f'{trainset}_train.log'), 'w') as f:
        cmd = ['java', classifier, '-v', '-x', '3', '-H', '20',
               '-t', train_file, '-d', f'{test_dir}/{testset}.model']
        utils.run_cmd(cmd, False, stdout=f, env=env, stderr=subprocess.DEVNULL)

    arff_files = []
    for file in files:
        arff_file = f'{file[:-4]}.arff'
        arff_files.append(arff_file)
        with open(arff_file, 'w') as f:
            cmd = ['csv2arff', '-ni', in_cols, 'angle', file]
            utils.run_cmd(cmd, False, stdout=f)

        with open(f'{file[:-4]}_test.log', 'w') as f:
            cmd = ['java', classifier, '-v', '-T', arff_file,
                   '-p', '0', '-l', f'{test_dir}/{testset}.model']
            utils.run_cmd(cmd, False, stdout=f, env=env,
                          stderr=subprocess.DEVNULL)


# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for extracting VH/VL relevant residues')
    parser.add_argument(
        '--train_dir', help='Directory of training datset', required=True)
    parser.add_argument(
        '--test_dir', help='Directory of testing datset', required=True)
    parser.add_argument(
        '--columns_4d', help='columns for reading encoded file', required=True)
    parser.add_argument(
        '--training_csv', help='.csv file used to train model for MLP', required=True)
    parser.add_argument(
        '--testing_csv', help='.csv file which will be split for testing', required=True)
    parser.add_argument(
        '--input_cols', help='Columns for .csv conversion', required=True)
    parser.add_argument(
        '--train_set', help='Name of set used for training (name+nr)', required=True)
    parser.add_argument(
        '--test_set', help='Name of set used for training (name+nr)', required=True)
    args = parser.parse_args()

    list_of_csv_files, training_file = make_separate_files(args.train_dir, args.test_dir, args.columns_4d,
                                                           args.training_csv, args.testing_csv, args.input_cols,
                                                           args.train_set, args.test_set)

    run_weka(list_of_csv_files, training_file, args.input_cols,
             args.test_dir, args.train_set, args.test_set)
