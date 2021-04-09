#!/usr/bin/python3
"""
Program:    graphVHVLangles
File:       graphVHVLangles.py

Version:    V1.0
Date:       07.04.2021
Function:

Description:
============


--------------------------------------------------------------------------
"""
# *************************************************************************
# Import libraries

# sys to take args from commandline
import sys
import pandas as pd
import collections
from collections import Counter
import matplotlib.pylab as plt

# *************************************************************************
def read_file():

    columns = ['pdb', 'angle']
# Take the commandline input as the file to search for packing angle data
    if sys.argv[1] != '':
        angle_file = pd.read_csv(sys.argv[1], usecols=columns)
    return angle_file


# *************************************************************************
def cluster_angles_by_value(table):
    cnt = Counter()
    for angle_val in table['angle']:
        cnt[angle_val] += 1
        lists = sorted(cnt.items())
    return lists

# *************************************************************************
def plot_angles_v_freq(data):

    x_labels = [val[0] for val in data]
    y_labels = [val[1] for val in data]
    plt.figure(figsize=(12, 6))
    ax = pd.Series(y_labels).plot(kind='bar')
    ax.set_xticklabels(x_labels)

    rects = ax.patches

    for rect, label in zip(rects, y_labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label, ha='center', va='bottom')

    plt.show()
    return
# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************

datatable = read_file()

clustered_data = cluster_angles_by_value(datatable)

graphing = plot_angles_v_freq(clustered_data)