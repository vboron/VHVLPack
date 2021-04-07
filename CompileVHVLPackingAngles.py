#!/usr/bin/python3
"""
Program:    VH_VL_Angle_Compiler
File:       VH_VL_Angle_Compiler.py

Version:    V1.1
Date:       15.03.2021
Function:   Calculate angles between VH and VL domains for all PDB files availble

Description:
============
The program takes a directory of Chothia numbered PDB files of antibodies and uses the coordinates to calculate
the packing angle between the VH and VL domains and outputs a list of names with the angles.
e.g.
5I5K_2: -43.150640
3I02_1: -44.048283

--------------------------------------------------------------------------
"""
# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, and subprocess for running external program
import os
import subprocess
import sys
import pandas as pd


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


# *************************************************************************
def read_directory_for_pdb_files(pdb_direct):
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


# *************************************************************************
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


# *************************************************************************
def run_abpackingangle(pdb_files, generate_pdb_names):
    """Run 'abpackingangle' on all files in directory by using the header and .pdb outputs produced and output the
    pdb name followed by the VH-VL packing angle
    e.g.
    2VDM_1: -46.928593
    5V6M_1: -41.396929
    6MLK_1: -48.376004
    5WKO_4: -43.998193
    3U0T_1: -35.507964

        Input:  pdb_files    --- All PDB files in the directory
                pdb_name     --- Names of all PDB files in the directory


        19.03.2021  Original   By: VAB
        """

    # Opens an txt file in binary writing mode and feeds the file output into it
    with open('out.txt', 'w') as outfile:
        # Takes the two lists made in files and combines them into lists of tuples that have
        # the name linked to the file.
        for pdb_file, pdb_code in zip(pdb_files, generate_pdb_names):

            # Uses the subprocess module to call abpackingangle and inputs the headers/.pdb lists
            # into the program as arguments
            try:
                angle_results = subprocess.check_output(['abpackingangle', '-p', pdb_code, '-q', pdb_file])

            # bypasses any files that raise an error and the abpackingangle cannot run
            except subprocess.CalledProcessError:
                continue
            # Converts the output of the subprocess into normal string
            angle_results = str(angle_results, 'utf-8')
            outfile.write(angle_results)
    return angle_results


# *************************************************************************
def convert_to_csv(angles):
    """Break the lines resulting from the abpackingangle function and convert them into a csv table

        Input:  angles    --- lines containing the pdb name and the packing angle separated by ':'


        07.04.2021  Original   By: VAB
        """

    c = ['pdb', 'angle']
    table = []

    # lines are split into objects in the line by the ':' and assigned variable names
    for line in angles:
        pdb_name = (line.split(':')[0]).strip()
        angle = (line.split(':')[1]).strip()
        angle_info = [pdb_name, angle]
        table.append(angle_info)

    # make table that will contain the pdb and the angle in a csv format
    atable = pd.DataFrame(data=table, columns=c)

    return atable


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

pdb_directory = get_pdbdirectory()
# print(pdb_direct)

all_pdb_files = read_directory_for_pdb_files(pdb_directory)
# print('files', pdb_files)

all_pdb_names = extract_pdb_name(pdb_directory)
# print('generate_pdb_names', generate_pdb_names)

calculate_angles = run_abpackingangle(all_pdb_files, all_pdb_names)

produce_csv = convert_to_csv(calculate_angles)
produce_csv.to_csv('VHVL_Packing_Angles.csv', index=False)
