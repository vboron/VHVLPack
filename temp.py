#!/usr/bin/python3
import pandas as pd
import argparse

def combine_dfs(code_file, pred_file):
    code_df = pd.read_csv(code_file)
    pred_df = pd.read_csv(pred_file)
    final = code_df.merge(pred_df, on='code')
    final = final[['code', 'predicted']]
    print(final)
    # final.to_csv('')

parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--code', required=True, type=str)
parser.add_argument('--pred', required=True, type=str)

args = parser.parse_args()
combine_dfs(args.code, args.pred)