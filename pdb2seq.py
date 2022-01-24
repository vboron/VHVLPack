#!/usr/bin/env python3
"""
Function:   Convert .pdb files to .seq files

Description:
============
Program looks for .pdb files in directory and extracts the chain, position, and residue identity. It the uses that to
construct a .seq file.

------------------------------------------------
"""
# *************************************************************************
# Import libraries

import argparse
import os

# *************************************************************************
def conv_pdb2seq(directory):

    src_dir = directory
    dst_dir = os.path.join(src_dir, 'seq_files')
    try:
        os.mkdir(dst_dir)
    except FileExistsError:
        print(f'Directory {dst_dir} already exists. Continuing...')

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
parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--directory', help='Directory of datset', required=True)
args = parser.parse_args()
conv_pdb2seq(args.directory)