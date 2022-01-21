#!/usr/bin/env python3
"""
Function:   Produce scatter graph of predicted vs. actual packing angles and a file with the statistics for the run.
Description:
============
The program calculates and then outputs (as a .csv) all relevant statistical data for the run (mean error, RMSE,
RELRMSE, pearson's coefficient, and the best fit lines).

Commandline input: 1) .dat with columns
                   2) .csv file for all data
                   3) dataset name
                   4) directory where data will be saved
------------------------------------------------
"""

import os
import sys
import pandas as pd
import numpy as np
import re
import math
import subprocess
import matplotlib.pyplot as plt


# *************************************************************************
def find_normal_and_outliers():
    """ Function looks at data frame with prediction values and separates the data into two dataframes based
        on whether the predicted angles are withing a normal range or not.
        e.g. code,angle,predicted,error
             4YHI,-48.288,-44.388,3.9
             1QYG,-45.585,-44.701,0.884

        Return: df_n  -- Dataframe containing angles in normal range
                df_o  -- Dataframe containing angles out of normal range

        11.24.2021  Original   By: VAB
    """

    # define the boundaries for the range of angles that are not outliers
    min_norm = -48
    max_norm = -42

    # extract data where the predicted angle is within the normal range into a new dataframe
    df_n = df_a[df_a['predicted'].between(min_norm, max_norm)]

    # extract data where predicted angles are outside of the normal range and add into a new dataframe
    df_o1 = df_a[df_a['predicted'] >= max_norm]
    df_o2 = df_a[df_a['predicted'] <= min_norm]
    df_o = pd.concat([df_o1, df_o2])

    # reset the indexes (as the original ones will be kept) and export as .csv files

    df_n = df_n.reset_index()
    path_n = os.path.join(cwd, directory, (f'normal_{sys.argv[3]}.csv'))
    df_n.to_csv(path_n, index=False)

    df_o = df_o.reset_index()
    path_o = os.path.join(cwd, directory, (f'outlier_{sys.argv[3]}.csv'))
    df_o.to_csv(path_o, index=False)

    return df_n, df_o

# *************************************************************************
def find_stats(df_o):
    """ Function calculates and compiles relevant statistical data related to the (ML) run that the data is from.

        Input:  df_o        -- Dataframe containing angles out of normal range
        Return: stats_df    -- Dataframe with statistics for the model performance

        11.24.2021  Original   By: VAB
    """

    # create a deep copy to prevent modification of the global variable
    df_a_temp = df_a.copy()

    # Calculate the Root Mean Square Error
    df_a_temp['sqerror'] = np.square( df_a_temp['error'])
    sum_sqerror =  df_a_temp['sqerror'].sum()
    average_error = sum_sqerror / int( df_a_temp['code'].size)
    RMSE = math.sqrt(average_error)

    # Call the RELRMSE.py script which converts the RMSE into Relative RMSE
    getResult = lambda rmse: subprocess.check_output(['./RELRMSE.py', f'{sys.argv[2]}', 'graph.dat', rmse])
    RELRMSE   = getResult(str(RMSE)).decode('ascii')

    # gather all of the relevant run statistics into a single table
    # .corr() returns the correlation between two columns
    pearson_a =  df_a_temp['angle'].corr( df_a_temp['predicted'])

    mean_abs_err_a =  df_a_temp['error'].mean()

    # everything is done for outliers, if they exist
    num_outliers = int(df_o['code'].size)
    if num_outliers != 0:
        df_o['sqerror'] = np.square(df_o['error'])
        sum_sqerror_o = df_o['sqerror'].sum()
        average_error_o = sum_sqerror_o/num_outliers
        RMSE_o = math.sqrt(average_error_o)
        RELRMSE_o = getResult(str(RMSE_o)).decode('ascii')
        pearson_o = df_o['angle'].corr(df_o['predicted'])
        mean_abs_err_o = df_o['error'].mean()
    else:
        average_error_o = None
        RMSE_o = None
        RELRMSE_o = None
        pearson_o = None
        mean_abs_err_o = None

    stat_data = [pearson_a, pearson_o, mean_abs_err_a, mean_abs_err_o, RMSE, RMSE_o, RELRMSE, RELRMSE_o]
    stat_col = ['pearson_a', 'pearson_o', 'mean_abs_err_a', 'mean_abs_err_o', 'RMSE', 'RMSE_o', 'RELRMSE_a',
    'RELRMSE_o']

    stats_df = pd.DataFrame(data=[stat_data], columns=stat_col)

    return stats_df


