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

    min_norm = -53
    max_norm = -37

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


def combine_dfs(directory, list_of_dfs, df2csv_name):
    file_name = os.path.join(
        directory, f'Everything_NR2_GBReg_{df2csv_name}.csv')
    df = pd.concat(list_of_dfs)
    df = df.reset_index()
    df.to_csv(file_name, index=False)
    return df


def run_graphs(directory, set_name, df_all, df_out, df_norm):
    file_name = f'Everything_NR2_GBReg_{set_name}'
    # cmd = ['./stats2graph.py',
    #        '--directory', directory, '--csv_input', csv, '--name_stats', f'{file_name}_stats', '--name_graph', file_name]
    # utils.run_cmd(cmd, False)
    stats_all, stats_out = stats2graph.find_stats(
        directory, f'{file_name}.csv', df_all, df_out)
    stats2graph.plot_scatter(directory, df_out, df_norm,
                             stats_all, stats_out, df_all, file_name, file_name)
    graphing.sq_error_vs_actual_angle(
        directory, f'{file_name}.csv', f'{file_name}_sqerror_vs_actual')
    graphing.angle_distribution(
        directory, f'{directory}_ang.csv', f'{file_name}_angledistribution')
    graphing.error_distribution(
        directory, f'{file_name}.csv', f'{file_name}_errordistribution')
    graphing.sq_error_vs_actual_angle(
        directory, f'{file_name}.csv', f'{file_name}_sqerror_vs_actual')


def three_fold_GBR(directory, csv_file):
    df_norm, df_out_max, df_out_min = make_norm_out_dfs(directory, csv_file)
    runGBReg(directory, df_norm, 'norm')
    runGBReg(directory, df_out_max, 'out_max')
    runGBReg(directory, df_out_min, 'out_min')
    df_alldata = combine_dfs(
        directory, [df_norm, df_out_max, df_out_min], 'all3fold')
    df_outdata = combine_dfs(
        directory, [df_out_max, df_out_min], 'outliers3fold')
    run_graphs(directory, 'all_3fold', df_alldata, df_outdata, df_norm)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for applying a rotational correction factor recursively')

    parser.add_argument('--directory', help='Directory', required=True)
    parser.add_argument(
        '--csv_file', help='Uncorrected csv file', required=True)
    args = parser.parse_args()

    three_fold_GBR(args.directory, args.csv_file)
