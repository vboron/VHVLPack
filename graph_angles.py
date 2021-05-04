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
    col1 = ['code', 'L38a', 'L38b', 'L38c', 'L38d', 'L38e', 'L40a', 'L40b', 'L40c', 'L40d', 'L40e', 'L41a', 'L41b',
            'L41c', 'L41d', 'L41e', 'L44a', 'L44b', 'L44c', 'L44d', 'L44e',
            'L46a', 'L46b', 'L46c', 'L46d', 'L46e', 'L87a', 'L87b', 'L87c', 'L87d', 'L87e',
            'H33a', 'H33b', 'H33c', 'H33d', 'H33e', 'H42a', 'H42b', 'H42c', 'H42d', 'H42e',
            'H45a', 'H45b', 'H45c', 'H45d', 'H45e', 'H60a', 'H60b', 'H60c', 'H60d', 'H60e',
            'H62a', 'H62b', 'H62c', 'H62d', 'H62e', 'H91a', 'H91b', 'H91c', 'H91d', 'H91e',
            'H105a', 'H105b', 'H105c', 'H105d', 'H105e', 'angle']

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