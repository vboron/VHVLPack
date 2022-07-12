#!/usr/bin/env python3
import functools as ft
import os
import pandas as pd
from utils import *
import argparse
import re
from multiprocessing import Pool

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
            angle = (subprocess.check_output(['abpackingangle', '-p', pdb_code, '-q', pdb_file])).decode("utf-8")
        except subprocess.CalledProcessError:
            pass
        angle = angle.split()
        data = [pdb_code, angle[1]]
        data_list.append(data)

    data_list = []
    with Pool() as p:
        results = []
        for file in os.listdir(directory):
            if file.endswith(".pdb") or file.endswith(".ent"):
                code = file[:-4]
                results.append(p.apply_async(run_abpackingangle, (code, os.path.join(directory, file), data_list)))
                # run_abpackingangle(code, os.path.join(directory, file), data_list)
        p.close()
        p.join()
        if not all([r.successful() for r in results]):
            raise 

    col = ['code', 'angle']
    df_ang = pd.DataFrame(data=data_list, columns=col)
    try:
        df_ang = df_ang[df_ang['angle'].str.contains('Packing') == False]
    except:
        print('No missing angles.')
    df_ang['angle'] = df_ang['angle'].astype(float)
    print(df_ang)
    return df_ang


# *************************************************************************
def read_pdbfiles_as_lines(directory):
    files = []
    for file in os.listdir(directory):
        if file.endswith(".pdb") or file.endswith(".ent"):
            files.append(os.path.join(directory, file))

    atom_lines = []
    col = ['code', 'L/H position', 'residue']
    re_search_start = re.compile(r'^\s*ATOM')
    for structure_file in files:
        with open(structure_file, "r") as text_file:
            structure_file = structure_file.replace(directory, '')
            pdb_code = structure_file[:-4]
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
    cdrL1_pos = [f'L{i}' for i in range(24, 35)]
    cdrH2_pos = [f'H{i}' for i in range(50, 59)]
    cdrH3_pos = [f'H{i}' for i in range(95, 103)]

    def calc_loop_length(pos_list, loop_name):
        df_loop = df[df['L/H position'].isin(pos_list)]
        df_loop = df_loop.groupby(['code']).sum()
        df_loop[f'{loop_name}_length'] = df_loop['residue'].str.len()
        df_loop = df_loop.drop(columns=['L/H position', 'residue'])
        return df_loop
    
    l1_df = calc_loop_length(cdrL1_pos, 'L1')
    h2_df = calc_loop_length(cdrH2_pos, 'H2')
    h3_df = calc_loop_length(cdrH3_pos, 'H3')

    loop_dfs = [l1_df, h2_df, h3_df]
    loop_df = ft.reduce(lambda left, right: pd.merge(left, right, on='code'), loop_dfs)

    good_positions = [i.strip('\n')
                      for i in open(residue_list_file).readlines()]
    df = df[df['L/H position'].isin(good_positions)]

    def apply_one_letter_code(row):
        res_one_letter = one_letter_code(row[0], row[2])
        return res_one_letter

    df['residue'] = df.apply(apply_one_letter_code, axis=1)
    return df


# *************************************************************************
def pivot_df(df, directory, csv_output, angles):
    df = df.pivot(index='code', columns='L/H position', values='residue')
    complete_df = pd.merge(df, angles, how="right", on=["code"], sort=True)
    csv_path = os.path.join(directory, f'{csv_output}_unencoded_toH100G.csv')
    complete_df.to_csv(csv_path, index=False)
    return df


# *************************************************************************
def extract_and_export_packing_residues(directory, csv_output, residue_positions):
    angle_df = calculate_packing_angles(directory)
    pdb_lines = read_pdbfiles_as_lines(directory)
    res_table = prep_table(pdb_lines, residue_positions)
    pivotted_table = pivot_df(res_table, directory, csv_output, angle_df)
    encoded_table = encode_4d(pivotted_table)
    final_df = pd.merge(encoded_table, angle_df, how="right", on=["code"], sort=True)
    csv_path = os.path.join(directory, f'{csv_output}_toH100G_4d.csv')
    final_df.to_csv(csv_path, index=False)
    return final_df


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

    extract_and_export_packing_residues(
        args.directory, args.csv_output, args.residue_positions)
