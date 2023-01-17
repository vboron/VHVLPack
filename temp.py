#!/usr/bin/env python3

import pandas as pd
import argparse
import os


# *************************************************************************
def extract_data(directory, file):
    lines = []
    with open(os.path.join(directory, file), 'r') as f:
        lines = f.readline().strip()
        print(lines)
    lines = [i for i in lines if i != '------------------------------------']
    print(lines)


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--directory', required=True)
parser.add_argument('--file', required=True)
args = parser.parse_args()

extract_data(args.directory, args.file)