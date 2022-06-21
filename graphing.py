# *************************************************************************
# Import libraries 

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import utils


# *************************************************************************
def angle_distribution(directory, csv_ang, graph_name):
    """Plot a histogram of the VH-VL packing angle distribution

    Input: directory    --- directory where the data can be found and where the graph will be saved
           csv_ang      --- .csv files containing the actual angle of the pdbs which will be analized
           graph_name   --- the name that the graph file will be saved under

    By: VAB
    """

    plt.figure()
    ang_file = os.path.join(directory, csv_ang)
    data = pd.read_csv(ang_file)

    data['angle'] = (data['angle']).astype(float)

    # Specify the mean width of bins and make them equidistant
    w = 0.5
    n = math.ceil((data['angle'].max() - data['angle'].min()) / w)
    plt.hist(data['angle'], bins=n, edgecolor='k', color='rosybrown')

    # Add axis labels to graph
    plt.xlabel('VH-VL Packing Angle')
    plt.ylabel('Frequency')

    # Add a black, dashed line at the mean
    plt.axvline(data['angle'].mean(), color='k', linestyle='dashed', linewidth=1)

    # Add 'Mean: ' label to graph, the first number specifies the x-position of the label and the second the y-position
    _, max_ylim = plt.ylim()
    plt.text(data['angle'].mean() * 0.9, max_ylim * 0.9, 'Mean: {:.2f}'.format(data['angle'].mean()))

    # plt.suptitle(f'{graph_title}', fontsize=14)

    path_fig = os.path.join(directory, f'{graph_name}.jpg')
    plt.savefig(path_fig, format='jpg')
    plt.close()


# *************************************************************************
def error_distribution(directory, csv_input, graph_name):
    """Plot the error distribution for the dataset predictions

    Input: directory    --- directory where the data can be found and where the graph will be saved
           csv_input    --- the datafile with the predictions for the method
           csv_columns  --- column file that will be used to read the .csv file
           graph_name   --- the name that the graph file will be saved under

    By: VAB
    """
    plt.figure()

    df = pd.read_csv(os.path.join(directory, csv_input)).copy()

    df = df.round({'error': 1})

    df_count=df['error'].value_counts().sort_index()
    plt.plot(df_count)

    plt.xlabel('Errors in prediction')
    plt.ylabel('Frequency')

    plt.tight_layout()

    path_fig = os.path.join(directory, f'{graph_name}.jpg')
    plt.savefig(path_fig, format='jpg')
    plt.close()

# *************************************************************************
def sq_error_vs_actual_angle(directory, csv_input, graph_name):
       """Plot squared error in predicted packing angle against actual packing angle.

       Input: directory    --- directory where the data can be found and where the graph will be saved
              csv_input    --- the datafile with the predictions for the method
              csv_columns  --- column file that will be used to read the .csv file
              graph_name   --- the name that the graph file will be saved under

       By: VAB
       """
       plt.figure()

       df = pd.read_csv(os.path.join(directory, csv_input)).copy()
       df['sqerror'] = np.square(df['error'])

       x = df['angle']
       y = df['sqerror']
       plt.scatter(x, y, s=2, color='mediumturquoise')

       plt.tight_layout()

       path_fig = os.path.join(directory, f'{graph_name}.jpg')
       plt.savefig(path_fig, format='jpg')
       plt.close()

# *************************************************************************

def actual_vs_predicted_from_df(df, directory, stats_csv_name, pa_graph_name):

       # Calculate the Root Mean Square Error
       df['sqerror'] = np.square(df['error'])
       sum_sqerror = df['sqerror'].sum()
       average_error = sum_sqerror / int(df['angle'].size)
       rmse = math.sqrt(average_error)

       relrmse = utils.relrmse_from_df(df, rmse)

       # .corr() returns the correlation between two columns
       pearson_a = df['angle'].corr(df['predicted'])

       mean_abs_err = df['error'].abs().mean()
       stat_data = [pearson_a, mean_abs_err, rmse, relrmse]
       stat_col = ['pearson', 'error', 'RMSE', 'RELRMSE']
       stats = pd.DataFrame(data=[stat_data], columns=stat_col)

       plt.figure()

       color_values = 'mediumpurple'
       color_bf_line = 'rebeccapurple'

       x = df['angle']
       y = df['predicted']

       m, b = np.polyfit(x, y, 1)
       plt.plot(x, m * x + b, color=color_bf_line, linestyle='dashed', linewidth=1)

       plt.scatter(x, y, s=2, color=color_values)

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

       plt.text(s='Best fit: y={:.3f}x+{:.3f}'.format(m, b),
              x=-61, y=-33, fontsize=8, color=color_bf_line)
       plt.text(s='RELRMSE: {:.3}'.format(
              float(stats['RELRMSE'])), x=-61, y=-34, fontsize=8)

       plt.tight_layout()

       # add best fit data to dataframe and export the dataframe
       # add best fit lines to statistics dataframe
       bf_line = 'y={:.3f}x+{:.3f}'.format(m, b)

       stats['fit'] = bf_line
       stats['slope'] = m
       stats['intercept'] = b

       path_stats = os.path.join(directory, f'{stats_csv_name}.csv')
       stats.to_csv(path_stats, index=False)

       # Exports the figure as a .jpg file
       path_fig = os.path.join(directory, f'{pa_graph_name}.jpg')
       plt.savefig(path_fig, format='jpg')
       plt.close()

       return m, b
