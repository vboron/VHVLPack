#!/usr/bin/env python3

import argparse
import os

# *************************************************************************
def make_list(dire):
    with open('500files.txt', 'a') as f:
        for file in os.listdir(dire):
            f.write(f'{file[:5]}, ')
# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--directory', required=True)
args = parser.parse_args()

make_list(args.directory)