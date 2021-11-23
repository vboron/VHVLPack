#!/usr/bin/env python3
"""
Program:    add_correction_factor
File:       add_correction_factor.py
Version:    V1.0
Date:       11.23.2021
Function:   Use data from previous run to calculate a correction factor and create a new predicted value
Description:
============
Program uses the slope and intercept of the graph from the run and then applies these to create a corrected value for
the prediction.

Commandline input: 1) .csv file with data from previous run 
                   2) .csv file with the stats for the run
                   3) name of the output .csv
------------------------------------------------
"""

import os
import sys
import pandas as pd
import numpy as np
import math


# *************************************************************************
def correct_pred(prediction):
    """ Read the .csv file with the statistics for the run. Correct the prediction by using the slope and intercept.

        Inputs: prediction      -- the predicted angle
        Return: correction      -- the angle with the correction applied
                
        11.23.2021  Original   By: VAB
    """
    stat_col = ['pearson_a', 'pearson_o', 'mean_abs_err_a', 'mean_abs_err_o', 'RMSE', 'RMSE_o', 'RELRMSE_a', 
    'RELRMSE_o', 'best_ft_a', 'bf_slope_a', 'bf_int_a', 'best_ft_o', 'bf_int_o', 'bf_slope_o']

    stats = pd.read_csv(sys.argv[2], usecols=stat_col)

    m = stats['bf_slope_a']
    c = stats['bf_int_a']

    correction = round(((prediction-c)/m), 3)
    return correction


# *************************************************************************
def make_dataset_with_corrections():
   """ Read the .csv file with the data for the run. Call the correction function and then export the new dataset.
                
        11.23.2021  Original   By: VAB
    """
    # Specify column names for .csv file that will be made from the log files
    data_col = ['code', 'angle', 'predicted', 'error']
    

    # file with uncorrected data
    data_df = pd.read_csv(sys.argv[1], usecols=data_col)

    # file with statistics
 
    data_df['predicted'] = data_df['predicted'].apply(correct_pred)

    data_df['error'] = data_df['predicted'] - data_df['angle']

    return

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
result = make_dataset_with_corrections()

result.to_csv('{}.csv'.format(sys.argv[3]), index=False)

