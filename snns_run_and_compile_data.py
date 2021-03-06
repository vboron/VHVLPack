#!/usr/bin/env python3
"""
Function:   Compile the data from .log produced when dataset is run through machine learning model.
Description:
============
Program extracts lines of statistics from .log files produced using MLP through Weka framework and converts them into a
dataframe.

------------------------------------------------
"""
import argparse
import os
import pandas as pd
import subprocess

# *************************************************************************
def build_snns_dataframe(directory, seq_directory, angle_file, papa_version):
    seq_files = []
    for file in os.listdir(seq_directory):
        if file.endswith('.seq'):
            code = file[:-4]
            seq_files.append((code, os.path.join(seq_directory, file)))

    df_ang = pd.read_csv(os.path.join(directory, angle_file))

    p_col = ['code', 'predicted']
    file_data = []
    for code, seq_file in seq_files:
        pred = float(subprocess.check_output([papa_version, '-q', seq_file]))
        data = [code, pred]
        file_data.append(data)

    df_pred = pd.DataFrame(data=file_data, columns=p_col)

    df_snns = pd.merge(df_ang, df_pred, how="right", on='code', sort=False)
    df_snns = df_snns.dropna()
    df_snns.reset_index()

    df_snns['error'] = df_snns['predicted'] - df_snns['angle']

    return df_snns

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--directory', help='Directory of datset', required=True)
parser.add_argument('--seq_directory', help='Directory where .seq files are', required=True)
parser.add_argument('--angle_csv', help='.csv file containing VHVL packing angles', required=True)
parser.add_argument('--csv_output', help='Name of the csv file that will be the output', required=True)
parser.add_argument('--which_papa', help='Specify the name of the papa version being used: "papa" for just PAPA and "~/name_for_new_papa/papa" for all other versions of papa', required=True)
args = parser.parse_args()

result = build_snns_dataframe(args.directory, args.seq_directory, args.angle_csv, args.which_papa)
path = os.path.join(args.directory, f'{args.csv_output}.csv')
result.to_csv(path, index=False)