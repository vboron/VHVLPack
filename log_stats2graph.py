#!/usr/bin/env python3
"""
Program:    log_stats2graph
File:       log_stats2graph.py
Version:    V2.0
Date:       11.23.2021
Function:   Produce scatter graph of predicted vs. actual packing angles and a file with the statistics for the run.
Description:
============
Program extracts lines of statistics from .log files produced using MLP through Weka framework and converts them into a
dataframe that is then plotted. Outliers and normal values are plotted separetly, best fit lines and RELRMSE determined
for outliers and the full dataset. The program also calculates and then outputs (as a .csv) all relevant statistical
data for the run (mean error, RMSE, RELRMSE, pearson's coefficient, and the best fit lines).

Commandline input: 1) Directory where the .log files are
                   2) Number of Hidden layers
                   3) Name for statistics .csv
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
def stats_to_df():
    """ Read the directory and extract .log files. For each log file, extract the predicted and the actual angle, then
        calculate the RMSE. Call RELRMSE.py to calculate the RELRMSE from the RMSE. Export as a .csv file.

        Return: df_o      -- Dataframe containing predicted and actual angles for outliers
                RELRMSE_o -- RELRMSE for outliers
                df_n      -- Dataframe containing predicted and actual angles for normal range values
                df_a      -- Dataframe containing predicted and actual angles for all values
                RELRMSE   -- RELRMSE for whole dataset
                stats_df  -- Dataframe containing the statistical information from the run 
                
        14.07.2021  Original   By: VAB
    """
    # Take the directory where the .log files are from commandline
    direct = sys.argv[1]

    # Specify column names for .csv file that will be made from the log files
    col = ['code', 'angle', 'predicted', 'error']

    all_data = []
    files = []
    out_data = []
    normal_data = []

    # Open the directory and make a list of .log files that are in there
    for file in os.listdir(direct):
        if file.endswith("{}_test.log".format(sys.argv[2])):
            files.append('{}/{}'.format(direct, file))

    # Open each log file in the directory and find the relevant information
    for log_file in files:
        with open(log_file) as text_file:
            for line in text_file:
                if str(line).strip().startswith('1'):
                    line = re.sub(' +', ' ', line)
                    line = line.strip()
                    line_list = line.split(' ')
                    name = log_file.split('_')
                    name = name[2].split('/')
                    code = name[1]
                    pred = float(line_list[2])
                    angle = float(line_list[1])
                    error = float(line_list[3])
                    all = [code, angle, pred, error]
                    all_data.append(all)

                    # Find files that are out of the normal range and will be considered outliers
                    if not -48 < int(pred) < -42:
                        out = [code, angle, pred, error]
                        out_data.append(out)
                    else:
                        normal = [code, angle, pred, error]
                        normal_data.append(normal)

    # Make .csv files for all of the data, splitting it into files that have all the data, only outliers, and only the
    # data withing the 'norm'
    df_a = pd.DataFrame(data=all_data, columns=col)
    df_a.to_csv('all_{}.csv'.format(sys.argv[2]), index=False)

    # Calculate the Root Mean Square Error
    df_a['sqerror'] = np.square(df_a['error'])
    sum_sqerror = df_a['sqerror'].sum()
    average_error = sum_sqerror / int(df_a['code'].size)
    RMSE = math.sqrt(average_error)
    print('All RMSE:', RMSE)

    df_o = pd.DataFrame(data=out_data, columns=col)
    df_o.to_csv('outlier_{}.csv'.format(sys.argv[2]), index=False)

    df_o['sqerror'] = np.square(df_o['error'])
    sum_sqerror_o = df_o['sqerror'].sum()
    average_error_o = sum_sqerror_o/int(df_o['code'].size)
    RMSE_o = math.sqrt(average_error_o)
    print('Outlier RMSE:', RMSE_o)

    df_n = pd.DataFrame(data=normal_data, columns=col)
    df_n.to_csv('normal_{}.csv'.format(sys.argv[2]), index=False)

    # Call the RELRMSE.py script which converts the RMSE into Relative RMSE

    # getResult = lambda rmse: subprocess.check_output(['./RELRMSE.py', 'all_{}.csv'.format(sys.argv[2]), 'graph.dat', rmse ])
    # RELRMSE   = getResult(RMSE)
    # RELRMSE_o = getResult(RMSE_o)
    RELRMSE   = float(subprocess.check_output(['./RELRMSE.py', 'all_{}.csv'.format(sys.argv[2]), 'graph.dat', str(RMSE)  ]))
    RELRMSE_o = float(subprocess.check_output(['./RELRMSE.py', 'all_{}.csv'.format(sys.argv[2]), 'graph.dat', str(RMSE_o)]))

    # gather all of the relevant run statistics into a single table
    # .corr() returns the correlation between two columns 
    pearson_a = df_a['angle'].corr(df_a['predicted'])
    pearson_o = df_o['angle'].corr(df_o['predicted'])

    mean_abs_err_a = df_a['error'].mean()
    mean_abs_err_o = df_o['error'].mean()

    stat_data = [pearson_a, pearson_o, mean_abs_err_a, mean_abs_err_o, RMSE, RMSE_o, RELRMSE, 
    RELRMSE_o]
    stat_col = ['pearson_a', 'pearson_o', 'mean_abs_err_a', 'mean_abs_err_o', 'RMSE', 'RMSE_o', 'RELRMSE_a', 
    'RELRMSE_o']

    stats_df = pd.DataFrame(data=[stat_data], columns=stat_col)

    return df_o, RELRMSE_o, df_n, df_a, RELRMSE, stats_df


# *************************************************************************
def plot_scatter(file_o, RELRMSE_o, file_n, file_a, RELRMSE_a, stat_df):
    """ Create a scatter plot where outliers and normal range values are different colors. There is also a best fit
        line for outliers and for the whole dataset, as well as a y=x line for comparisons. Axis titles and max/mins
        are set. Text displays the legend, equation of best fit lines, and the RELRMSE for the whole set and the
        outliers. Graphs are exported as a .png.

        Inputs: file_o    -- Dataframe containing predicted and actual angles for outliers
                RELRMSE_o -- RELRMSE for outliers
                file_n    -- Dataframe containing predicted and actual angles for normal range values
                file_a    -- Dataframe containing predicted and actual angles for all values
                RELRMSE   -- RELRMSE for whole dataset
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
    plt.suptitle('ML prediction of VHVL packing angle (HL = {})'.format(sys.argv[2]), fontsize=14)

    plt.tight_layout()

    # add best fit data to dataframe and export the dataframe
    # add best fit lines to statistics dataframe
    best_ft_a = 'y={:.3f}x+{:.3f}'.format(m3, b3)
    best_ft_o = 'y={:.3f}x+{:.3f}'.format(m1, b1)

    stat_df['best_ft_a'] = best_ft_a
    stat_df['bf_slope_a'] = m3
    stat_df['bf_int_a'] = b3
    
    stat_df['best_ft_o'] = best_ft_o
    stat_df['bf_int_o'] = b1
    stat_df['bf_slope_o'] = m1

    stat_df.to_csv('run_stats_{}_HL{}.csv'.format(sys.argv[3], sys.argv[2]), index=False)

    # Exports the figure as a .png file
    plt.savefig('HL{}.tiff'.format(sys.argv[2]), format='tiff')
    plt.show()

    return

# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
frame_o, data_o, frame_n, frame_a, data_a, run_data = stats_to_df()

plot = plot_scatter(frame_o, data_o, frame_n, frame_a, data_a, run_data)
