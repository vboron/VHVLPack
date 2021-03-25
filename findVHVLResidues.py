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
def prep_table(pdb_files):
    """Build table for atom information using pandas dataframes

    Input:  pdb_files      --- All PDB files in the directory
    Return: ftable     --- Sorted table of information about all atoms in the PDB file:
   e.g.


    10.03.2021  Original   By: VAB
    """
    # Create blank lists for lines in file that contain atom information
    atom_lines = []
    table = []
    # Assign column names for residue table
    c = ["residue", "res_num"]
    # Search for lines that contain 'ATOM' and add to atom_lines list
    for items in pdb_files:
        if items.startswith('ATOM'):
            atom_lines.append(items)
    # Locate specific atom information by line indices and label them. Compound all the data into one list.
    for res_info in atom_lines:
        residue = res_info[17:20]
        res_num = int(res_info[23:27])
        res_id = "{}{}".format(residue, res_num)
        table.append(res_info)
    # Use pandas to build a data table from compiled residue info and column headers:
    ftable = pd.DataFrame(table, columns=c)
    return ftable


#*************************************************************************
#*** Main program                                                      ***
#*************************************************************************

pdb_direct = get_pdbdirectory()

pdb_files = read_directory_for_PDB_files(pdb_direct)

ftable = prep_table(pdb_files)
print(ftable)
