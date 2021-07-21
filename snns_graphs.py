#!/usr/bin/env python3
"""
Program:    snns_graphs
File:       snns_graphs.py

Version:    V1.0
Date:       07.21.2021
Function:   Takes data from SNNS and plots predicted vs actual, frequency of errors, and square error vs actual angle.

Description:
============
Program takes a .csv file containing pdb code, actual and predicted angles and calculates the error, RMSE, RELRMSE.
It then uses this data to plot three graphs: actual vs predicted angle, the frequency of errors, and suared error
vs actual angle.

Commandline input: 1) .csv file containing snns data
                   2) Name for dataset


------------------------------------------------
"""

import sys
import pandas as pd
import numpy as np
import math
import subprocess
import matplotlib.pyplot as plt

# *************************************************************************
def read_csv():

    # .csv column names
    col1 = ['code', 'pred', 'angle']

    # Read .csv file as a dataframe
    snns_df = pd.read_csv(sys.argv[1], usecols=col1)

    # Add a column that has the error in angle prediction
    snns_df['error'] = snns_df['angle'] - snns_df['pred']

    # Make column for squared error
    snns_df['sqerror'] = snns_df['error']**2

    # Sum all of the squared errors
    sum_sqerror = float(snns_df['sqerror'].sum())

    # Average the square error
    average_error = sum_sqerror / int(snns_df['code'].size)

    # Calculate the RMSE
    RMSE = str(math.sqrt(average_error))

    # Call the program that calculates the RELRMSE
    RELRMSE = subprocess.check_output(['python3', 'RELRMSE.py', '{}'.format(sys.argv[1]), 'snns_graph.dat', RMSE])

    return snns_df, RELRMSE


# *************************************************************************
def actual_vs_predicted(data, RELRMSE):
    # Color points
    c1 = 'rosybrown'

    # Color of best fit line
    c2 = 'firebrick'

    # Assign axis
    x1 = data['angle']
    y1 = data['pred']

    plt.scatter(x1, y1, s=2, color=c1)

    # Make the line of best fit
    m1, b1 = np.polyfit(x1, y1, 1)
    plt.plot(x1, m1 * x1 + b1, color=c2, linestyle='dashed', linewidth=1)

    # Plot a y=x line in black
    plt.plot(x1, x1 + 0, '-k')

    axes = plt.gca()

    # Sets the maximum and minimum values for the axes
    axes.set_xlim([-62, -30])
    axes.set_ylim([-60, -30])

    # Sets the axes labels
    plt.xlabel('Calculated Angle')
    plt.ylabel('Predicted Angle')

    plt.text(s='Line: y=x', x=-61, y=-32, fontsize=8)
    plt.text(s='Best fit: y={:.3f}x+{:.3f}'.format(m1, b1), x=-61, y=-33, fontsize=8, color=c2)
    plt.text(s='RELRMSE: {:.3}'.format(float(RELRMSE)), x=-61, y=-34, fontsize=8)

    # Adds graph title
    plt.suptitle('Predictions of packing angles using SNNS for {} dataset'.format(sys.argv[2]), fontsize=14)


    plt.tight_layout()

    # Exports the figure as a .png file
    plt.savefig('snns_{}_dataset_predvsactual.png'.format(sys.argv[2]), format='png')
    # plt.show()

    return


# *************************************************************************
def graph_error(data):

    # Round each error value to 1dp
    data['error'] = data['error'].round(decimals=1)

    # Reads data as a numpy array
    error = np.array(data['error'], dtype='float')

    # Counting occurrence of each value
    x, y = np.unique(error, return_counts=True)
    plt.plot(x, y, color='rosybrown')

    plt.xlabel('Error in Prediction')
    plt.ylabel('Frequency')

    plt.suptitle('Distribution of errors when using SNNS for {} dataset'.format(sys.argv[2]), fontsize=14)

    # plt.show()

    plt.savefig('snns_{}_dataset_errors.png'.format(sys.argv[2]), format='png')

    return


# *************************************************************************
def graph_sq_error(data):

    x = data['angle']
    y = data['sqerror']

    plt.xlabel('Actual Packing Angle')
    plt.ylabel('Square of Error ')

    plt.scatter(x, y, s=2, color='rosybrown')
    plt.suptitle('Square error vs actual packing angle using SNNS for {} dataset'.format(sys.argv[2]), fontsize=12)

    # plt.show()
    plt.savefig('snns_{}_dataset_sqerrors.png'.format(sys.argv[2]), format='png')

    return
# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

df, dataRELRMSE = read_csv()

a_vs_p = actual_vs_predicted(df, dataRELRMSE)

error_graph = graph_error(df)

sqerror = graph_sq_error(df)
