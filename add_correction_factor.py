#!/usr/bin/env python3
"""
Function:   Use data from previous run to calculate a correction factor and create a new predicted value
Description:
============
Program uses the slope and intercept of the graph from the run and then applies these to create a corrected value for
the prediction.
------------------------------------------------
"""
import os
import pandas as pd
import argparse


def make_dataset_with_corrections(directory, input_csv, stats_csv):
    """ Read the .csv file with the data for the run. Call the correction function and then export the new dataset.

    11.23.2021  Original   By: VAB
    """
    stats = pd.read_csv(os.path.join(directory, stats_csv))
    # y = mx + c
    m = stats['slope']
    c = stats['intercept']

    # file with uncorrected data
    data_df = pd.read_csv(os.path.join(directory, input_csv))

    correction = (lambda pred : round(((pred * m) + c), 3))
    data_df['predicted'] = data_df['predicted'].apply(correction)
    data_df['error'] = data_df['predicted'] - data_df['angle']
    return data_df

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
    parser.add_argument('--directory', help='Directory where files will', required=True)
    parser.add_argument('--csv_input', help='File that was the input to the method', required=True)
    parser.add_argument('--csv_stats', help='Table with output stats', required=True)
    parser.add_argument('--output_name', help='Name for outputted correction', required=True)
    args = parser.parse_args()

    result = make_dataset_with_corrections(args.directory, args.csv_input, args.csv_stats)
    path = os.path.join(args.directory, args.output_name)
    result.to_csv(f'{path}.csv', index=False)
