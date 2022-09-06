#!/usr/bin/python3

# Program can be run like this:  ./gbr_angle_prediction.py --trainset 'Everything' --testset 'new_data' 
# --modelname 'train_Everything_H100G_residues_considered_nosubsampling' 
# --graphname 'train_everything_test_abdbnew_nosubsampling'
# # *************************************************************************
import os
import argparse
import shutil
import utils
import encode_res_calc_angles as erca
import nonred
import graphing
from sklearn_methods import *
import numpy as np


# *************************************************************************
def preprocessing(ds):
    print('Extracting angles and residues, and encoding...')
    encoded_df, ang_df = erca.extract_and_export_packing_residues(
        ds, ds, 'expanded_residues.dat')
    print('Nonredundantizing...')
    nonred_df = nonred.NR2(encoded_df, ds, f'{ds}_NR2_expanded_residues')
    return nonred_df, ang_df


# *************************************************************************
def runGBReg(train_df: pd.DataFrame, test_df: pd.DataFrame, model_name: str, graph_name: str, graph_dir) -> pd.DataFrame:
    if '/' in graph_dir:
        graph_dir = graph_dir.replace('/', '')
    print('Making train and test sets...')
    X_train, y_train, _x_, X_test, y_true, df_test = make_reg_sets_from_df(train_df, test_df)
    print('Building ML model...')
    gbr = build_GradientBoostingRegressor_model( X_train, y_train,model_name)
    print('Running ML...')
    df = run_GradientBoostingRegressor(X_test, df_test, model_name)
    df.to_csv(f'results_for_{model_name}.csv', index=False)
    print('Plotting deviance...')
    plot_deviance(gbr, os.path.join(graph_dir, f'{graph_name}_deviance'), X_test, y_true)
    return df


# *************************************************************************
def postprocessing(df, dataset, ang_df, name):
    graphing.actual_vs_predicted_from_df(df, dataset, name, f'{name}_pa')
    graphing.sq_error_vs_actual_angle(
        dataset, df, f'{name}_sqerror_vs_actual')
    graphing.angle_distribution(
        dataset, ang_df, f'{name}_angledistribution')
    graphing.error_distribution(
        dataset, df, f'{name}_errordistribution')


# *************************************************************************
parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--trainset', required=True, help='directory of pdb files used for training model', type=str)
parser.add_argument('--testset', required=True, help='directory of pdb files used for testing model', type=str)
parser.add_argument('--modelname', required=True, help='name which will be given to the model that is trained', type=str)
parser.add_argument('--graphname', required=True, help='name which will be included in the graphs', type=str)
# parser.add_argument('--latex', action='store_true', default=False)

args = parser.parse_args()

# if args.latex:
#     print('Generating LaTeX...')
#     # ltp.generate_latex('PostAF2', 'Everything', 'GBReg_PostAF2')
print(f'Preprocessing {args.trainset}...')
df_train, train_angles = preprocessing(args.trainset)
print(f'Preprocessing {args.testset}...')
df_test, test_angles= preprocessing(args.testset)
print('Processing...')
result_df = runGBReg(df_train, df_test, args.modelname, args.graphname, args.testset)
print(result_df)
print('Postprocessing...')
postprocessing(result_df, args.testset, test_angles, args.graphname)
print('Goodbye!')