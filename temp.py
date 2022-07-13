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
    df = pd.read_csv(os.path.join(directory, 'VHVL_res_expanded_toH100G_4d.csv'))
    X_train, y_train, _x_ = sklearn_methods.make_sets_from_df(df)
    X_test, y_true, df_test = sklearn_methods.make_sets_from_df(df)
    df = sklearn_methods.run_GradientBoostingRegressor(X_train, y_train, X_test, df_test, 'af2clean_trained_gbr_123features')
    mean_error = df['error'].abs().mean()
    std = df['error'].std()
    df['sq_angle'] = np.square(df['angle'])
    sum_sq_angles = df['sq_angle'].sum()
    relrmse = std*(len(df)**(1/2))/(sum_sq_angles**(1/2))
    print(f'relrmse:{relrmse}, std: {std}, mean error: {mean_error}')
    df = df.drop(['sq_angle'])

    df.to_csv('testing_123features_gbr.csv', index=False)
    graphing.actual_vs_predicted_from_df(df, 'everything_123features')
    graphing.error_distribution('/', 'testing_123features_gbr.csv', '123features')
    graphing.sq_error_vs_actual_angle('/', 'testing_123features_gbr.csv', '123features')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for applying a rotational correction factor recursively')

    parser.add_argument('--directory', help='Directory', required=True)
    args = parser.parse_args()
    generate_GBReg_model_everything(args.directory)

    
