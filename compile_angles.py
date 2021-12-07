#!/usr/bin/env python3
"""
Program:    compile_angles
File:       compile_angles.py

Version:    V1.1
Date:       15.03.2021
Function:   Calculate packing angles between VH and VL domains for all PDB files available and output csv.

Description:
============
The program takes a directory of Chothia numbered PDB files of antibodies and uses the coordinates to calculate
the packing angle between the VH and VL domains and outputs a .csv file containing columns with the pdb code and the
packing angle
e.g.
      pdb       angle
   6NOV_2  -44.016817

Commandline inputs: 1) directory which contains .pdb files for processing
                    2) name of outputted .csv file
--------------------------------------------------------------------------
"""
# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, subprocess for running external program, pandas
# for making dataframes
import os
import sys
import pandas as pd
import subprocess

# *************************************************************************
def buid_table_of_angles():
    """Run 'abpackingangle' on all files in directory by using the header and .pdb outputs produced and output the
    pdb name followed by the VH-VL packing angle
    e.g.
    2VDM_1: -46.928593
    5V6M_1: -41.396929
    6MLK_1: -48.376004
    5WKO_4: -43.998193
    3U0T_1: -35.507964

        Input:  pdb_files         --- All PDB files in the directory
                pdb_name          --- Names of all PDB files in the directory
        Return: angle_results     --- List of angles corresponding to pdb codes
            e.g. ['3U0T_1: -35.507964', '5V6M_1: -41.396929', ...]

        19.03.2021  Original   By: VAB
        """
    
    angle_results = []
    pdb_files = []

    for file in os.listdir(directory):
        if file.endswith(".pdb") or file.endswith(".ent"):
            code = file[:-4]
            pdb_files.append((code, os.path.join(directory, file)))
    
    file_data = []
    # Takes the two lists made in files and combines them into lists of tuples that have
    # the name linked to the file.
    for pdb_code, pdb_file in pdb_files:

        # Uses the subprocess module to call abpackingangle and inputs the headers/.pdb lists
        # into the program as arguments
        try:
            angle = (subprocess.check_output(['abpackingangle', '-p', pdb_code, '-q', pdb_file])).decode("utf-8")

        # bypasses any files that raise an error and the abpackingangle cannot run
        except subprocess.CalledProcessError:
            continue
        # Converts the output of the subprocess into normal string
        angle = angle.split()
        angle = float(angle[1])
        print(angle)
        data = [code, angle]
        file_data.append(data)

    col = ['code', 'angle']
    df_ang = pd.DataFrame(data=file_data, columns=col)

    try:
        df_ang = df_ang[df_ang['angle'].str.contains('Packing angle') == False]
    except:
        print('No missing angles.')

    return df_ang


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
directory = sys.argv[1]
csv_path = os.path.join(directory, (sys.argv[2] + '.csv'))

result = buid_table_of_angles()

result.to_csv(csv_path, index=False)
