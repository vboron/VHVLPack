#!/usr/bin/env python3

import pandas as pd
from sklearn.neural_network import MLPRegressor
from ordered_set import OrderedSet
# from sklearn.datasets import make_regression
from sklearn.ensemble import GradientBoostingRegressor
import pickle
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import matthews_corrcoef

gbr_params = {'alpha': 0.01,
              # 'ccp_alpha': 0.00001,
              'learning_rate': 0.1,
              'max_depth': 2,
              'min_samples_leaf': 10,
              'n_estimators': 50000,
              'random_state': 100,
              #   'subsample': 0.1,
              #   'loss':'absolute_error',
              'verbose': 1}

gbc_params = {'learning_rate': 0.1,
              'max_depth': 2,
              'min_samples_leaf': 10,
              'n_estimators': 50000,
              'random_state': 100,
              'warm_start': 'True',
              #   'subsample': 0.1,
              #   'loss':'absolute_error',
              'verbose': 1}


def make_sets(df):
    target_column = {'angle'}
    pdb_code = {'code'}
    predictors = list(OrderedSet(df.columns) - target_column - pdb_code)
    df2 = df[['code', 'angle']]
    X_df = df[predictors].values
    y_df = df[target_column].values
    return X_df, y_df, df2


def make_reg_sets_from_df(df_train, df_test):
    def make_set(df):
        target_column = {'angle'}
        pdb_code = {'code'}
        predictors = list(OrderedSet(df.columns) - target_column - pdb_code)
        df2 = df[['code', 'angle']]
        X_df = df[predictors].values
        y_df = df[target_column].values
        return X_df, y_df, df2
    X_train, y_train, code_ang_train = make_set(df_train)
    X_test, y_test, code_ang_test = make_set(df_test)
    return X_train, y_train, code_ang_train, X_test, y_test, code_ang_test

# X_train, y_train, _x_ = make_sets('PreAF2/PreAF2_NR2_4d.csv')
# X_test, y_true, df_test = make_sets('PostAF2/PostAF2_NR2_4d.csv')


def build_MLPRegressor(X_train, y_train, model_name):
    mlp = MLPRegressor(hidden_layer_sizes=15, max_iter=12000).fit(
        X_train, y_train.ravel())
    pkl_filename: str = f'{model_name}.pkl'
    with open(pkl_filename, 'wb') as file:
        pickle.dump(mlp, file)

def build_GradientBoostingRegressor_model(X_train, y_train, model_name):
    gbr = GradientBoostingRegressor(**gbr_params).fit(X_train, y_train.ravel())
    # Save to file in the current working directory
    pkl_filename: str = f'{model_name}.pkl'
    with open(pkl_filename, 'wb') as file:
        pickle.dump(gbr, file)
    return gbr

def run_model(X_test, df: pd.DataFrame, model_name):
    pkl_filename: str = f'{model_name}.pkl'
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    y_pred = pickle_model.predict(X_test)
    df['predicted'] = y_pred
    df['error'] = df['predicted']-df['angle']
    return df

def make_set_class(df):
    target_column = {'class'}
    pdb_code = {'code'}
    predictors = list(OrderedSet(df.columns) - target_column - pdb_code - {'angle'})
    df2 = df[['code', 'class']]
    X_df = df[predictors].values
    y_df = df[target_column].values
    return X_df, y_df, df2

def make_class_sets_from_df(df_train, df_test):
    X_train, y_train, code_class_train = make_set_class(df_train)
    X_test, y_test, code_class_test = make_set_class(df_test)
    return X_train, y_train, code_class_train, X_test, y_test, code_class_test

def build_GradientBoostingClassifier_model(X_train, y_train, model_name):
    gbc = GradientBoostingClassifier(**gbc_params).fit(X_train, y_train.ravel())
    # Save to file in the current working directory
    pkl_filename: str = f'{model_name}.pkl'
    print('Making .pkl file...')
    with open(pkl_filename, 'wb') as file:
        pickle.dump(gbc, file)


def run_GradientBoostingClassifier(X_test, df: pd.DataFrame, model_name):
    pkl_filename: str = f'{model_name}.pkl'
    # Inputted dataframe contains the pdb code and the true value being inputted
    # Load from file
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    y_pred = pickle_model.predict(X_test)
    df['predclass'] = y_pred
    df['result'] = df['predclass'].apply(set) == df['class'].apply(set)
    mcc = matthews_corrcoef(y_true = df['class'], y_pred=df['predclass'])
    print(f'MCC: {mcc}')
    print(df['result'].value_counts())
    print(df['class'].value_counts())
    print(df['predclass'].value_counts())
    df.to_csv('classification_results.csv', index=False)
    return df


def plot_deviance(gbr, graph_name, X_test, y_test):
    test_score = np.zeros((gbr_params["n_estimators"],), dtype=np.float64)
    for i, y_pred in enumerate(gbr.staged_predict(X_test)):
        test_score[i] = gbr.loss_(y_test, y_pred)

    fig = plt.figure(figsize=(6, 6))
    plt.subplot(1, 1, 1)
    plt.title("Deviance")
    plt.plot(
        np.arange(gbr_params["n_estimators"]) + 1,
        gbr.train_score_,
        "b-",
        label="Training Set Deviance")
    plt.plot(np.arange(gbr_params["n_estimators"]) + 1,
             test_score, "r-", label="Test Set Deviance")
    plt.legend(loc="upper right")
    plt.xlabel("Boosting Iterations")
    plt.ylabel("Deviance")
    fig.tight_layout()
    path_fig: str = f'{graph_name}.jpg'
    plt.savefig(path_fig, format='jpg')
    # plt.show()
