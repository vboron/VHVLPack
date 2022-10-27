#!/usr/bin/env python3

from graphing import *
import pandas as pd
import argparse
import os

def makegraphs(csv, output, dire):
    df = pd.read_csv(os.path.join(dire, csv))
    error_distribution(dire, df, f'{output}_ed')
    sq_error_vs_actual_angle(dire, df, f'{output}_sqe')
    actual_vs_predicted_from_df(df, dire, output, f'{output}_pa')


parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--dir', required=True)
parser.add_argument('--out', required=True)
parser.add_argument('--csv', required=True)
args = parser.parse_args()

makegraphs(args.csv, args.out, args.dir)