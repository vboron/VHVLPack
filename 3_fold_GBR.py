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


def preprocessing(ds, set_name):
    print('Extracting angles and residues, and encoding...')
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

    list_of_dfs = [normal_classed, out_max_classed, out_min_classed]
    list_of_dfs = [df.reset_index() for df in list_of_dfs]
    # print(list_of_dfs)
    df_classed = pd.concat(list_of_dfs, axis=1)
    print(df_classed)
    return df_normal, outliers_max, outliers_min, df_classed


def determine_class(X_train, y_train, X_test, y_true, df_test, set_name):
    print(f'Running GBClassifier on {set_name}')
    df = run_GradientBoostingClassifier(
        X_train, y_train, X_test, df_test, f'gbc_{set_name}')
    df = df.reset_index()
    return class_df


def runGBReg(directory, X_train, y_train, X_test, y_true, df_test, set_name):

    print(f'Running GBRegressor on {set_name}')
    df = run_GradientBoostingRegressor(
        X_train, y_train, X_test, df_test, f'gbr_{set_name}')
    df = df.reset_index()
    # print(df)
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


def three_fold_GBR(train_dir):
    encoded_train_df, train_just_angs_df = preprocessing(
        train_dir, 'Everything')
    # encoded_test_df, test_just_angs_df = preprocessing(test_dir)
    df_norm, df_out_max, df_out_min, classed_df = make_norm_out_dfs(
        encoded_train_df)
    print(df_norm)
    print(classed_df)
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

    parser.add_argument('--directory', help='Directory', required=True)
    args = parser.parse_args()

    three_fold_GBR(args.directory)
