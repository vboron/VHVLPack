#!/usr/bin/env python3

import os
import pandas as pd
import utils
import argparse

# *************************************************************************


def read_pdbfiles_as_lines(directory):
    files = []

    for file in os.listdir(directory):
        if file.endswith(".pdb") or file.endswith(".ent"):
            files.append(os.path.join(directory, file))

    atom_lines = []
    col = ['code', 'L/H position', 'residue']
    for structure_file in files:

        with open(structure_file, "r") as text_file:

            structure_file = structure_file.replace(directory, '')
            pdb_code = structure_file[:-4]

            for line in text_file.read().split('\n'):
                if str(line).strip().startswith('ATOM'):
                    items = line.split()
                    if items[2] == 'CA':
                        res_num = items[5]
                        chain = items[4]
                        residue = items[3]
                        lhposition = str(f'{chain}{res_num}')
                        data = [pdb_code, lhposition, residue]
                        atom_lines.append(data)
            text_file.close()

    df = pd.DataFrame(data=atom_lines, columns=col)
    return df


# *************************************************************************
def prep_table(df, residue_list_file):

    good_positions = [i.strip('\n')
                      for i in open(residue_list_file).readlines()]
    df = df[df['L/H position'].isin(good_positions)]

    def apply_one_letter_code(row):
        res_one_letter = utils.one_letter_code(row[0], row[2])
        # print(res_one_letter)
        return res_one_letter

    df['residue'] = df.apply(apply_one_letter_code, axis=1)
    return df

# *************************************************************************
def pivot_df(df, directory, csv_output):
    df = df.pivot(index='code', columns='L/H position', values='residue')
    # df.reset_index()
    csv_path = os.path.join(directory, f'{csv_output}.csv')
    df.to_csv(csv_path, index=True)
    return df

def encode_4d(df):
    def encode_rows(row):
        print(row)
    test = df.apply(encode_rows, axis=1)

def extract_and_export_packing_residues(directory, csv_output, residue_positions):
    pdb_lines = read_pdbfiles_as_lines(directory)
    VHVLtable = prep_table(pdb_lines, residue_positions)
    pivotted_table = pivot_df(VHVLtable, directory, csv_output)
    # return VHVLtable
    encode_4d(pivotted_table)


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
