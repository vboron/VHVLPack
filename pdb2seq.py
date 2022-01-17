#!/usr/bin/env python3
"""
Program:    pdb2seq
File:       pdb2seq

Version:    V1.0
Date:       10.20.2021
Function:   Convert .pdb files to .seq files

Description:
============
Program looks for .pdb files in directory and extracts the chain, position, and residue identity. It the uses that to
construct a .seq file.

Commandline input:  1) directory of pdb files

------------------------------------------------
"""
# *************************************************************************
# Import libraries

import sys
import os

# *************************************************************************
def conv_pdb2seq():

    src_dir = sys.argv[1]
    dst_dir = os.path.join(src_dir, 'seq_files')
    os.mkdir(dst_dir)
    #takes a name of directiry from the commandline and looks through it
    for file in os.listdir(src_dir):

        # looks for files ending in .pdb
        if str(file).endswith('.pdb'):

            # constructs the path to each file
            path = os.path.join(src_dir, file)

            # constructs a path for each file once it is in the .seq format
            path_for_seq = os.path.join(dst_dir, (file[:-4] + '.seq'))

            with open(path, 'r') as f:

                # creates the file specified by the new path and writes in it
                with open(path_for_seq, 'w') as f_seq:
                    for line in f:

                        # looks for lines that contain the alpha carbon details for each residue
                        if str(line).startswith('ATOM') and 'CA' in line:
                            line_info = line.split()
                            chain = line_info[4]
                            res_num = line_info[5]
                            chain_pos = [chain, res_num]
                            chain_pos = ''.join(chain_pos)
                            res = line_info[3]
                            f_seq.write('{} {}{}'.format(chain_pos, res, '\n'))

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
conv_pdb2seq()