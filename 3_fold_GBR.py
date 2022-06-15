#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing
import stats2graph
from sklearn_methods import *


def make_norm_out_dfs(directory, csv_file):
    path_csv_file = os.path.join(directory, csv_file)
    df = pd.read_csv(path_csv_file)

    min_norm = -48
    max_norm = -42

    # extract data where the predicted angle is within the normal range into a new dataframe
    df_normal = df[df['angle'].between(min_norm, max_norm)]

    # extract data where predicted angles are outside of the normal range and add into a new dataframe
    outliers_max = df[df['angle'] >= max_norm]
    outliers_min = df[df['angle'] <= min_norm]

    return df_normal, outliers_max, outliers_min


def runGBReg(directory, df, set_name):
    X_train, y_train, _x_ = make_sets_from_df(df)
    X_test, y_true, df_test = make_sets_from_df(df)
    print(f'Running GBRegressor on {set_name}')
    df = run_GradientBoostingRegressor(
        X_train, y_train, X_test, df_test, f'gbr_{set_name}')
    df = df.reset_index()
    # print(df)
    df.to_csv(f'{directory}/Everything_NR2_GBReg_{set_name}.csv', index=False)

def combine_all_post_3fold_data(directory, df_norm, df_out_max, df_out_min):
    file_name = os.path.join(directory, f'Everything_NR2_GBReg_all_3fold.csv')
    df = pd.concat([df_norm, df_out_max, df_out_min])
    df = df.reset_index()
    df.to_csv(file_name, index=False)

def run_graphs(directory, set_name, csv):
    file_name = f'Everything_NR2_GBReg_{set_name}'
    cmd = ['./stats2graph.py',
           '--directory', directory, '--csv_input', csv, '--name_stats', f'{file_name}_stats', '--name_graph', file_name]
    utils.run_cmd(cmd, False)
    graphing.sq_error_vs_actual_angle(
        directory, f'{file_name}.csv', f'{file_name}_sqerror_vs_actual')
    graphing.angle_distribution(
        directory, f'{directory}_ang.csv', f'{file_name}_angledistribution')
    graphing.error_distribution(
        directory, f'{file_name}.csv', f'{file_name}_errordistribution')
    graphing.sq_error_vs_actual_angle(
        directory, f'{file_name}.csv', f'{file_name}_sqerror_vs_actual')


def run_GBR_graph(directory, df, set_name, csv):
    runGBReg(directory, df, set_name)
    run_graphs(directory, set_name, csv)


def three_fold_GBR(directory, csv_file):
    df_norm, df_out_max, df_out_min = make_norm_out_dfs(directory, csv_file)
    run_GBR_graph(directory, df_norm, 'norm', csv_file)
    run_GBR_graph(directory, df_out_max, 'out_max', csv_file)
    run_GBR_graph(directory, df_out_min, 'out_min', csv_file)
    combine_all_post_3fold_data(directory, df_norm, df_out_max, df_out_min)
    run_graphs(directory, 'all_3fold', csv_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for applying a rotational correction factor recursively')

    parser.add_argument('--directory', help='Directory', required=True)
    parser.add_argument(
        '--csv_file', help='Uncorrected csv file', required=True)
    args = parser.parse_args()

    three_fold_GBR(args.directory, args.csv_file)
