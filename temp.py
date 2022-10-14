#!/usr/bin/python3

# Program can be run like this:  ./gbr_angle_prediction.py --trainset 'Everything' --testset 'new_data' 
# --modelname 'train_Everything_H100G_residues_considered_nosubsampling' 
# --graphname 'train_everything_test_abdbnew_nosubsampling'
# # *************************************************************************
import argparse
import pandas as pd


# *************************************************************************
def combine(in_with_code, in_with_pred, out):
    code_df = pd.read_csv(in_with_code)
    code_list = code_df['code'].to_list()

    pred_df = pd.read_csv(in_with_pred)
    print(pred_df)
    pred_df = pred_df[['code', 'predicted']]
    df = pred_df.loc[pred_df['code'].isin(code_list)]
    
    print(df)


# *************************************************************************
parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--in1', required=True, help='input csv', type=str)
parser.add_argument('--in2', required=True, help='input csv', type=str)
parser.add_argument('--out', required=True, help='output csv name', type=str)

args = parser.parse_args()
combine(args.in1, args.in2, args.out)

print('Bye bye bye!')