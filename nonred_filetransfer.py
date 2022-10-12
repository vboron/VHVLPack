#!/usr/bin/env python3
import argparse
import os
import shutil
import nonred
import encode_res_calc_angles as erca


def preprocessing(ds):
    print('Extracting angles and residues, and encoding...')
    encoded_df, _x_ = erca.extract_and_export_packing_residues(
        ds, ds, 'expanded_residues.dat')
    # encoded_df, ang_df = erca.extract_and_export_packing_residues(
    #     ds, ds, '4d.dat')
    print('Nonredundantizing...')
    nonred_df = nonred.NR2(encoded_df, ds, f'{ds}_NR2_expanded_residues')
    # nonred_df = nonred.NR2(encoded_df, ds, f'{ds}_NR2_13res')
    return nonred_df


def compare_dirs(df, dir_sept, dir_jul):
    non_red_list = df['code'].tolist()
    sept_files = os.listdir(dir_sept)
    jul_files = os.listdir(dir_jul)

    jul_nonred = []
    for file in jul_files:
        if file in non_red_list:
            jul_nonred.append(file)
    jul_dir = 'files_july_nonred'
    sept_dir = 'files_july2sept_nonred'
    os.mkdir(jul_dir)
    os.mkdir(sept_dir)
    print(len(jul_nonred))

    for file in jul_nonred:
        print(file)
        src = os.path.join(dir_jul, file)
        dst = os.path.join(jul_dir, file)
        shutil.copy2(src, dst)
    sept_nonred = []
    for file in sept_files:
        if file in non_red_list and file not in jul_nonred:
            sept_nonred.append(file)
    print(len(sept_nonred))
    for file in sept_nonred:
        print(file)
        src = os.path.join(dir_sept, file)
        dst = os.path.join(sept_dir, file)
        shutil.copy2(src, dst)
    check = len(non_red_list)-len(sept_nonred)-len(jul_nonred)
    print(check)


parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--sept', required=True, help='Directory which is used as base')
parser.add_argument('--jul', required=True, help='Directory from which files will be copied into new directory')

args = parser.parse_args()

df_nonred = preprocessing(args.sept)
compare_dirs(df_nonred, args.sept, args.jul)