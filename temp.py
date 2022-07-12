#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing
from sklearn.ensemble import GradientBoostingRegressor
import pickle


gbr_params = {
    'n_estimators': 550,
    'max_depth': 2,
    'min_samples_leaf': 10,
    'learning_rate': 0.05,
    'subsample': 0.1,
    'random_state': 105
    }

def generate_GBReg_model_everything(directory):
    X_train, y_train, _x_ = utils.make_sets(os.path.join(directory, 'VHVL_res_expanded_toH100G_4d.csv'))
    gbr = GradientBoostingRegressor(**gbr_params).fit(X_train, y_train.ravel())
    # Save to file in the current working directory
    pkl_filename = 'af2clean_trained_gbr_123features.pkl'
    with open(pkl_filename, 'wb') as file:
        pickle.dump(gbr, file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for applying a rotational correction factor recursively')

    parser.add_argument('--directory', help='Directory', required=True)
    args = parser.parse_args()
    generate_GBReg_model_everything(args.directory)

    
