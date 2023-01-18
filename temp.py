#!/usr/bin/env python3

import pandas as pd
import argparse
import os


# *************************************************************************
def extract_data(directory, file):
    lines = []
    with open(os.path.join(directory, file), 'r') as f:
        lines = f.readlines()
        print(lines)
    # lines = [i.strip() for i in lines if '------------------------------------' not in i]
    codes = []
    angles = []
    for line in lines:
        if line.startswith('PDB Code:'):
            codes.append(line.strip())
        if line.startswith('Torsion angle:'):
            angles.append(line.strip())
    # print(lines)
    print('codes: ', codes)
    print('angles: ', angles)


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--directory', required=True)
parser.add_argument('--file', required=True)
args = parser.parse_args()

extract_data(args.directory, args.file)