#!/usr/bin/env python3
"""
Program:    stats2graph
File:       stats2graph.py

Version:    V1.0
Date:       10.20.2021
Function:   Scatter graph of predicted vs. actual packing angles for snns data

Description:
============
Program extracts lines of statistics from .csv file produced using our snns (papa or newpapa) and converts them into
dataframe that is then plotted. Outliers and normal values are plotted separetly, best fit lines and RELRMSE determined
for outliers and the full dataset.

Commandline input: 1) .csv file with actual and predicted angles
                   2) name that will be added into the created .csv files
                   3) .dat with column names 
                   4) method used to get data


------------------------------------------------
"""
# *************************************************************************
# Import libraries
import os
import sys
import re
import pandas as pd
import numpy as np
import math
import subprocess
import matplotlib.pyplot as plt


# *************************************************************************
def stats_to_df():
    """ Read the directory and extract .log files. For each log file, extract the predicted and the actual angle, then
        calculate the RMSE. Call RELRMSE.py to calculate the RELRMSE from the RMSE. Export as a .csv file.

        Return:

        14.07.2021  Original   By: VAB
    """
    # Open file where the snns results and actual values are
    file  = sys.argv[1]

    # Specify column names
    col = []
    for i in open(sys.argv[3]).readlines():
        i = i.strip('\n')
        col.append(i)

    # Make .csv files for all of the data, splitting it into files that have all the data, only outliers, and only the
    # data withing the 'norm'
    df_all = pd.read_csv(file, usecols=col)
    df_all.to_csv('all_{}.csv'.format(sys.argv[2]), index=False)

    # Calculate the Root Mean Square Error
    sum_sqerror = float(df_a['sqerror'].sum())
    average_error = sum_sqerror / int(df_a['code'].size)
    RMSE = str(math.sqrt(average_error))
    print('All RMSE:', RMSE)

    df_norm = df_all[-48 <= df_all['pred'] <= -42]
    df_n.to_csv('normal_{}.csv'.format(sys.argv[2]), index=False)

    df_outlier1 = df_all[df[all] < -48]
    df_outlier2 = df_all[df[all] > -42]
    df_outliers = pd.concat([df_outlier1, df_outlier2], ignore_index=True)
    df_outliers.to_csv('outlier_{}.csv'.format(sys.argv[2]), index=False)

    sum_sqerror_o = float(df_o['sqerror'].sum())
    average_error_o = sum_sqerror_o/int(df_o['code'].size)
    RMSE_o = str(math.sqrt(average_error_o))
    print('Outlier RMSE:', RMSE_o)

    # Call the RELRMSE.py script which converts the RMSE into Relative RMSE
    RELRMSE = subprocess.check_output(['./RELRMSE.py', 'all_{}.csv'.format(sys.argv[2]), sys.argv[3], RMSE])
    RELRMSE_o = subprocess.check_output(['./RELRMSE.py', 'all_{}.csv'.format(sys.argv[2]),
                                         sys.argv[3], RMSE_o])

    return df_outliers, RELRMSE_o, df_norm, df_all, RELRMSE


# *************************************************************************
def plot_scatter(file_o, RELRMSE_o, file_n, file_a, RELRMSE_a):
    """ Create a scatter plot where outliers and normal range values are different colors. There is also a best fit
        line for outliers and for the whole dataset, as well as a y=x line for comparisons. Axis titles and max/mins
        are set. Text displays the legend, equation of best fit lines, and the RELRMSE for the whole set and the
        outliers. Graphs are exported as a .png.

        Inputs: file_o    -- Dataframe containing predicted and actual angles for outliers
                RELRMSE_o -- RELRMSE for outliers
                file_n    -- Dataframe containing predicted and actual angles for normal range values
                file_a    -- Dataframe containing predicted and actual angles for all values
                RELRMSE   -- RELRMSE for whole dataset

        14.07.2021  Original   By: VAB
    """
    # Color of outlier points
    c1 = 'rosybrown'

    # Color of normal points
    c2 = 'mediumturquoise'

    # Color of outlier best fit line
    c3 = 'firebrick'

    # Color of best fit line for full set
    c4 = 'teal'

    # Angle values are converted into float format
    file_o['angle'] = file_o['angle'].apply(lambda x: float(x))
    file_o['predicted'] = file_o['predicted'].apply(lambda y: float(y))

    # Angle values are designated axis names
    x1 = file_o['angle']
    y1 = file_o['predicted']

    # Line of best fit is calculated
    m1, b1 = np.polyfit(x1, y1, 1)
    plt.plot(x1, m1 * x1 + b1, color=c3, linestyle='dashed', linewidth=1)

    file_n['angle'] = file_n['angle'].apply(lambda x: float(x))
    file_n['predicted'] = file_n['predicted'].apply(lambda y: float(y))
    x2 = file_n['angle']
    y2 = file_n['predicted']

    file_a['angle'] = file_a['angle'].apply(lambda x: float(x))
    file_a['predicted'] = file_a['predicted'].apply(lambda y: float(y))
    x3 = file_a['angle']
    y3 = file_a['predicted']

    m3, b3 = np.polyfit(x3, y3, 1)
    plt.plot(x3, m3 * x3 + b3, color=c4, linestyle='dashed', linewidth=1)

    # Plot a y=x line in black
    plt.plot(x1, x1 + 0, '-k')

    # Plot the outliers and normal values as scatter plots
    plt.scatter(x1, y1, s=2, color=c1)
    plt.scatter(x2, y2, s=2, color=c2)

    axes = plt.gca()

    # Sets the maximum and minimum values for the axes
    axes.set_xlim([-62, -30])
    axes.set_ylim([-60, -30])

    # Sets the axes labels
    plt.xlabel('Calculated Angle')
    plt.ylabel('Predicted Angle')

    # Adds graph annotations
    plt.text(s='Line: y=x', x=-61, y=-32, fontsize=8)

    plt.text(s='Best fit (all): y={:.3f}x+{:.3f}'.format(m3, b3), x=-61, y=-33, fontsize=8, color=c4)
    plt.text(s='RELRMSE (all): {:.3}'.format(float(RELRMSE_a)), x=-61, y=-34, fontsize=8)

    plt.text(s='Outliers', x=-61, y=-35, fontsize=8, color=c1)
    plt.text(s='Best fit (outliers): y={:.3f}x+{:.3f}'.format(m1, b1), x=-61, y=-36, fontsize=8, color=c3)
    plt.text(s='RELRMSE (outliers): {:.3}'.format(float(RELRMSE_o)), x=-61, y=-37, fontsize=8)

    plt.text(s='-48 < Normal Values < -42', x=-61, y=-38, fontsize=8, color=c2)

    # Adds graph title
    plt.suptitle('Predictions vs. actual packing angles ({})'.format(sys.argv[4]), fontsize=14)

    plt.tight_layout()

    # Exports the figure as a .png file
    plt.savefig('{}.tiff'.format(sys.argv[2]), format='tiff')
    plt.show()

    return

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
frame_o, data_o, frame_n, frame_a, data_a = stats_to_df()

plot = plot_scatter(frame_o, data_o, frame_n, frame_a, data_a)
