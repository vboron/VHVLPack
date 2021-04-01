#!/usr/bin/python3
'''
Program:    findVHVLResidues
File:       findVHVLResidues.py

Version:    V1.0
Date:       25.03.2021
Function:   Find the residue identities corresponding to the numbering for VH-VL-packing relevant residues

Description:
============
The program will take PDB files and extract a string of one letter residue codes for the VH-VL-Packing relevant region
e.g.


--------------------------------------------------------------------------
'''
# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, and subprocess for running external program
import os
import sys
import pandas as pd
import numpy as np

# *************************************************************************
def get_pdbdirectory():
    """Read the directory name from the commandline argument

    Return: pdb_directory      --- Directory of PBD files that will be processed for VH-VL packing angles

    15.03.2021  Original   By: VAB
    """

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        pdb_direct = sys.argv[1]
    else:
        pdb_direct = '.'
    return pdb_direct

#*************************************************************************
def extract_pdb_name(pdb_direct):
    """Return a list of headers of PDB files in the called directory

    Input:  pdb_direct   --- Directory of PBD files that will be processed for VH-VL packing angles
    Return: pdb_name     --- Names of all PDB files in the directory
    e.g. ['5DMG_2', '5DQ9_3']


    18.03.2021  Original   By: VAB
    """

    # Iternates over all files in directory, checks if they are pdb files and returns the
    # name without the extension into a list.
    pdb_names = []
    for pdb in os.listdir(pdb_direct):
        if pdb.endswith(".pdb") or pdb.endswith(".ent"):
            pdb_name = os.path.splitext(pdb)[0]
            pdb_names.append(pdb_name)
    return pdb_names

#*************************************************************************
def read_directory_for_PDB_files(pdb_direct):
    """Print a list of all files that are PDB files in the called directory

    Input:  pdb_direct   --- Directory of PBD files that will be processed for VH-VL packing angles
    Return: files        --- All PDB files in the directory
    e.g. ['/Users/veronicaboron/Desktop/git/VH_VL_Pack/some_pdbs/5DMG_2.pdb',
    '/Users/veronicaboron/Desktop/git/VH_VL_Pack/some_pdbs/5DQ9_3.pdb']


    15.03.2021  Original   By: VAB
    """

    # Creates an empty list, then iterates over all files in the directory called from the
    # commandline. Adds all these .pdb files to the list.
    files = []
    for file in os.listdir(pdb_direct):
        if file.endswith(".pdb") or file.endswith(".ent"):
            files.append('{}/{}'.format(pdb_direct, file))
    return files


#*************************************************************************
def read_pdbfiles_as_lines(files):
    """Read PDB files as lines, then make a dictionary of the PDB code and all the lines that start with 'ATOM'

    Input:  pdb_files   --- All PDB files in the directory
    Return: pdb_dict    --- Dictionary containing PDB code of file and all the ATOM lines in that file
    e.g {'5DMG_2': ['ATOM   4615  N   GLN L   2     -34.713  12.044 -12.438  1.00 44.10           N  ',
    'ATOM   4616  CA  GLN L   2     -33.620  11.176 -11.893  1.00 43.59           C  ',
    'ATOM   4617  C   GLN L   2     -33.836   9.696 -12.231  1.00 39.04           C  '...']}

    10.03.2021  Original   By: VAB
    29.03.2021  V2.0       By: VAB
    """

    lines = []
    atom_lines = []

    # Search all PDB files inside the list of all PDB files made before
    for structure_file in files:

        # Open each file in 'read' using the file-paths stored in 'files'
        text_file = open(structure_file, "r")

        # For each PDB file name remove the
        structure_file = structure_file.replace('{}/'.format(pdb_direct), '')
        structure_file = structure_file[:-4]
    # Splits the opened PDB file at '\n' (the end of a line of text) and returns those lines
        lines.append(text_file.read().split('\n'))
        print(lines)

 # Search for lines that contain 'ATOM' and add to atom_lines list
        for pdb_file_split in lines:

            for line in pdb_file_split:
                if str(line).strip().startswith('ATOM'):
                    atom_lines.append(line)
            pdb_dict = {structure_file: atom_lines}
            #print(pdb_dict)
        return pdb_dict


#*************************************************************************
def one_letter_code(res):

    """
    Go from the three-letter code to the one-letter code.

    Input:  residue      --- Three-letter residue identifier
    Return: one_letter   --- The one-letter residue identifier

    20.10.2020  Original   By: LD
    """

    dic = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K', 'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M','XAA': 'X', 'UNK':'X'}
    if len(res) % 3 != 0:
        raise ValueError("error")
    one_letter = dic[res]
    return one_letter

#*************************************************************************
def prep_table(dict_list):
    """Build table for atom information using pandas dataframes

    Input:  lines      --- All PDB files split into lines
    Return: ftable     --- Sorted table that contains the residue id:
    e.g.
          chain residue number L/H position
    0        L       D      1           L1
    8        L       I      2           L2
    16       L       V      3           L3
    23       L       L      4           L4
    31       L       T      5           L5

    10.03.2021  Original   By: VAB
    26.03.2021  V2.0       By: VAB
    """

    # Create blank lists for lines in file that contain atom information
    table = []
    pdb_code = []
    # Assign column names for residue table
    c = ['PDB Code', 'chain', "residue", 'number', 'L/H position']

    # Locate specific residue information, covert three-letter identifier into one-letter
    for key, values in lines.items():
        if (isinstance(values, list)):
            for data in values:
                pdb_code = key
                res_num  = str(data[23:27]).strip()
                chain    = str(data[21:22]).strip()
                residue  = str(data[17:21]).strip()
                res_one  = str(one_letter_code(residue))
                L_H_position = str("{}{}".format(chain, res_num))
                res_info = [pdb_code, chain, res_one, res_num, L_H_position]
                table.append(res_info)
    #print(table)
    # Use pandas to build a data table from compiled residue info and column headers:
    ftable = pd.DataFrame(data=table, columns=c)

    # Remove all row duplicates
    ftable = ftable.drop_duplicates()
    return ftable

#*************************************************************************
def VH_VL_relevant_residues(vtable):
    """Filter table for residues relevant for VH-VL packing

    Input:  vtable     --- Sorted table that contains the residue id
    Return:  :
    e.g.

    26.03.2021  Original   By: VAB
    """

    # Find all of the key residues for VH/VL packing:
    # e.g  chain residue number L/H position
    # 267      L       Q     38          L38
    # 285      L       S     40          L40
    # 291      L       G     41          L41
    # 308      L       P     44          L44
    vtable = vtable[vtable['L/H position'].str.contains('L38|L40|L41|L44|L46|L87|H33|H42|H45|H60|H62|H91|H105')]
    #print(vtable)

    vtable['res_id'] = vtable['residue'].str.cat(vtable['number'], sep='')

    #create a table of just res_id values
    otable = vtable[['res_id']]
    #print(vtable)

    return otable
#*************************************************************************
#*** Main program                                                      ***
#*************************************************************************

pdb_direct = get_pdbdirectory()
#print('pdb_direct', pdb_direct)

generate_pdb_names = extract_pdb_name(pdb_direct)
#print('generate_pdb_names', generate_pdb_names)

pdb_files = read_directory_for_PDB_files(pdb_direct)
#print(pdb_files) # a list of all pdb files (full paths)

pdb_lines = read_pdbfiles_as_lines(pdb_files)
#print(pdb_lines)

ftable = prep_table(pdb_lines)
#print(ftable)

VHVLtable = VH_VL_relevant_residues(ftable)
#print(VHVLtable)