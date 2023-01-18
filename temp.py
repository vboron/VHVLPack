#!/usr/bin/env python3

import pandas as pd
import argparse
import os


# *************************************************************************
def extract_data(directory, file):
    lines = []
    with open(os.path.join(directory, file), 'r') as f:
        lines = f.readlines()
    codes = []
    angles = []
    for line in lines:
        if line.startswith('PDB Code:'):
            line = line.replace('PDB Code: ', '')
            if '_' not in line:
                line = line + '_0'
            codes.append(line.strip().upper())
        if line.startswith('Torsion angle:'):
            line = line.replace('Torsion angle: ', '')
            angles.append(float(line.strip()))
    data = zip(codes, angles)
    newpapa_df = pd.DataFrame(data = data, columns = ['code', 'predicted'])
    print(newpapa_df)
    newpapa_df.to_csv(os.path.join(directory, 'results_newpapa.csv'), index=False)


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--directory', required=True)
parser.add_argument('--file', required=True)
args = parser.parse_args()

extract_data(args.directory, args.file)