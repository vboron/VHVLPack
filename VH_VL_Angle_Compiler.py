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

# argparse for commandline tags, os for reading directory, and subprocess for running external program
import argparse
import os
import subprocess

# *************************************************************************
def make_commandline_flags():
    """Create command line tags for importing pdb directory

    Return: pdb_directory      --- Directory of PBD files that will be processed for VH-VL packing angles

    15.03.2021  Original   By: VAB
    """

    # Call parser
    parser = argparse.ArgumentParser()

    # Set command line tags. nargs='?' specifies that for an empty argument the default value will be taken. Help args
    # can be called using --h and will display the message in 'help='.
    # commandline input: $python3 VH_VL_Angle_Compiler.py -d
    parser.add_argument('-d', '--directory', help='Directory of PDB files for VH-VL processing')
    args = parser.parse_args()
    pdb_direct = args.directory
    return pdb_direct

#*************************************************************************
def read_directory(pdb_direct):
    """Print a list of all files that are PDB files in the called directory

    Input:  pdb_direct   --- Directory of PBD files that will be processed for VH-VL packing angles
    Return: files        --- All PDB files in the directory


    15.03.2021  Original   By: VAB
    """

    # Creates an empty list, then iterates over all files in the directory called from the
    # commandline. Adds all these .pdb files to the list.
    files = []
    for file in os.listdir(pdb_direct):
        if file.endswith(".pdb"):
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
        if pdb.endswith(".pdb"):
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
    with open('out.txt', 'wb') as outfile:
        # Takes the two lists made in files and combines them into lists of tuples that have
        # the name linked to the file.
        for list1, list2 in zip(pdb_files, generate_pdb_names):

            # Uses the subprocess module to call abpackingangle and inputs the headers/.pdb lists
            # into the program as arguments
            p1 = subprocess.check_output(['abpackingangle', '-p', list1, '-q', list2])
            outfile.write(p1)
    return

#*************************************************************************
#***                               Main                                ***
#*************************************************************************

pdb_direct = make_commandline_flags()

pdb_files = read_directory(pdb_direct)

generate_pdb_names = extract_pdb_name(pdb_direct)

calculate_angles = run_abpackingangle(pdb_files, generate_pdb_names)
