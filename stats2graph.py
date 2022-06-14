#!/usr/bin/env python3
"""
Function:   Produce scatter graph of predicted vs. actual packing angles and a file with the statistics for the run.
Description:
============
The program calculates and then outputs (as a .csv) all relevant statistical data for the run (mean error, RMSE,
RELRMSE, pearson's coefficient, and the best fit lines).
------------------------------------------------
"""

import argparse
import os
import pandas as pd
import numpy as np
import utils
import math
import matplotlib.pyplot as plt


# *************************************************************************
def find_normal_and_outliers(directory, input_csv):
    """ Function looks at data frame with prediction values and separates the data into two dataframes based
        on whether the predicted angles are withing a normal range or not.
        e.g. code,angle,predicted,error
             4YHI,-48.288,-44.388,3.9
             1QYG,-45.585,-44.701,0.884

        Return: df_n  -- Dataframe containing angles in normal range
                df_o  -- Dataframe containing angles out of normal range

        11.24.2021  Original   By: VAB
    """

    df_a = pd.read_csv(os.path.join(directory, input_csv))

    # define the boundaries for the range of angles that are not outliers
    # -48 and -42 are chosen based on angle population graphs
    min_norm = -48
    max_norm = -42

    # extract data where the predicted angle is within the normal range into a new dataframe
    df_n = df_a[df_a['angle'].between(min_norm, max_norm)]

    # extract data where predicted angles are outside of the normal range and add into a new dataframe
    df_o1 = df_a[df_a['angle'] >= max_norm]
    df_o2 = df_a[df_a['angle'] <= min_norm]
    df_o = pd.concat([df_o1, df_o2])

    # reset the indexes (as the original ones will be kept) and export as .csv files

    df_n = df_n.reset_index()
    # path_n = os.path.join(directory, (f'{norm_name}.csv'))
    # df_n.to_csv(path_n, index=False)

    df_o = df_o.reset_index()
    # path_o = os.path.join(directory, (f'{out_name}.csv'))
    # df_o.to_csv(path_o, index=False)

    return df_a, df_n, df_o

# *************************************************************************


def find_stats(directory, input_csv, df_a, df_o):
    """ Function calculates and compiles relevant statistical data related to the (ML) run that the data is from.

        Input:  df_o        -- Dataframe containing angles out of normal range
        Return: stats_df    -- Dataframe with statistics for the model performance

        11.24.2021  Original   By: VAB
    """

    # create a deep copy to prevent modification of the global variable
    df_a_temp = df_a.copy()

    # Calculate the Root Mean Square Error
    df_a_temp['sqerror'] = np.square(df_a_temp['error'])
    sum_sqerror = df_a_temp['sqerror'].sum()
    average_error = sum_sqerror / int(df_a_temp['angle'].size)
    rmse = math.sqrt(average_error)

    os.path.join(directory, input_csv)

    # Call the utils.calc_rmse script which converts the RMSE into Relative RMSE
    def getResult(rmse): return utils.calc_relemse(
        os.path.join(directory, input_csv), rmse)
    relrmse = getResult(rmse)

    # gather all of the relevant run statistics into a single table
    # .corr() returns the correlation between two columns
    pearson_a = df_a_temp['angle'].corr(df_a_temp['predicted'])

    mean_abs_err_a = df_a_temp['error'].abs().mean()
    stat_data_all = [pearson_a, mean_abs_err_a, rmse, relrmse]
    # everything is done for outliers, if they exist
    num_outliers = int(df_o['angle'].size)

    stat_data_out = []
    stat_col = ['pearson', 'error', 'RMSE', 'RELRMSE']
    print('outliers:', df_o)
    if num_outliers != 0:
        df_o['sqerror'] = np.square(df_o['error'])
        sum_sqerror_o = df_o['sqerror'].sum()
        average_error_o = sum_sqerror_o/num_outliers
        rmse_o = math.sqrt(average_error_o)
        relrmse_o = getResult(rmse_o)
        pearson_o = df_o['angle'].corr(df_o['predicted'])
        mean_abs_err_o = df_o['error'].abs().mean()
        stat_data_out.append(pearson_o)
        stat_data_out.extend([mean_abs_err_o, rmse_o, relrmse_o])
        print('outlier loop:', stat_data_out)

    print(stat_data_all)
    print(stat_data_out)
    stats_all = pd.DataFrame(data=[stat_data_all], columns=stat_col)
    stats_out = pd.DataFrame(data=[stat_data_out], columns=stat_col)
    return stats_all, stats_out


