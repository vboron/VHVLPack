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
        cmds = ['./datarot.py', '-o', path_name]
        utils.run_cmd(cmds, False)
        df = pd.read_csv(path_name)
        df['error'] = df['predicted'] - df['angle']

        # TODO: write part which will graph the rotated values and output the slope then run it again
 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for applying a rotational correction factor recursively')
    
    parser.add_argument('--directory', help='Directory', required=True)
    args = parser.parse_args()
    run_correction()