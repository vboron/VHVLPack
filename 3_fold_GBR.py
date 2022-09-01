#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing
from sklearn_methods import *
import encode_res_calc_angles as erca
import nonred


def preprocessing(ds):
    print('Extracting angles and residues, and encoding...')
    set_name = ds
    if set_name.endswith('/'):
        set_name = set_name.replace('/', '')
    encoded_df, ang_df = erca.extract_and_export_packing_residues(
        ds, set_name, 'expanded_residues.dat')
    print('Nonredundantizing...')
    nonred_df = nonred.NR2(encoded_df, ds, f'{set_name}_NR2_expanded_residues')
    return nonred_df, ang_df


def define_class(df):
    print('Defining class of eeach angle...')

    min_norm = -50
    max_norm = -40

    df['class'] = df['angle']
    df.loc[df['angle'].between(min_norm, max_norm), 'class'] = 'normal'
    df.loc[df['angle'] >= max_norm, 'class'] = 'max_out'
    df.loc[df['angle'] <= min_norm, 'class'] = 'min_out'
    return df


def make_norm_out_dfs(df):
    print('Building split dataframes for regression training...')

    min_norm = -50
    max_norm = -40

    df_normal = df[df['angle'].between(min_norm, max_norm)]
    outliers_max = df[df['angle'] >= max_norm]
    outliers_min = df[df['angle'] <= min_norm]
    return df_normal, outliers_max, outliers_min


def determine_class(X_train, y_train, X_test, y_true, df_test, set_name):
    if set_name.endswith('/'):
        set_name = set_name.replace('/', '')
    print(f'Running GBClassifier on {set_name}')
    build_GradientBoostingClassifier_model(X_train, y_train, f'gbc_{set_name}')
    class_df = run_GradientBoostingClassifier(
        X_test, df_test, f'gbc_{set_name}')
    print(class_df.value_counts())
    return class_df


def run_graphs(directory, set_name, df_all, df_out, df_norm):
    file_name = f'Everything_NR2_GBReg_{set_name}'
    graphing.sq_error_vs_actual_angle(
        directory, f'{file_name}.csv', f'{file_name}_sqerror_vs_actual')
    graphing.angle_distribution(
        directory, f'{directory}_ang.csv', f'{file_name}_angledistribution')
    graphing.error_distribution(
        directory, f'{file_name}.csv', f'{file_name}_errordistribution')

def make_sets_train_model_gbr(df, model_name):
    print('Making GBR training sets...')
    X_train, y_train, _x_ = make_sets(df)
    print(X_train)
    X_train = X_train.drop(['class'], axis=1)
    build_GradientBoostingRegressor_model(X_train, y_train, model_name)


def split_testdata_runGBR(df):
    print('Making GBR test sets...')
    df = df.drop(['class', 'result'], axis=1)
    df_normal = df[df['predclass'] == 'normal']
    outliers_max = df[df['predclass'] == max_out]
    outliers_min = df[df['predclass'] == min_out]

    def make_test_sets_runGBR(df, model_name):
        df = df.drop(['predclass'], axis=1)
        print(f'Making test set for {df}')
        X_test, _x_, angle_df = make_sets(df)
        print(f'Running {model_name} on test set...')
        result_df = run_GradientBoostingRegressor(X_test, angle_df, model_name)
        return result_df

    dir_name = train_dir.replace('/', '')
    norm_result = make_test_sets_runGBR(df_normal, f'norm_class_{dir_name}')
    max_out_result = make_test_sets_runGBR(outliers_max, f'max_out_class_{dir_name}')
    min_out_result = make_test_sets_runGBR(outliers_min, f'min_out_class_{dir_name}')
    df_list = [norm_result, max_out_result, min_out_result]
    print('Making final results dataframe...')
    df_final = pd.concat(df_list)
    return df_final



def three_fold_GBR(train_dir, test_dir):
    encoded_train_df, train_just_angs_df = preprocessing(train_dir)
    encoded_test_df, test_just_angs_df = preprocessing(test_dir)
    train_classed_df = define_class(encoded_train_df)
    test_classed_df = define_class(encoded_test_df)
    X_train_class, y_train_class, _x_, X_test_class, y_test_class, code_class_test_class = make_class_sets_from_df(train_classed_df, test_classed_df)
    pred_class_df = determine_class(X_train_class, y_train_class, X_test_class, y_test_class, test_classed_df, test_dir)
    print(pred_class_df)

    # Train 3 regression models for normal and min/max outliers
    print('Training GBReg models...')
    train_df_norm, train_df_out_max, train_df_out_min = make_norm_out_dfs(encoded_train_df)
    dir_name = train_dir.replace('/', '')
    print(train_df_norm)
    make_sets_train_model_gbr(train_df_norm, f'norm_class_{dir_name}')
    make_sets_train_model_gbr(train_df_out_max, f'max_out_class_{dir_name}')
    make_sets_train_model_gbr(train_df_out_min, f'min_out_class_{dir_name}')
    results = split_testdata_runGBR(pred_class_df)
    print(results)



    # run_graphs(directory, 'all3fold', df_alldata, df_outdata, df_norm)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for applying a rotational correction factor recursively')
    parser.add_argument(
        '--train_directory', help='Directory with files that will be used to train models', required=True)
    parser.add_argument(
        '--test_directory', help='Directory with files that will be used to test models', required=True)
    args = parser.parse_args()

    three_fold_GBR(args.train_directory, args.test_directory)