# *************************************************************************
def plot_scatter(directory, file_o, file_n, stat_df_all, stat_df_out, file_a, stats_csv_name, graph_name):
    """ Create a scatter plot where outliers and normal range values are different colors. There is also a best fit
        line for outliers and for the whole dataset, as well as a y=x line for comparisons. Axis titles and max/mins
        are set. Text displays the legend, equation of best fit lines, and the RELRMSE for the whole set and the
        outliers. Graphs are exported as a .jpg.

        Inputs: file_o    -- Dataframe containing predicted and actual angles for outliers
                file_n    -- Dataframe containing predicted and actual angles for normal range values
                stat_df  -- Dataframe containing the statistical information from the run

        14.07.2021  Original   By: VAB
    """
    plt.figure()
    # Color of outlier points
    # TODO rename colors to something like "col_bestfit" etc.
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
    # axes.autoscale(tight=True)
    axes.set_xlim([-65, -25])
    axes.set_ylim([-65, -25])

    axes.axline((0, 0), (1, 1), color='k')

    # Sets the axes labels
    plt.xlabel('Actual interface angle')
    plt.ylabel('Predicted interface angle')

    # Adds graph annotations
    plt.text(s='Line: y=x', x=-61, y=-32, fontsize=8)

    plt.text(s='Best fit (all): y={:.3f}x+{:.3f}'.format(m3, b3),
             x=-61, y=-33, fontsize=8, color=c4)
    plt.text(s='RELRMSE (all): {:.3}'.format(
        float(stat_df_all['RELRMSE'])), x=-61, y=-34, fontsize=8)
    plt.text(s='-48 < Normal Values < -42', x=-61, y=-38, fontsize=8, color=c2)

    plt.tight_layout()

    # add best fit data to dataframe and export the dataframe
    # add best fit lines to statistics dataframe
    best_ft_a = 'y={:.3f}x+{:.3f}'.format(m3, b3)

    stat_df_all['fit'] = best_ft_a
    stat_df_all['slope'] = m3
    stat_df_all['intercept'] = b3

    num_outliers = int(file_o['angle'].size)
    if num_outliers != 0:
        # Angle values are designated axis names
        x1 = file_o['angle']
        y1 = file_o['predicted']

        # Line of best fit is calculated
        m1, b1 = np.polyfit(x1, y1, 1)
        plt.plot(x1, m1 * x1 + b1, color=c3, linestyle='dashed', linewidth=1)
        plt.scatter(x1, y1, s=2, color=c1)
        plt.text(s='RELRMSE (outliers): {:.3}'.format(
            float(stat_df_out['RELRMSE'])), x=-61, y=-37, fontsize=8)
        plt.text(s='Best fit (outliers): y={:.3f}x+{:.3f}'.format(
            m1, b1), x=-61, y=-36, fontsize=8, color=c3)
        plt.text(s='Outliers', x=-61, y=-35, fontsize=8, color=c1)
        best_ft_o = 'y={:.3f}x+{:.3f}'.format(m1, b1)
        stat_df_out['fit'] = best_ft_o
        stat_df_out['slope'] = m1
        stat_df_out['intercept'] = b1

    path_stats_all = os.path.join(directory, f'{stats_csv_name}_all.csv')
    path_stats_out = os.path.join(directory, f'{stats_csv_name}_out.csv')
    stat_df_all.to_csv(path_stats_all, index=False)
    stat_df_out.to_csv(path_stats_out, index=False)

    # Exports the figure as a .jpg file
    path_fig = os.path.join(directory, f'{graph_name}.jpg')
    plt.savefig(path_fig, format='jpg')
    plt.close()

    return m3, b3


def create_stats_and_graph(directory, csv_input, name_stats, name_graph):
    all_df, norm_df, out_df = find_normal_and_outliers(directory, csv_input)

    stat_df_all, stats_df_out = find_stats(
        directory, csv_input, all_df, out_df)

    m, c = plot_scatter(directory, out_df, norm_df, stat_df_all, stats_df_out, all_df.copy(),
                        name_stats, name_graph)

    return m, c


# *************************************************************************
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for extracting VH/VL relevant residues')
    parser.add_argument(
        '--directory', help='Directory where files will', required=True)
    parser.add_argument(
        '--csv_input', help='File that was the input to the method', required=True)
    parser.add_argument(
        '--name_stats', help='Name for output with statistics for run', required=True)
    parser.add_argument(
        '--name_graph', help='Name for graph outputted', required=True)
    args = parser.parse_args()

    create_stats_and_graph(args.directory, args.csv_input,
                           args.name_stats, args.name_graph)