# *************************************************************************
def plot_scatter(file_o, file_n, stat_df, file_a):
    """ Create a scatter plot where outliers and normal range values are different colors. There is also a best fit
        line for outliers and for the whole dataset, as well as a y=x line for comparisons. Axis titles and max/mins
        are set. Text displays the legend, equation of best fit lines, and the RELRMSE for the whole set and the
        outliers. Graphs are exported as a .png.

        Inputs: file_o    -- Dataframe containing predicted and actual angles for outliers
                file_n    -- Dataframe containing predicted and actual angles for normal range values
                stat_df  -- Dataframe containing the statistical information from the run

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

    x2 = file_n['angle']
    y2 = file_n['predicted']

    x3 = file_a['angle']
    y3 = file_a['predicted']

    m3, b3 = np.polyfit(x3, y3, 1)
    plt.plot(x3, m3 * x3 + b3, color=c4, linestyle='dashed', linewidth=1)


    # Plot the outliers and normal values as scatter plots
    plt.scatter(x2, y2, s=2, color=c2)

    axes = plt.gca()

    # Sets the maximum and minimum values for the axes
    axes.set_xlim([-62, -30])
    axes.set_ylim([-60, -30])

    axes.axline((0, 0), (1, 1), color='k')
    # y_counter = -60
    # while y_counter < -30:
    #     x_counter = y_counter
    #     # Plot a y=x line in black
    #     plt.plot(x_counter, y_counter, 'k')
    #     y_counter + 1

    # Sets the axes labels
    plt.xlabel('Calculated Angle')
    plt.ylabel('Predicted Angle')

    # Adds graph annotations
    plt.text(s='Line: y=x', x=-61, y=-32, fontsize=8)

    plt.text(s='Best fit (all): y={:.3f}x+{:.3f}'.format(m3, b3), x=-61, y=-33, fontsize=8, color=c4)
    plt.text(s='RELRMSE (all): {:.3}'.format(float(stat_df['RELRMSE_a'])), x=-61, y=-34, fontsize=8)


    plt.text(s='-48 < Normal Values < -42', x=-61, y=-38, fontsize=8, color=c2)

    # Adds graph title
    plt.suptitle('ML prediction of VHVL packing angle (set {})'.format(sys.argv[3]), fontsize=14)

    plt.tight_layout()

    # add best fit data to dataframe and export the dataframe
    # add best fit lines to statistics dataframe
    best_ft_a = 'y={:.3f}x+{:.3f}'.format(m3, b3)

    stat_df['best_ft_a'] = best_ft_a
    stat_df['bf_slope_a'] = m3
    stat_df['bf_int_a'] = b3

    num_outliers = int(file_o['code'].size)
    if num_outliers != 0:
        # Angle values are designated axis names
        x1 = file_o['angle']
        y1 = file_o['predicted']

        # Line of best fit is calculated
        m1, b1 = np.polyfit(x1, y1, 1)
        plt.plot(x1, m1 * x1 + b1, color=c3, linestyle='dashed', linewidth=1)
        plt.scatter(x1, y1, s=2, color=c1)
        plt.text(s='RELRMSE (outliers): {:.3}'.format(float(stat_df['RELRMSE_o'])), x=-61, y=-37, fontsize=8)
        plt.text(s='Best fit (outliers): y={:.3f}x+{:.3f}'.format(m1, b1), x=-61, y=-36, fontsize=8, color=c3)
        plt.text(s='Outliers', x=-61, y=-35, fontsize=8, color=c1)
        best_ft_o = 'y={:.3f}x+{:.3f}'.format(m1, b1)
        stat_df['best_ft_o'] = best_ft_o
        stat_df['bf_int_o'] = b1
        stat_df['bf_slope_o'] = m1

    path_stats = os.path.join(cwd, directory, (f'{sys.argv[3]}_run_stats.csv'))
    stat_df.to_csv(path_stats, index=False)

    # Exports the figure as a .png file
    path_fig = os.path.join(cwd, directory, f'{sys.argv[3]}.tiff')
    plt.savefig(path_fig, format='tiff')
    plt.show()

    return

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
col = []
for i in open(sys.argv[1]).readlines():
    i = i.strip('\n')
    col.append(i)
cwd = os.getcwd()
directory = sys.argv[4]
df_a = pd.read_csv(sys.argv[2], usecols=col)

norm_df, out_df = find_normal_and_outliers()

statistics_df = find_stats(out_df)

plot = plot_scatter(out_df, norm_df, statistics_df, df_a.copy())
