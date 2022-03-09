#!/usr/bin/env python3

import pandas as pd
from sklearn.neural_network import MLPRegressor
from ordered_set import OrderedSet
from sklearn.datasets import make_regression
from sklearn.ensemble import GradientBoostingRegressor


def make_sets(file):
    df = pd.read_csv(file)
    target_column = {'angle'}
    pdb_code = {'code'}
    predictors = list(OrderedSet(df.columns) - target_column - pdb_code)
    df2 = df[['code', 'angle']]
    X_df = df[predictors].values
    y_df = df[target_column].values
    return X_df, y_df, df2

# X_train, y_train, _x_ = make_sets('PreAF2/PreAF2_NR2_4d.csv')
# X_test, y_true, df_test = make_sets('PostAF2/PostAF2_NR2_4d.csv')

def run_MLPRegressor(X_train, y_train, X_test, df):
    mlp = MLPRegressor(hidden_layer_sizes=15, max_iter=1000).fit(X_train, y_train.ravel())
    y_pred=mlp.predict(X_test)
    y_pred=mlp.predict(X_test)
    df['predicted']=y_pred
    df['error']=df['predicted']-df['angle']
    return df

def run_GradientBoostingRegressor(X_train, y_train, X_test, df):
    gbr = GradientBoostingRegressor().fit(X_train, y_train.ravel())
    y_pred=gbr.predict(X_test)
    df['predicted']=y_pred
    df['error']=df['predicted']-df['angle']
    return df
