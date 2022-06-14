#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing
import stats2graph


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

    df_outliers.to_csv(os.path.join(directory, 'Everything_NR2_GBReg_out.csv'))
    # print('normal:', df_normal, 'outliers:', df_outliers)
    return df_normal, df_outliers

def run_norm_correction(directory, df_normal, df_out, first_m, first_c):
    df_normal.to_csv(os.path.join(directory, 'Everything_NR2_GBReg_norm_0.csv'), index=False)
    m = first_m
    c = first_c
    for i in range(1, 6):

        file_name = f'Everything_NR2_GBReg_norm_{i}'

        csv_name = f'{file_name}.csv'
        path_name = os.path.join(directory, csv_name)

        cmds = ['./datarot.py', '-o', path_name, '-m', str(m), '-c', str(c), '--dataFile', os.path.join(directory, f'Everything_NR2_GBReg_norm_{i-1}.csv')]

        utils.run_cmd(cmds, False)
        df = pd.read_csv(path_name)

        # Make table of rotated normal values and the outliers 
        df_all = df.concat(df_out)
        corr_norm_out = f'{file_name}_plus_out.csv'
        df_all.to_csv(corr_norm_out, index = False)

        df['abs_err'] = df['error'].abs()
        df['sqerror'] = df['error'].pow(2)
        df['sq_angle'] = df['angle'].pow(2)
        sum_sqe = df['sqerror'].sum()
        n = df['angle'].count()
        meanabserror = (df['abs_err'].sum())/n
        rmsd = math.sqrt(sum_sqe/n)
        relrmse = utils.calc_relemse(path_name, rmsd)
        # print(df, sum_sqe, n, meanabserror, rmsd, relrmse)

        graphing.error_distribution(directory, csv_name, f'error_dist_correction_{i}_norm')
        m, c = stats2graph.create_stats_and_graph(directory, corr_norm_out, file_name, file_name)
        stats = [meanabserror, rmsd, relrmse, m, c]
        stats_df = pd.DataFrame(data=[stats], columns=['meanabserror', 'rmsd', 'relrmse', 'm', 'c'])
        # print(stats_df)
    return pd.read_csv(os.path.join(directory, 'Everything_NR2_GBReg_norm_5.csv')), 

def run_outlier_correction(directory, df_outliers, first_m, first_c):
    m = float(first_m)
    c = float(first_c)
    
    df_outliers['predicted'] = df_outliers['predicted'].apply(lambda x: x * m)
    df_outliers['predicted'] = df_outliers['predicted'] - c

    df_outliers['error'] = df_outliers['predicted'] - df_outliers['angle']

    df_out_just_ape = df_outliers

    file_name = 'Everything_NR2_GBReg_outliers'
    csv_name = f'{file_name}.csv'
    path_name = os.path.join(directory, csv_name)
    df_outliers.to_csv(path_name, index=False)

    # df_outliers['abs_err'] = df_outliers['error'].abs()
    # df_outliers['sqerror'] = df_outliers['error'].pow(2)
    # df_outliers['sq_angle'] = df_outliers['angle'].pow(2)
    # sum_sqe = df_outliers['sqerror'].sum()
    # n = df_outliers['angle'].count()
    # meanabserror = (df_outliers['abs_err'].sum())/n
    # rmsd = math.sqrt(sum_sqe/n)
    # relrmse = utils.calc_relemse(path_name, rmsd)

    graphing.error_distribution(directory, csv_name, f'error_dist_correction_outlier')
    m, c = stats2graph.create_stats_and_graph(directory, csv_name, file_name, file_name)
    # stats = [meanabserror, rmsd, relrmse, m, c]
    # stats_df = pd.DataFrame(data=[stats], columns=['meanabserror', 'rmsd', 'relrmse', 'm', 'c'])
    # print(stats_df)
    print(m, c)
    return df_out_just_ape

def plot_entire_corrected_set(directory, norm_df, out_df):
    df = pd.concat([norm_df, out_df])
    # print(df)
    df = df.reset_index()
    file_name = 'Everything_NR2_GBReg_corrected_all'
    csv_name = f'{file_name}.csv'
    path_name = os.path.join(directory, csv_name)
    df.to_csv(path_name, index=False)
    stats2graph.create_stats_and_graph(directory, csv_name, file_name, file_name)
    graphing.error_distribution(directory, csv_name, f'error_dist_correction_all_data')

def two_fold_correction_and_plot(directory, csv_file, slope_m, intercept_c):
    df_norm, df_out = find_norms_and_outliers(directory, csv_file)
    df_norm_full = run_norm_correction(directory, df_norm, df_out, slope_m, intercept_c)
    df_out_full = run_outlier_correction(directory, df_out, slope_m, slope_m)
    plot_entire_corrected_set(directory, df_norm_full, df_out_full)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for applying a rotational correction factor recursively')
    
    parser.add_argument('--directory', help='Directory', required=True)
    parser.add_argument('-m', help='Slope of best fit line before correction', required=True)
    parser.add_argument('-c', help='Intercept of best fit line before correction', required=True)
    parser.add_argument('--csv_file', help='Uncorrected csv file', required=True)
    args = parser.parse_args()

  
    two_fold_correction_and_plot(args.directory, args.csv_file, args.m, args.c)