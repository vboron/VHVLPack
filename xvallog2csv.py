#!/usr/bin/python3

# Program can be run like this:  ./gbr_angle_prediction.py --trainset 'Everything' --testset 'new_data'
# --modelname 'train_Everything_H100G_residues_considered_nosubsampling'
# --graphname 'train_everything_test_abdbnew_nosubsampling'
# # *************************************************************************
import os
import argparse
import encode_res_calc_angles as erca
import nonred
import graphing
from sklearn_methods import *
from sklearn.model_selection import RepeatedKFold


# *************************************************************************
def preprocessing(ds):
    print('Extracting angles and residues, and encoding...')
    encoded_df, ang_df = erca.extract_and_export_packing_residues(
        ds, ds, 'expanded_residues.dat')
    # encoded_df, ang_df = erca.extract_and_export_packing_residues(
    #     ds, ds, '4d.dat')
    print('Nonredundantizing...')
    nonred_df = nonred.NR2(encoded_df, ds, f'{ds}_NR2_expanded_residues')
    # nonred_df = nonred.NR2(encoded_df, ds, f'{ds}_NR2_13res')
    return nonred_df, ang_df


# *************************************************************************
def runGBReg(df: pd.DataFrame, model_name: str, graph_name: str, graph_dir) -> pd.DataFrame:
    if '/' in graph_dir:
        graph_dir = graph_dir.replace('/', '')

    print('Making train and test sets...')
    target_column = {'angle'}
    pdb_code = {'code'}
    predictors = list(OrderedSet(df.columns) - target_column - pdb_code)
    df2 = df[['code', 'angle']]
    print(f'df2:{df2}')
    X = df[predictors].values
    y = df[target_column].values
    df = pd.DataFrame()

    rkf = RepeatedKFold(n_splits=10, n_repeats=1)
    def run_GradientBoostingRegressor_(X_test, y_test, model_name):
        pkl_filename: str = f'{model_name}.pkl'
        with open(pkl_filename, 'rb') as file:
            pickle_model = pickle.load(file)
        y_pred = pickle_model.predict(X_test)
        y_test = y_test.flatten()
        assert len(y_pred) == len(y_test)
        df = pd.DataFrame([y_test, y_pred]).T
        df.columns = ['angle', 'predicted']
        print(f'df={df}')
        return df

    for train_index, test_index in rkf.split(X, y):
        # print(f'fold:{fold}')
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        print('Building ML model...')
        gbr = build_GradientBoostingRegressor_model(X_train, y_train, model_name)
        print('Running ML...')
        # print('X_test', X_test)
        result = run_GradientBoostingRegressor_(X_test, y_test, model_name)
        if 'predicted' not in df.columns:
            df = result
        else:
            df = pd.concat([df, result])
        assert not df.empty
        # print('df after merge:', df)
        # fold += 1
        # print('dataframe:', df)
        # df.to_csv(os.path.join(
        #     graph_dir, f'results_for_{model_name}.csv'), index=False)
    # df2 = df2.groupby('angle').mean('predicted')
    df.reset_index()
    # df=df.groupby(by='angle')
    # print(df)
    final = df2.merge(df, on='angle')
    final.sort_values(by='code')
    print('final:', final)
    # print('Plotting deviance...')
    # plot_deviance(gbr, os.path.join(graph_dir, f'{graph_name}_deviance'), X_test, y_true)
    return final


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
parser.add_argument('--data', required=True,
                    help='directory of pdb files used for training model', type=str)
parser.add_argument('--modelname', required=True,
                    help='name which will be given to the model that is trained', type=str)
parser.add_argument('--graphname', required=True,
                    help='name which will be included in the graphs', type=str)

args = parser.parse_args()

print(f'Preprocessing {args.data}...')
df, angles = preprocessing(args.data)
print('Processing...')
result_df = runGBReg(df, args.modelname,
                     args.graphname, args.data)
# print(result_df)
print('Postprocessing...')
# postprocessing(result_df, args.testset, test_angles, args.graphname)
print('Goodbye!')
