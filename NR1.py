#!/usr/bin/env python3
"""
Program:    NR1
File:       NR1.py

Version:    V1.0
Date:       16.11.2021
Function:   Combine duplicate antibody sequences.

Description:
============
The program will extract the sequences from pdb files in a directory and put them in a dictionary, with the pdb files
as the key. Dictionary properties make sure that only one identical key (sequnece) is present. The values which contain
the pdb file name, are then used to move unique sequences into a new directory.

Commandline input: 1) origin directory of pdb files
                   2) name for destination directory for unique sequence psb files
--------------------------------------------------------------------------
"""

# *************************************************************************
# Import libraries

# sys to take args from commandline, os for reading directory, and pandas for building dataframes
import os
import sys
import shutil
import pandas as pd
from utils import one_letter_code

# *************************************************************************
def make_seq_pdb_dict(in_directory):
    """Read PDB files as lines, then make a dictionary of the PDB code and all the lines that start with 'ATOM'

    Return: pdb_dict    --- Dictionary of PDB names with all of the lines containing atom details
    e.g.
    
    16.12.2021  Original   By: VAB
    """

    # create a new directory
    seq_dict = {}

    # look through files in the directory
    for file in os.listdir(in_directory):

        # make sure that the file is a 
        if file.endswith(".pdb") or file.endswith(".ent"):

            # create the full file path so the file can be found
            file_path = os.path.join(in_directory, file)

            # open file in 'read' mode
            with open(file_path, "r") as text_file:

                # create empty string where the sequence will be added
                sequence=''

                # Search for lines that contain the alpha carbon atoms of the amino acid 
                for line in text_file.readlines():
                    if 'ATOM' in str(line) and 'CA' in str(line):

                        # split line so that we can access its elements
                        split_line = line.split()

                        # the .pdb file containes the names of the amino acids in the three-letter code
                        # we use the dictionary that we made earlier to convert these into single letter code
                        residue = one_letter_code(file, split_line[3])

                        # we add the residue into the string to create the full one-letter sequence
                        sequence = sequence + residue
                
                # we create a dictionary entry, where the sequence is the key and the pdb file the value. This allows
                # us to find only one file per sequence.
                seq_dict[sequence] = file

    return seq_dict

# *************************************************************************
def directory_of_unique_files(seq_dict, in_directory, out_directory):

    # new dictionary is made using the second commanline input as the name
    try:
        os.mkdir(out_directory)
    except:
        print('Directory already exists.')

    # we take the pdb file that is in the dictionary and copy it to the new directory we just created (src=source, 
    # dst=destination)
    for key, value in seq_dict.items():
        src = os.path.join(in_directory, value)
        dst = os.path.join(out_directory, value)
        shutil.copyfile(src, dst)

def NR1(in_directory, out_directory):
    dictionary = make_seq_pdb_dict(in_directory)
    directory_of_unique_files(dictionary, in_directory, out_directory)