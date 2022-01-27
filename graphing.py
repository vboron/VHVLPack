# *************************************************************************
# Import libraries

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

# *************************************************************************
def angle_distribution(directory, csv_ang, graph_name):
    """Plot a histogram of the VH-VL packing angle distribution

    Input: directory    --- directory where the data can be found and where the graph will be saved
           csv_ang      --- .csv files containing the actual angle of the pdbs which will be analized
           graph_name   --- the name that the graph file will be saved under

    By: VAB
    """

    col1 = ['code', 'angle']
    ang_file = os.path.join(directory, csv_ang)
    data = pd.read_csv(ang_file, usecols=col1)

    plt.figure()
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
    min_ylim, max_ylim = plt.ylim()
    plt.text(data['angle'].mean() * 0.9, max_ylim * 0.9, 'Mean: {:.2f}'.format(data['angle'].mean()))

    # plt.suptitle(f'{graph_title}', fontsize=14)

    path_fig = os.path.join(directory, f'{graph_name}.png')
    plt.savefig(path_fig, format='png')
    plt.show()

# *************************************************************************
def error_distribution(directory, csv_input, csv_columns, graph_name):
    """Plot the error distribution for the dataset predictions

    Input: directory    --- directory where the data can be found and where the graph will be saved
           csv_input    --- the datafile with the predictions for the method
           csv_columns  --- column file that will be used to read the .csv file
           graph_name   --- the name that the graph file will be saved under

    By: VAB
    """
    cols = [i.strip('\n') for i in open(csv_columns).readlines()]

    df = pd.read_csv(os.path.join(directory, csv_input), usecols=cols).copy()

    df = df.round({'error': 1})

    df_count=df['error'].value_counts().sort_index()
    plt.plot(df_count)

    plt.xlabel('Errors in prediction')
    plt.ylabel('Frequency')

    plt.tight_layout()

    path_fig = os.path.join(directory, f'{graph_name}.png')
    plt.savefig(path_fig, format='png')

# *************************************************************************
def sq_error_vs_actual_angle(directory, csv_input, csv_columns, graph_name):
    """Plot squared error in predicted packing angle against actual packing angle.

    Input: directory    --- directory where the data can be found and where the graph will be saved
           csv_input    --- the datafile with the predictions for the method
           csv_columns  --- column file that will be used to read the .csv file
           graph_name   --- the name that the graph file will be saved under

    By: VAB
    """
    cols = [i.strip('\n') for i in open(csv_columns).readlines()]

    df = pd.read_csv(os.path.join(directory, csv_input), usecols=cols).copy()
    df['sqerror'] = np.square(df['error'])

    x = df['angle']
    y = df['sqerror']
    plt.scatter(x, y, s=2, color='mediumturquoise')

    plt.xlabel('Actual packing angle')
    plt.ylabel('Square of error')

    plt.tight_layout()

    path_fig = os.path.join(directory, f'{graph_name}.png')
    plt.savefig(path_fig, format='png')