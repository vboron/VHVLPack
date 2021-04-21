#!/usr/bin/python3
"""
Program:    filter_by_resolution
File:       filter_by_resolution.py

Version:    V1.0
Date:       20.04.2021
Function:   Find PDB files with a resolution of up to 'd'Å and then move them into a new directory.

Description:
============
The program will take PDB files and take the ones that have a resolution up to a desired Å
and move them to a new directory.

--------------------------------------------------------------------------
"""

# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, subprocess for running external program, pandas
# for making dataframes
import os
import sys
import shutil


# *************************************************************************
def get_pdbdirectory():
    """Read the directory name from the commandline argument

    Return: pdb_direct      --- Directory of PBD files that will be processed

    15.03.2021  Original   By: VAB
    """

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        pdb_direct = sys.argv[1]

    return pdb_direct


# *************************************************************************
def read_directory_for_pdb_files(pdb_direct):
    """Return a list of all files that are PDB files in the called directory

    Input:  pdb_direct   --- Directory of PBD files that will be processed
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
def read_pdbfiles_as_lines(files):
    """Read PDB files as lines, then make a dictionary of the PDB code and the Å resolution

    Input:  files       --- Paths to all PDB files present in the directory
    Return: pdb_dict    --- Dictionary of PDB names and resolution of structure in Å
    e.g. {'2G75_1': ['2.280'], '3IXT_1': ['2.750'],...}

    10.03.2021  Original   By: VAB
    20.04.2021  V2.0       By: VAB
    """

    pdb_dict = {}

    for structure_file in files:
        reso_lines = []
        with open(structure_file, "r") as text_file:

            # Remove the path and the extension from the name of the PDB file
            structure_file = structure_file.replace('{}/'.format(pdb_directory), '')
            structure_file = structure_file[:-4]

            # Search for lines that contain 'REMARK 950 RESOLUTION' and add to reso_lines list
            for line in text_file.read().split('\n'):
                if str(line).strip().startswith('REMARK 950 RESOLUTION'):
                    reso_lines.append(line[22:])

        # Associate the name of the file with the relevant lines in a dictionary
        pdb_dict[structure_file] = reso_lines

    return pdb_dict


# *************************************************************************
def sort_reso(dictionary):
    """
    Look for files whose resolution is better than the maximum given in the command line or a 3Å
    default and put a copy of them into a new directory

    Input:  dictionary      --- Dictionary of PDB name and resolution

    """

    # take the max resolution value from commandline or use 3Å
    if sys.argv[2] == '':
        max_reso = 3
    else:
        max_reso = sys.argv[2]

    for key, value in dictionary.items():
        pdb_code = key
        for reso in value:
            resolution = float(reso)
            if resolution < float(max_reso):

                # Make a copy of the file and put it into the second directory
                shutil.copy('/Users/veronicaboron/Desktop/git/VH_VL_Pack/LH_Combined_Chothia/{}.pdb'.format(pdb_code),
                            '/Users/veronicaboron/Desktop/git/VH_VL_Pack/Good_reso')
    return


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

pdb_directory = get_pdbdirectory()

all_pdb_files = read_directory_for_pdb_files(pdb_directory)

pdb_lines = read_pdbfiles_as_lines(all_pdb_files)

results = sort_reso(pdb_lines)
