#!/usr/bin/python3


# # *************************************************************************
import os
import argparse
import shutil
import utils
import encode_res_calc_angles as erca
import nonred
import graphing
from sklearn_methods import *
import numpy as np
from encode_res_calc_angles import calculate_packing_angles

def get_angle_from_af2_model(af2dir, actualdir):
    pred_df = calculate_packing_angles(af2dir)
    pred_df = pred_df.rename({'angle': 'predicted'}, axis=1)
    print(pred_df)
    actual_df = calculate_packing_angles(actualdir)
    print(actual_df)
    final_df = actual_df.merge(pred_df, on='code')
    print(final_df)


# # *************************************************************************
parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--af2dir', required=True, help='directory of pdb files used for training model', type=str)
parser.add_argument('--actualdir', required=True, help='directory of pdb files used for testing model', type=str)

args = parser.parse_args()
get_angle_from_af2_model(args.af2dir, args.actualdir)