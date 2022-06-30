#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing

if __name__ == '__main__':
    path = os.path.join('Everything', 'Everything_NR2_GBReg.csv')
    df = pd.read_csv(path)
    pdb_codes = df['code'].to_list()
    with open(os.path.join('Everything', 'pdb_list.txt'), 'w') as f:
        for item in pdb_codes:
            f.write(item + '\n')
