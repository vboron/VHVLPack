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

    return df_normal, df_outliers

def run_norm_correction(directory, df_normal, first_m, first_c):
    df_normal.to_csv(os.path.join(directory, 'Everything_NR2_GBReg_norm.csv'))
    m = first_m
    c = first_c
    for i in range(1, 6):
        # TODO change name here
        file_name = f'NR2_GBReg_correction_{i}'
        
        csv_name = f'{file_name}.csv'
        path_name = os.path.join(directory, csv_name)

        # TODO fix this line here to work for this case
        cmds = ['./datarot.py', '-o', path_name, '-m', str(m), '-c', str(c), '--dataFile', datafile]

        utils.run_cmd(cmds, False)
        df = pd.read_csv(path_name)
        df['abs_err'] = df['error'].abs()
        df['sqerror'] = df['error'].pow(2)
        df['sq_angle'] = df['angle'].pow(2)
        sum_sqe = df['sqerror'].sum()
        n = df['angle'].count()
        meanabserror = (df['abs_err'].sum())/n
        rmsd = math.sqrt(sum_sqe/n)
        relrmse = utils.calc_relemse(path_name, rmsd)
        # print(df, sum_sqe, n, meanabserror, rmsd, relrmse)

        graphing.error_distribution(directory, csv_name, f'error_dist_correction_{i}')
        m, c = stats2graph.create_stats_and_graph(args.directory, csv_name, file_name, file_name)
        datafile = path_name
        stats = [meanabserror, rmsd, relrmse, m, c]
        stats_df = pd.DataFrame(data=[stats], columns=['meanabserror', 'rmsd', 'relrmse', 'm', 'c'])
        print(stats_df)
