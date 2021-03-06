#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing


def find_norms_and_outliers(directory, csv_file):
    path_csv_file = os.path.join(directory, csv_file)
    df = pd.read_csv(path_csv_file)

    min_norm = -48
    max_norm = -42

    # extract data where the predicted angle is within the normal range into a new dataframe
    df_normal = df[df['angle'].between(min_norm, max_norm)]

    # extract data where predicted angles are outside of the normal range and add into a new dataframe
    outliers_max = df[df['angle'] >= max_norm]
    outliers_min = df[df['angle'] <= min_norm]

    df_outliers = pd.concat([outliers_max, outliers_min])

    return df_normal, df_outliers


def run_outlier_correction(directory, df_out, first_m, first_c):
    df_out.to_csv(os.path.join(
        directory, 'Everything_NR2_GBReg_out_0.csv'), index=False)
    m = first_m
    c = first_c
    for i in range(1, 6):

        file_name = f'Everything_NR2_GBReg_out_{i}'

        csv_name = f'{file_name}.csv'
        path_name = os.path.join(directory, csv_name)

        cmds = ['./datarot.py', '-o', path_name, '-m', str(m), '-c', str(
            c), '--dataFile', os.path.join(directory, f'Everything_NR2_GBReg_out_{i-1}.csv')]

        utils.run_cmd(cmds, False)
        df = pd.read_csv(path_name)

        # Make table of rotated normal values and the outliers
        df_all = pd.concat([df, df_out])
        corr_norm_out = f'{file_name}_plus_norm.csv'
        df_all.to_csv(os.path.join(directory, corr_norm_out), index=False)

        df['abs_err'] = df['error'].abs()
        df['sqerror'] = df['error'].pow(2)
        df['sq_angle'] = df['angle'].pow(2)
        sum_sqe = df['sqerror'].sum()
        n = df['angle'].count()
        meanabserror = (df['abs_err'].sum())/n
        rmsd = math.sqrt(sum_sqe/n)
        relrmse = utils.relrmse_from_df(df, rmsd)
        # print(df, sum_sqe, n, meanabserror, rmsd, relrmse)

        graphing.error_distribution(
            directory, csv_name, f'error_dist_correction_{i}_out')
        graphing.actual_vs_predicted_from_df(
            df, directory, file_name, file_name)

    return pd.read_csv(os.path.join(directory, 'Everything_NR2_GBReg_out_2.csv'))


def plot_entire_corrected_set(directory, norm_df, out_df):
    df = pd.concat([norm_df, out_df])
    # print(df)
    df = df.reset_index()
    file_name = 'Everything_NR2_GBReg_corrected_all'
    csv_name = f'{file_name}.csv'
    path_name = os.path.join(directory, csv_name)
    df.to_csv(path_name, index=False)
    graphing.normandout_actual_vs_predicted_from_df(
        norm_df, out_df, directory, file_name, file_name)
    graphing.error_distribution(
        directory, csv_name, f'error_dist_correction_all_data')


def two_fold_correction_and_plot(directory, csv_file, slope_m, intercept_c):
    df_norm, df_out = find_norms_and_outliers(directory, csv_file)
    df_out_full = run_outlier_correction(
        directory, df_out, slope_m, intercept_c)
    plot_entire_corrected_set(directory, df_norm, df_out_full)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for applying a rotational correction factor recursively')

    parser.add_argument('--directory', help='Directory', required=True)
    parser.add_argument(
        '-m', help='Slope of best fit line before correction', required=True)
    parser.add_argument(
        '-c', help='Intercept of best fit line before correction', required=True)
    parser.add_argument(
        '--csv_file', help='Uncorrected csv file', required=True)
    args = parser.parse_args()

    two_fold_correction_and_plot(args.directory, args.csv_file, args.m, args.c)
