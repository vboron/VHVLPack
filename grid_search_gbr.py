#!/usr/bin/env python3
import argparse
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from ordered_set import OrderedSet
import os

def run_gridsearch(directory, file):
    df = pd.read_csv(os.path.join(directory, file))
    target_column = {'angle'}
    pdb_code = {'code'}
    predictors = list(OrderedSet(df.columns) - target_column - pdb_code)
    X = df[predictors].values
    y = df[target_column].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
    GBR = GradientBoostingRegressor()

    gbr_params = {
    'n_estimators': [100,500, 550, 1000,1500],
    'max_depth': [2, 4,6,8,10],
    'min_samples_leaf': [10],
    'learning_rate': [0.01,0.02,0.03,0.04, 0.05, 0.1],
    'subsample': [0.9, 0.5, 0.2, 0.1],
    'random_state': [10, 20, 30, 50, 80, 100, 200, 250, 105],
    'ccp_alpha': [1, 2, 5, 10, 50, 100],
    'alpha': [0, 0.1, 0.2, 0.5, 0.7, 0.8, 0.9, 1]
    }

    grid_GBR = GridSearchCV(estimator=GBR, param_grid = gbr_params, cv = 2, n_jobs=-1)
    grid_GBR.fit(X_train, y_train.ravel())

    print(" Results from Grid Search " )
    print("\n The best estimator across ALL searched params:\n",grid_GBR.best_estimator_)
    print("\n The best score across ALL searched params:\n",grid_GBR.best_score_)
    print("\n The best parameters across ALL searched params:\n",grid_GBR.best_params_)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for applying a rotational correction factor recursively')

    parser.add_argument('--directory', help='Directory', required=True)
    parser.add_argument(
        '--csv_file', help='Uncorrected csv file', required=True)
    args = parser.parse_args()

    run_gridsearch(args.directory, args.csv_file)