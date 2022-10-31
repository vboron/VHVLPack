#!/usr/bin/env python3
import functools as ft
import os
from ssl import ALERT_DESCRIPTION_UNEXPECTED_MESSAGE
import pandas as pd
from utils import *
import argparse
import re


# *************************************************************************
def calculate_packing_angles(directory, angle_file):
    """Run 'abpackingangle' on all files in directory by using the header and .pdb outputs produced and output the
    pdb name followed by the VH-VL packing angle
    e.g.
    2VDM_1: -46.928593
    5V6M_1: -41.396929
    6MLK_1: -48.376004
    5WKO_4: -43.998193
    3U0T_1: -35.507964
    """

    def run_abpackingangle(pdb_code, pdb_file, data_list):
        try:
            angle = (subprocess.check_output(
                ['abpackingangle', '-p', pdb_code, '-q', pdb_file])).decode("utf-8")
            angle = angle.split()
            data = [pdb_code, angle[1]]
            data_list.append(data)
        except subprocess.CalledProcessError:
            error_files.append(code)

    ang_df = pd.read_csv(angle_file)
    ang_df = ang_df[['code', 'angle']]
    print(ang_df)
    data_list = []
    error_files = []
    for file in os.listdir(directory):
        if file.endswith(".pdb") or file.endswith(".ent"):
            code = file[:-4]
            run_abpackingangle(code, os.path.join(directory, file), data_list)

    col = ['code', 'predicted']
    df_pred = pd.DataFrame(data=data_list, columns=col)
    try:
        df_pred = df_pred[df_pred['predicted'].str.contains('Packing') == False]
    except:
        print('No missing angles.')
    df_pred['predicted'] = df_pred['predicted'].astype(float)
    print(df_pred)
    final = df_pred.merge(ang_df, on='code')
    final['error'] = final['predicted'] - final['angle']
    final.to_csv(os.path.join(directory, 'results_abymod.csv'), index=False)

parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--dir', help='Directory of datset', required=True)
parser.add_argument('--ang', help='File which has actual angles', required=True)
parser.add_argument('--out', help='Output name', required=True)
args = parser.parse_args()

calculate_packing_angles(args.dir, args.ang)