#!/usr/bin/env python3
'''
Program:    VH_VL_Angle_Compiler
File:       VH_VL_Angle_Compiler.py

Version:    V1.0
Date:       15.03.2021
Function:   Calculate angles between VH and VL domains for all PDB files availble

Description:
============
The program takes a directory of Chothia numbered PDB files of antibodies and uses the coordinates to calculate
the packing angle between the VH and VL domains and outputs a list of names with the angles.
e.g.


--------------------------------------------------------------------------
'''
# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, and subprocess for running external program
import os
import subprocess
import sys

# *************************************************************************
def get_pdbdirectory():
    """Read the directory name from the commandline argument

    Return: pdb_directory      --- Directory of PBD files that will be processed for VH-VL packing angles

    15.03.2021  Original   By: VAB
    """

    # Take the commandline input as the directory
    pdb_direct = sys.argv[1]
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
            files.append(file)
    return files

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
        if pdb.endswith(".pdb") or file.endswith(".ent"):
            pdb_name = os.path.splitext(pdb)[0]
            pdb_names.append(pdb_name)
    return pdb_names


#*************************************************************************
def run_abpackingangle(pdb_files, generate_pdb_names):
    """Run abpackingangle on all files in directory by using the header and .pdb outputs produced

        Input:  pdb_files    --- DAll PDB files in the directory
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
            #p1 = subprocess.check_output(['echo', '-p', pdb_file, list2])
            angle_results = subprocess.check_output(['abpackingangle', '-p', pdb_file, '-q', pdb_code])

            # Converts the output of the subprocess into normal string
            angle_results = str(angle_results, 'utf-8')
            outfile.write(angle_results)
    return

#*************************************************************************
#*** Main program                                                      ***
#*************************************************************************

pdb_direct = get_pdbdirectory()
#print(pdb_direct)

pdb_files = read_directory_for_PDB_files(pdb_direct)
#print('files', pdb_files)

generate_pdb_names = extract_pdb_name(pdb_direct)
#print('generate_pdb_names', generate_pdb_names)

calculate_angles = run_abpackingangle(pdb_files, generate_pdb_names)
