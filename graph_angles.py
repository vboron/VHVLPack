#!/usr/bin/python3
"""
Program:    graph_angles
File:       graph_angles.py

Version:    V1.0
Date:       04.05.2021
Function:   Graph distribution of VHVL packing angles

Description:
============
This program takes a .csv file of encoded residues and their angles and then plots a histogram of the angle frequency.

------------------------------------------------
"""

# *************************************************************************
# Import libraries

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import math


# *************************************************************************
def read():
    """Read .csv file as a dataframe

    Return: res_file    --- dataframe containing encoded residues and angles

    04.05.2021  Original   By: VAB
    """

    # The column names contained in the .csv file
    col1 = ['code', 'angle']

    # Take the commandline input as the directory, otherwise look in current directory
    if sys.argv[1] != '':
        res_file = pd.read_csv(sys.argv[1], usecols=col1)

    # Removes all rows that are missing angles
    res_file = res_file[res_file['angle'].str.contains('Packing angle') == False]

    return res_file


# *************************************************************************
def plot(data):
    """Plot a histogram of the VH-VL packing angle distribution

    Input: data    --- dataframe containing encoded residues and angles

    04.05.2021  Original   By: VAB
    """

    plt.figure()
    data['angle'] = (data['angle']).astype(float)

    # Specify the mean width of bins and make them equidistant
    w = 1
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

    # Open a pop-up window with plot
    plt.show()
    return


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

dataframe = read()

graph = plot(dataframe)