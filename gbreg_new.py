#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import numpy as np
import utils
import math
import graphing
from sklearn.ensemble import GradientBoostingRegressor
import pickle
import sklearn_methods


gbr_params = {
    'n_estimators': 1500,
    'max_depth': 2,
    'min_samples_leaf': 10,
    'learning_rate': 0.05,
    'subsample': 0.9,
    'random_state': 50
    }

def generate_GBReg_model_everything(directory):
    df_test = pd.read_csv(os.path.join('Everything', 'VHVL_res_expanded_toH100G_4d.csv'))
    df_train = pd.read_csv(os.path.join('PreAF2', 'PreAF2_VHVL_res_expanded_toH100G_4d.csv'))
    X_train, y_train, _x_ = sklearn_methods.make_sets_from_df(df_train)
    X_test, y_true, df_test = sklearn_methods.make_sets_from_df(df_test)
    df = sklearn_methods.run_GradientBoostingRegressor(X_train, y_train, X_test, df_test, 'preaf2_trained_gbr_123features')
    mean_error = df['error'].abs().mean()
    std = df['error'].std()
    df['sq_angle'] = np.square(df['angle'])
    sum_sq_angles = df['sq_angle'].sum()
    relrmse = std*(len(df)**(1/2))/(sum_sq_angles**(1/2))
    print(f'relrmse:{relrmse}, std: {std}, mean error: {mean_error}')
    df.drop(['sq_angle'], axis=1)
    print(df)

    df.to_csv('trainpreaf2_testeverything_123features_gbr.csv', index=False)
    graphing.actual_vs_predicted_from_df(df, './', 'trainpreaf2_testeverything_123features', 'trainpreaf2_testeverything_123features_pa')
    graphing.error_distribution('./', 'trainpreaf2_testeverything_123features_gbr.csv', '123features_err_dist')
    graphing.sq_error_vs_actual_angle('./', 'trainpreaf2_testeverything_123features_gbr.csv', 'trainpreaf2_testeverything_123features_sq_err')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for applying a rotational correction factor recursively')

    parser.add_argument('--directory', help='Directory', required=True)
    args = parser.parse_args()
    generate_GBReg_model_everything(args.directory)

    
