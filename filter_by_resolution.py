#!/usr/bin/env python3
"""
Program:    filter_by_resolution
File:       filter_by_resolution.py

Version:    V1.0
Date:       20.04.2021
Function:   Find PDB files with a resolution of up to 'd'Å and then move them into a new directory.

Description:
============
The program will look at PDB files and take the ones that have a resolution up to a desired Å
and move them to a new directory.

Commandline inputs: 1) directory of pdb files with full path
                    2) maximum desired resolution in Å
		    3) name for the directory where the files will be
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
def find_xray_files():
    """Return a list of all files that are PDB files in the called directory

    Input:  pdb_direct   --- Directory of PBD files that will be processed
    Return: files        --- All PDB files in the directory


    15.03.2021  Original   By: VAB
    """

    # Creates an empty list, then iterates over all files in the directory called from the
    # commandline. Adds all these .pdb files to the list.
    files = []
    xray_files = []
    path = os.getcwd()
    pdb_direct = sys.argv[1]

    for file in os.listdir(pdb_direct):
        if file.endswith(".pdb") or file.endswith(".ent"):
            files.append(os.path.join(path, sys.argv[1], file))

    for structure_file in files:
        with open(structure_file, 'r') as text_file:

            # Search for lines that contain 'REMARK 950 RESOLUTION' and add to reso_lines list
            for line in text_file:
                if str(line).startswith(' REMARK 950 METHOD     X-RAY'):
                    xray_files.append(structure_file)

    return xray_files


# *************************************************************************
def read_pdbfiles_as_lines(xfiles):
    """Read PDB files as lines, then make a dictionary of the PDB code and the Å resolution

    Input:  files       --- Paths to all PDB files present in the directory
    Return: pdb_dict    --- Dictionary of PDB names and resolution of structure in Å
    e.g. {'2G75_1': ['2.280'], '3IXT_1': ['2.750'],...}

    10.03.2021  Original   By: VAB
    20.04.2021  V2.0       By: VAB
    """

    pdb_dict = {}

    for structure_file in xfiles:
        reso_lines = []
        with open(structure_file) as text_file:

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

    # take the max resolution value from commandline or use 5Å
    if len(sys.argv) < 3:
        max_reso = 5
    else:
        max_reso = sys.argv[2]

    # find current directory and make a new file in it
    cwd = os.getcwd()
    new_directory = sys.argv[3]
    path = os.path.join(cwd, new_directory)
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

    for key, value in dictionary.items():
        pdb_code = key
        for reso in value:
            resolution = float(reso)
            if resolution < float(max_reso):

                # Make a copy of the file and put it into the second directory
                shutil.copy(os.path.join(sys.argv[1], '{}.pdb'.format(pdb_code)), path)
    return


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

x_ray_files = find_xray_files()

pdb_lines = read_pdbfiles_as_lines(x_ray_files)

results = sort_reso(pdb_lines)