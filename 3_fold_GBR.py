#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing
import stats2graph
from sklearn_methods import *


def test(directory, csv_file):
    path_csv_file = os.path.join(directory, csv_file)
    df = pd.read_csv(path_csv_file)

    min_norm = -48
    max_norm = -42

    # extract data where the predicted angle is within the normal range into a new dataframe
    df_normal = df[df['angle'].between(min_norm, max_norm)]

    # extract data where predicted angles are outside of the normal range and add into a new dataframe
    outliers_max = df[df['angle'] >= max_norm]
    outliers_min = df[df['angle'] <= min_norm]

    # df_outliers = pd.concat([outliers_max, outliers_min])

    # df_outliers.to_csv(os.path.join(directory, 'Everything_NR2_GBReg_out.csv'))
    # print('normal:', df_normal, 'outliers:', df_outliers)
    print(df_normal, outliers_max, outliers_min)

def runGBReg(directory, df, set_name):
    X_train, y_train, _x_ = make_sets_from_df(df)
    X_test, y_true, df_test = make_sets(df)
    print(f'Running GBRegressor on {set_name}')
    df = run_GradientBoostingRegressor(
        X_train, y_train, X_test, df_test, f'gbr_{set_name}')
    df.to_csv(f'{directory}/Everything_NR2_GBReg_{set}.csv', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for applying a rotational correction factor recursively')

    parser.add_argument('--directory', help='Directory', required=True)
    parser.add_argument('--csv_file', help='Uncorrected csv file', required=True)
    args = parser.parse_args()
    test(args.directory, args.csv_file)