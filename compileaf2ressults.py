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
    actual_df = calculate_packing_angles(actualdir)
    final_df = actual_df.merge(pred_df, on='code')
    return final_df

def postprocessing(df, directory, name):
    graphing.actual_vs_predicted_from_df(df, dataset, name, f'{name}_pa')
    graphing.sq_error_vs_actual_angle(
        dataset, df, f'{name}_sqerror_vs_actual')
    graphing.error_distribution(
        dataset, df, f'{name}_errordistribution')


# # *************************************************************************
parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--af2dir', required=True, help='directory of pdb files used for training model', type=str)
parser.add_argument('--actualdir', required=True, help='directory of pdb files used for testing model', type=str)
parser.add_argument('--graphname', required=True, help='name for the graphs', type=str)

args = parser.parse_args()
data_df = get_angle_from_af2_model(args.af2dir, args.actualdir)
postprocessing(data_df, args.af2dir, args.graphname)