#!/usr/bin/env python3
import functools as ft
import os
import pandas as pd
from utils import *
import argparse
import re

# *************************************************************************


def calculate_packing_angles(directory):
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


    data_list = []
    error_files = []
    for file in os.listdir(directory):
        if file.endswith(".pdb") or file.endswith(".ent"):
            code = file[:-4]
            run_abpackingangle(code, os.path.join(directory, file), data_list)

    col = ['code', 'angle']
    df_ang = pd.DataFrame(data=data_list, columns=col)
    try:
        df_ang = df_ang[df_ang['angle'].str.contains('Packing') == False]
    except:
        print('No missing angles.')
    df_ang['angle'] = df_ang['angle'].astype(float)
    return df_ang


# *************************************************************************
def read_pdbfiles_as_lines(directory) -> pd.DataFrame:
    files = []
    for file in os.listdir(directory):
        if file.endswith(".pdb") or file.endswith(".cho"):
            files.append(os.path.join(directory, file))

    atom_lines = []
    col = ['code', 'L/H position', 'residue']
    re_search_start = re.compile(r'^\s*ATOM')
    for structure_file in files:
        with open(structure_file, "r") as text_file:
            structure_file = structure_file.replace(f'{directory}', '')
            pdb_code = structure_file.replace('.pdb', '')
            if '/' in pdb_code:
                pdb_code = pdb_code.replace('/', '')
            for line in text_file:
                if re_search_start.search(line) != None:
                    items = line.split()
                    if items[2] == 'CA':
                        res_num = items[5]
                        chain = items[4]
                        residue = items[3]
                        lhposition = f'{chain}{res_num}'
                        data = [pdb_code, lhposition, residue]
                        atom_lines.append(data)

    df = pd.DataFrame(data=atom_lines, columns=col)
    return df


# *************************************************************************
def prep_table(df, residue_list_file):
    good_positions = [i.strip('\n')
                      for i in open(residue_list_file).readlines()]
    df = df[df['L/H position'].isin(good_positions)]

    def apply_one_letter_code(row):
        res_one_letter = one_letter_code(row[0], row[2])
        return res_one_letter

    df['residue'] = df.apply(apply_one_letter_code, axis=1)
    df = df.reset_index().drop(["index"], axis=1)
    df = df.drop_duplicates(subset=['code', 'L/H position'], keep='first')
    # df.to_csv('dummy.csv', index=False)
    return df


# *************************************************************************
def pivot_df(df, directory, csv_output, angles):
    df_piv = df.pivot_table(index='code', columns='L/H position', values='residue', aggfunc='sum')
    df = df_piv.reset_index()
    df = df.rename_axis(None, axis=1)
    dfs = [df, angles]
    complete_df = ft.reduce(
        lambda left, right: pd.merge(left, right, on='code'), dfs)
    if '/' in csv_output:
        csv_output = csv_output.replace('/', '')
    csv_path = os.path.join(directory, f'{csv_output}_unencoded_toH100G_noloops.csv')
    complete_df.to_csv(csv_path, index=False)
    return df


# *************************************************************************
def extract_and_export_packing_residues(directory, csv_output, residue_positions):
    print('Making angle table...')
    angle_df = calculate_packing_angles(directory)
    print('Extracting residues...')
    pdb_lines = read_pdbfiles_as_lines(directory)
    print('Turing into one-letter code...')
    res_table = prep_table(pdb_lines, residue_positions)
    print('Pivotting and encoding table...')
    pivotted_table = pivot_df(res_table, directory,
                              csv_output, angle_df)
    just_residues_df = pivotted_table.drop(columns='code')
    encoded_table = encode_4d(just_residues_df)
    encoded_table = encoded_table.join(pivotted_table['code'], how='left')
    dfs = [encoded_table, angle_df]
    final_df = ft.reduce(lambda left, right: pd.merge(
        left, right, on='code'), dfs)
    if '/' in csv_output:
        csv_output = csv_output.replace('/', '')
    csv_path = os.path.join(directory, f'{csv_output}_toH100G_4d.csv')
    final_df.to_csv(csv_path, index=False)
    return final_df, angle_df


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for extracting VH/VL relevant residues')
    parser.add_argument(
        '--directory', help='Directory of pdb files', required=True)
    parser.add_argument(
        '--csv_output', help='Name of the csv file that will be the output', required=True)
    parser.add_argument(
        '--residue_positions', help='File containing a list of the residues to be used as features', required=True)
    args = parser.parse_args()

    extract_and_export_packing_residues(args.directory, 
                                        args.csv_output, 
                                        args.residue_positions)
