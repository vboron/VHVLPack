#!/usr/bin/env python3
"""
Function:   Find the residue identities corresponding to the numbering for VH-VL-packing relevant residues

Description:
============
The program will take PDB files and extract a string of one letter residue codes for the VH-VL-Packing relevant region
and deposits into csv file
e.g.
      code L/H position residue
    5DMG_2          L38       Q
    5DMG_2          L40       P
    5DMG_2          L41       G
    5DMG_2          L44       P

--------------------------------------------------------------------------
"""
# *************************************************************************
import os
import pandas as pd
from utils import one_letter_code
import argparse

# *************************************************************************


def read_pdbfiles_as_lines(directory):
    """Read PDB files as lines, then make a dictionary of the PDB code and all the lines that start with 'ATOM'

    Return: pdb_dict    --- Dictionary of PDB names with all of the lines containing atom details
    e.g.
    {'5DMG_2': ['ATOM   4615  N   GLN L   2     -34.713  12.044 -12.438  1.00 44.10         N  ',...'], '5DQ9_3':...'}

    10.03.2021  Original   By: VAB
    """
    # Creates an empty list, then iterates over all files in the directory called from the
    # commandline. Adds all these .pdb  and .ent files to the list.
    files = []

    for file in os.listdir(directory):
        if file.endswith(".pdb") or file.endswith(".ent"):

            # Prepends the directory path to the front of the file name to create full filepath
            files.append(os.path.join(directory, file))

    atom_lines = []
    col = ['code', 'L/H position', 'residue']
    for structure_file in files:
        
        with open(structure_file, "r") as text_file:

            structure_file = structure_file.replace(directory, '')
            pdb_code = structure_file[:-4]

            for line in text_file.read().split('\n'):
                if str(line).strip().startswith('ATOM'):
                    # atom_lines.append(line)
                    items = line.split()
                    if items[2] == 'CA':
                        res_num = items[5]
                        chain = items[4]
                        residue = items[3]
                        lhposition = str(f'{chain}{res_num}')
                        data = [pdb_code, lhposition, residue]
                        atom_lines.append(data)

            # pdb_dict[structure_file] = atom_lines
            text_file.close()
    
    df = pd.DataFrame(data = atom_lines, columns=col)
    return df


# *************************************************************************
def prep_table(df, residue_list_file, csv_output, directory):

    good_positions = [i.strip('\n')
                      for i in open(residue_list_file).readlines()]


    df = df[df['L/H position'].isin(good_positions)]
    def apply_one_letter_code(row):
        print(row[0], row[1], row[2])
        # one_letter_code(row[1], row[3])
    df['residue'] = df.apply(apply_one_letter_code, axis=1)
    print(df)
    # ftable = ftable.drop_duplicates()

    # csv_path = os.path.join(directory, (csv_output + '.csv'))
    # ftable.to_csv(csv_path, index=False)
    # return ftable


def extract_and_export_packing_residues(directory, csv_output, residue_positions):
    pdb_lines = read_pdbfiles_as_lines(directory)
    VHVLtable = prep_table(pdb_lines, residue_positions, csv_output, directory)
    # return VHVLtable
    
    


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
