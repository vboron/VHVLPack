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
    #     ds, ds, '13res.dat')
    print('Nonredundantizing...')
    nonred_df = nonred.NR2(encoded_df, ds, f'{ds}_NR2_expanded_residues')
    # nonred_df = nonred.NR2(encoded_df, ds, f'{ds}_NR2_13res')
    return nonred_df


def compare_dirs(df, dir_sept):
    non_red_list = df['code'].tolist()
    print('non_red_list:', len(non_red_list))
 
    sept_dir = 'files_sept_nonred'
    os.mkdir(sept_dir)

    for file in non_red_list:
        print(file)
        file = file + '.pdb'
        src = os.path.join(dir_sept, file)
        dst = os.path.join(sept_dir, file)
        shutil.copy2(src, dst)


parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--sept', required=True, help='Directory which is used as base')

args = parser.parse_args()

df_nonred = preprocessing(args.sept)
compare_dirs(df_nonred, args.sept)