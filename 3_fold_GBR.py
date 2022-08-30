#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing
from sklearn_methods import *
import encode_res_calc_angles as erca
import nonred


def preprocessing(ds):
    print('Extracting angles and residues, and encoding...')
    set_name = ds
    if set_name.endswith('/'):
        set_name = set_name.replace('/', '')
    encoded_df, ang_df = erca.extract_and_export_packing_residues(
        ds, set_name, 'expanded_residues.dat')
    print('Nonredundantizing...')
    nonred_df = nonred.NR2(encoded_df, ds, f'{set_name}_NR2_expanded_residues')
    return nonred_df, ang_df


def combine_dfs(list_of_dfs):
    # dfs = [df.set_index('code') for df in list_of_dfs]

    return df


def make_norm_out_dfs(df):
    min_norm = -50
    max_norm = -40

    def add_class(df, class_name):
        df['class'] = class_name
        return df

    # extract data where the predicted angle is within the normal range into a new dataframe
    df_normal = df[df['angle'].between(min_norm, max_norm)]
    normal_classed = add_class(df_normal, 'normal')

    # extract data where predicted angles are outside of the normal range and add into a new dataframe
    outliers_max = df[df['angle'] >= max_norm]
    out_max_classed = add_class(outliers_max, 'max_out')

    outliers_min = df[df['angle'] <= min_norm]
    out_min_classed = add_class(outliers_min, 'min_out')

    df_classed = pd.concat([normal_classed, out_max_classed, out_min_classed])
    return df_normal, outliers_max, outliers_min, df_classed


def determine_class(X_train, y_train, X_test, y_true, df_test, set_name):
    if set_name.endswith('/'):
        set_name = set_name.replace('/', '')
    print(f'Running GBClassifier on {set_name}')
    build_GradientBoostingClassifier_model(X_train, y_train, f'gbc_{set_name}')
    class_df = run_GradientBoostingClassifier(X_test, df_test, f'gbc_{set_name}')
    print(class_df)
    return class_df


def runGBReg(directory, X_train, y_train, X_test, y_true, df_test, set_name):
    print(f'Running GBRegressor on {set_name}')
    df = run_GradientBoostingRegressor(
        X_train, y_train, X_test, df_test, f'gbr_{set_name}')
    df = df.reset_index()
    path = os.join(directory, f'NR2_GBReg_{set_name}.csv')
    df.to_csv(path, index=False)


def run_graphs(directory, set_name, df_all, df_out, df_norm):
    file_name = f'Everything_NR2_GBReg_{set_name}'
    graphing.sq_error_vs_actual_angle(
        directory, f'{file_name}.csv', f'{file_name}_sqerror_vs_actual')
    graphing.angle_distribution(
        directory, f'{directory}_ang.csv', f'{file_name}_angledistribution')
    graphing.error_distribution(
        directory, f'{file_name}.csv', f'{file_name}_errordistribution')


def three_fold_GBR(train_dir, test_dir):
    encoded_train_df, train_just_angs_df = preprocessing(train_dir)
    encoded_test_df, test_just_angs_df = preprocessing(test_dir)
    train_df_norm, train_df_out_max, train_df_out_min, train_classed_df = make_norm_out_dfs(encoded_train_df)
    test_df_norm, test_df_out_max, test_df_out_min, test_classed_df = make_norm_out_dfs(encoded_train_df)
    print(test_classed_df)
    X_train_class, y_train_class, _x_, X_test_class, y_test_class, code_class_test_class = make_class_sets_from_df(train_classed_df, test_classed_df)
    determine_class(X_train_class, y_train_class, X_test_class, y_test_class, code_class_test_class, test_dir)
    # runGBReg(directory, df_norm, 'norm')
    # runGBReg(directory, df_out_max, 'out_max')
    # runGBReg(directory, df_out_min, 'out_min')
    # df_alldata = combine_dfs(
    #     directory, [df_norm, df_out_max, df_out_min], 'all3fold')
    # df_outdata = combine_dfs(
    #     directory, [df_out_max, df_out_min], 'outliers3fold')
    # run_graphs(directory, 'all3fold', df_alldata, df_outdata, df_norm)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for applying a rotational correction factor recursively')
    parser.add_argument('--train_directory', help='Directory with files that will be used to train models', required=True)
    parser.add_argument('--test_directory', help='Directory with files that will be used to test models', required=True)
    args = parser.parse_args()

    three_fold_GBR(args.train_directory, args.test_directory)
