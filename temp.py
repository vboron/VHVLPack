#!/usr/bin/python3
import pandas as pd
import argparse
from graphing import angle_distribution as angd

def runf(csv, dir):
    df_all = pd.read_csv(csv)
    df = df_all[['code', 'angle']]
    angd(dir, df, 'sept_ang_dist')

parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--csv', required=True, type=str)
parser.add_argument('--dir', required=True, type=str)

args = parser.parse_args()
runf(args.csv, args.dir)