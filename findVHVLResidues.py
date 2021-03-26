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
    """Print a list of headers of PDB files in the called directory

    Input:  pdb_direct   --- Directory of PBD files that will be processed for VH-VL packing angles
    Return: pdb_name     --- Names of all PDB files in the directory


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
def read_pdbfiles_as_lines(pdb_files):
    """Read PDB files as lines

    Input:  pdb_files   --- All PDB files in the directory
    Return: lines       --- PDB files split into lines


    10.03.2021  Original   By: VAB
    """
    for structure_files in pdb_files:
        text_file = open(structure_files, "r")
    # Splits the opened PDB file at '\n' (the end of a line of text) and returns those lines
        lines = text_file.read().split('\n')
    return lines

#*************************************************************************
def one_letter_code(residue):

    """
    Go from the three-letter code to the one-letter code.

    Input:  residue      --- Three-letter residue identifier
    Return: one_letter   --- The one-letter residue identifier

    20.10.2020  Original   By: LD
    """

    dic = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K', 'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M','XAA': 'X', 'UNK':'X'}
    if len(residue) % 3 != 0:
        raise ValueError("error")
    one_letter = dic[residue]
    return one_letter

#*************************************************************************
def prep_table(lines):
    """Build table for atom information using pandas dataframes

    Input:  lines      --- All PDB files split into lines
    Return: ftable     --- Sorted table that contains the residue id:
    e.g.
         residue
    0         D1

    10.03.2021  Original   By: VAB
    26.03.2021  V2.0       By: VAB
    """

    # Create blank lists for lines in file that contain atom information
    atom_lines = []
    table = []

    # Assign column names for residue table
    c = ["residue"]

    # Search for lines that contain 'ATOM' and add to atom_lines list
    for items in lines:
        if items.startswith('ATOM'):
            atom_lines.append(items)


        #res_name_one.append(res_one)

    # Locate specific residue information, covert three-letter identifier into one-letter and formulate residue id
    # e.g. D1, Q460 etc.
    for res_data in atom_lines:
        res_num = (res_data[23:27]).strip()
        residue = (res_data[17:20]).strip()
        res_one = one_letter_code(residue)
        res_id = "{}{}".format(res_one, res_num)
        #pdb_code = generate_pdb_names
        res_info = [res_id]
        table.append(res_info)

    # Use pandas to build a data table from compiled residue info and column headers:
    ftable = pd.DataFrame(table, columns=c)
    #print(atom_lines)
    return ftable

#*************************************************************************
def VH_VL_relevant_residues(ftable):
    """Filter table for residues relevant for VH-VL packing

    Input:  ftable     --- Sorted table that contains the residue id
    Return:  :
    e.g.

    26.03.2021  Original   By: VAB
    """

    VHVLtable = ftable[ftable.res_id == 'L38' or 'L40' or 'L41' or 'L44' or 'L46' or 'L87' or 'H33' or 'H42' or 'H45' or 'H60' or 'H62' or 'H91' or 'H105']
    for res_code in VHVLtable.iterrows:
        VHVLcode = ftable.res_id.values[index[0]]
        c2 = ['VH-VL residues']
        out_table = []
        out_data = [VHVLcode]
        out_table.append(out_data)
        otable = pd.DataFrame(out_table, columns=c2)

    return otable
#*************************************************************************
#*** Main program                                                      ***
#*************************************************************************

pdb_direct = get_pdbdirectory()

generate_pdb_names = extract_pdb_name(pdb_direct)

pdb_files = read_directory_for_PDB_files(pdb_direct)
#print(pdb_files)

lines = read_pdbfiles_as_lines(pdb_files)
#print(lines)

ftable = prep_table(lines)
#print(ftable)

#VHVL_residues = filtering_for_VH_VL_residues(ftable)

VHVLtable = VH_VL_relevant_residues(ftable)
print(VHVLcode)