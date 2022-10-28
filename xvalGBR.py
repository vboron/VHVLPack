#!/usr/bin/python3


# # *************************************************************************
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
    print('Nonredundantizing...')
    nonred_df = nonred.NR2(encoded_df, ds, f'{ds}_NR2_expanded_residues')
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
        return df

    for train_index, test_index in rkf.split(X, y):
        # print(f'fold:{fold}')
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        print('Building ML model...')
        build_GradientBoostingRegressor_model(X_train, y_train, model_name)
        print('Running ML...')
        result = run_GradientBoostingRegressor_(X_test, y_test, model_name)
        if 'predicted' not in df.columns:
            df = result
        else:
            df = pd.concat([df, result])
        assert not df.empty

    final = df2.merge(df, on='angle')
    final = final.sort_values(by='code')
    final.reset_index()
    final['error'] = final['predicted'] - final['angle']
    path = os.path.join(graph_dir, f'results_{graph_name}.csv')
    final.to_csv(path, index=False)
    return final


# *************************************************************************
def postprocessing(df, dataset, name):
    graphing.actual_vs_predicted_from_df(df, dataset, name, f'{name}_pa')
    graphing.sq_error_vs_actual_angle(
        dataset, df, f'{name}_sqerror_vs_actual')
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
print('Postprocessing...')
postprocessing(result_df, args.data, args.graphname)
print('Goodbye!')
