#!/usr/bin/python3
# # *************************************************************************
import os
import argparse
import shutil
import utils
import nonred
import graphing
import gbr_latex as ltp
from multiprocessing import Pool
from sklearn_methods import *

# *************************************************************************


def preprocessing(ds):
    def run_compile_angles(dataset):
        utils.run_cmd(['./compile_angles.py', '--directory', dataset,
                      '--csv_output', f'{dataset}_ang'], False)

    def run_find_VHVLres(dataset):
        utils.run_cmd(['./find_VHVLres.py', '--directory', dataset,
                      '--csv_output', f'{dataset}_res'], False)

    def run_encode_4d(dataset):
        utils.run_cmd(['./encode_4d.py', '--residue_csv', f'{dataset}_res.csv', '--angle_csv', f'{dataset}_ang.csv',
                       '--columns', args.cols_4d, '--csv_output', f'{dataset}_4d', '--directory', f'{dataset}'], False)
    run_compile_angles(ds)
    run_find_VHVLres(ds)
    run_encode_4d(ds)


# *************************************************************************
def run_nr(dataset):
    encoded_csv_path = os.path.join(dataset, f'{dataset}_4d.csv')
    new_file = f'{dataset}_NR2_4d'
    nonred.NR2(encoded_csv_path, args.cols_4d, dataset, new_file)

# *************************************************************************


def runGBReg(trainset, testset):
    X_train, y_train, _x_ = make_sets(
        f'{trainset}/{trainset}_NR2_4d.csv')
    X_test, y_true, df_test = make_sets(
        f'{testset}/{testset}_NR2_4d.csv')
    print(f'Running GBRegressor on {testset}')
    df = run_GradientBoostingRegressor(
        X_train, y_train, X_test, df_test, 'af2clean_trained_gbr_123features')
    df.to_csv(f'{testset}/{testset}_NR2_GBReg.csv', index=False)

# *************************************************************************


def run_graphs(dataset, name):
    cmd = ['./stats2graph.py',
           '--directory', dataset, '--csv_input', f'{name}.csv', '--name_normal',
           f'{name}_normal', '--name_outliers', f'{name}_normal',
           '--name_stats', f'{name}_stats', '--name_graph', name]
    utils.run_cmd(cmd, False)
    graphing.sq_error_vs_actual_angle(
        dataset, f'{name}.csv', f'{name}_sqerror_vs_actual')
    graphing.angle_distribution(
        dataset, f'{dataset}_ang.csv', f'{name}_angledistribution')
    graphing.error_distribution(
        dataset, f'{name}.csv', f'{name}_errordistribution')
    graphing.sq_error_vs_actual_angle(
        dataset, f'{name}.csv', f'{name}_sqerror_vs_actual')


def postprocessing(dataset):
    print(f'Postprocessing {dataset}')
    name = f'{dataset}_NR2_GBReg'
    return run_graphs(dataset, name)


# *************************************************************************
parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--cols-4d', default='4d.dat')
parser.add_argument('--preprocess', action='store_true', default=False)
parser.add_argument('--process', action='store_true', default=False)
parser.add_argument('--postprocess', action='store_true', default=False)
parser.add_argument('--latex', action='store_true', default=False)

args = parser.parse_args()

if not args.preprocess and not args.process and not args.postprocess and not args.latex:
    print('Neither --preprocess nor --process nor --postprocess nor --latex has been specified. Enabling all of them.')
    args.process = args.postprocess = args.latex = True


if args.preprocess:
    def preprocess_nr(dataset):
        print(f'Pre-processing...{dataset}')
        preprocessing(dataset)
        run_nr(dataset)
    preprocess_nr('PostAF2')
    preprocess_nr('PreAF2')
    preprocess_nr('Everything')

if args.process:
    print('Processing...')
    runGBReg('PreAF2', 'PostAF2')
    runGBReg('PreAF2', 'Everything')

if args.postprocess:
    print('Postprocessing...')
    postprocessing('PostAF2')
    postprocessing('Everything')

if args.latex:
    print('Generating LaTeX...')
    ltp.generate_latex('PostAF2', 'Everything', 'GBReg_PostAF2')

print('Goodbye!')
