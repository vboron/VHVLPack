#!/usr/bin/python3
"""
Function:   Graph distribution of VHVL packing angles

Description:
============
This program takes a .csv file of encoded residues and their angles and then plots a histogram of the angle frequency.

------------------------------------------------
"""

# *************************************************************************
# Import libraries

import argparse
import os
import matplotlib.pyplot as plt
import pandas as pd
import math

# *************************************************************************
def plot(directory, csv_ang, graph_name):
    """Plot a histogram of the VH-VL packing angle distribution

    Input: data    --- dataframe containing encoded residues and angles

    04.05.2021  Original   By: VAB
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

    path_fig = os.path.join(directory, f'{graph_name}.tiff')
    plt.savefig(path_fig, format='tiff')
    plt.show()
    return


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
parser = argparse.ArgumentParser(description='Program plots the frequency of packing angles')
parser.add_argument('--directory', help='Directory of datset', required=True)
parser.add_argument('--ang_csv', help='File that contains the packing angle for each .pdb file', required=True)
parser.add_argument('--out_graph', help='Output name for graph', required=True)
# parser.add_argument('--title_graph', help='Title that will appear above graph', required=True)
args = parser.parse_args()

graph = plot(args.directory, args.ang_csv, args.out_graph, args.title_graph)
