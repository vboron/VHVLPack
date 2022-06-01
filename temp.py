#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import numpy as np 
import utils
import matplotlib.pyplot as plt
import subprocess

def run_correction():
    for i in range(0, 1):
        path_name = os.path.join(args.directory, f'NR2_GBReg_correction_{i}.csv')
        with open(path_name, 'w') as f:
            cmds = ['./datarot.py']
            utils.run_cmd(cmds, False, stdout=f)
        df = pd.read_csv(path_name)
        # df['error'] = df['predicted'] - df['angle']
        for col in df.columns:
            print(col)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for applying a rotational correction factor recursively')
    
    parser.add_argument('--directory', help='Directory', required=True)
    args = parser.parse_args()
    run_correction()