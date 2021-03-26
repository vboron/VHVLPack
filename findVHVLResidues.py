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
def prep_table(lines):
    """Build table for atom information using pandas dataframes

    Input:  lines      --- All PDB files split into lines
    Return: ftable     --- Sorted table of information about all atoms in the PDB file:
   e.g.
     residue res_num
0        ASP      1
1        ASP      1
2        ASP      1

    10.03.2021  Original   By: VAB
    """

    # Create blank lists for lines in file that contain atom information
    atom_lines = []
    table = []

    # Assign column names for residue table
    c = ["residue", "res_num"]

    # Search for lines that contain 'ATOM' and add to atom_lines list
    for items in lines:
        if items.startswith('ATOM'):
            atom_lines.append(items)

    # Locate specific atom information by line indices and label them. Compound all the data into one list.
    for res_data in atom_lines:
        residue = (res_data[17:20]).strip()

        res_num = (res_data[23:27]).strip()
        res_id = "{}{}".format(residue, res_num)
        res_info = [residue, res_num]
        table.append(res_info)

    # Use pandas to build a data table from compiled residue info and column headers:
    ftable = pd.DataFrame(table, columns=c)
    #print(atom_lines)
    return ftable

#*************************************************************************
def filtering_for_VH_VL_residues(ftable):
    """Compare specified atom type in specified residue against atoms in other residues within specified distance

    Input:  ftable     --- Sorted table of information on all residues in PDB files
    Output: otable     --- Output table that contains the atoms (of specified parameters) and the distances between them
   e.g.


    10.03.2021  Original   By: VAB
    """

    if zip(pdb_files, generate_pdb_names) == ('LYS', '38') or ('LYS', '40') or ('LYS', '41') or ('LYS', '44') or ('LYS', '46') or ('LYS', '87') or ('HIS', '33') or ('HIS', '42') or ('HIS', '45') or ('HIS', 60) or (HIS, 62) or (HIS, 91) or (HIS, 105):
        ResA = ResA[ResA.atom_typ == atom_kind]
    ResB = ftable[ftable.res_num != res_numb]
    if atom_kind != '':
        ResB = ResB[ResB.atom_typ == atom_kind]
    # Label relevant information from ftable data. .iterrows iterates though all of the rows in the table and returns
    # a Series for each row. .values calls the values present in specified spot in the table.
    for index in ResA.iterrows():
        coordsAX = ftable.x_coord.values[index[0]]
        coordsAY = ftable.y_coord.values[index[0]]
        coordsAZ = ftable.z_coord.values[index[0]]
        res_numA = ftable.res_num.values[index[0]]
        residueA = ftable.residue.values[index[0]]
        atom_typA = ftable.atom_typ.values[index[0]]
        atom_numA = ftable.atom_num.values[index[0]]


                c2 = ['from atom', 'res', 'res no.', 'dist (A)', 'to atom', 'res', 'res no.']
                out_table = []
                out_data = [atom_typA, residueA, res_numA, '{:.3f}'.format(distAB), atom_typB, residueB, res_numB]
                out_table.append(out_data)
                otable = pd.DataFrame(out_table, columns=c2)
                print(otable)


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

VHVL_residues = filtering_for_VH_VL_residues(ftable)