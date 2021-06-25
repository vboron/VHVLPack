#!/usr/bin/env python3
"""
Program:    log_stats2graph
File:       log_stats2graph.py

Version:    V1.0
Date:       06.14.2021
Function:   Scatter graph of predicted vs. actual packing angles

Description:
============
Program extracts lines of statistics from .log files produced using MLP through Weka framework and converts them into
dataframe that is then plotted.

Commandline input: 1) Directory where the .log files are
                   2) Number of Hidden layers
                   3)

------------------------------------------------
"""
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

    direct = sys.argv[1]
    col = ['code', 'angle', 'predicted', 'error']

    all_data = []
    files = []

    for file in os.listdir(direct):
        if file.endswith("_{}_test.log".format(sys.argv[2])):
            files.append('{}/{}'.format(direct, file))

    for log_file in files:
        with open(log_file) as text_file:
            for line in text_file:
                if str(line).strip().startswith('1'):
                    line = re.sub(' +', ' ', line)
                    line = line.strip()
                    line_list = line.split(' ')
                    name = log_file.split('/')
                    name2 = name[1]
                    code = name2[:-4]
                    pred = float(line_list[2])
                    angle = float(line_list[1])
                    error = float(line_list[3])
                    this_data = [code, angle, pred, error]
                    all_data.append(this_data)


    df = pd.DataFrame(data=all_data, columns=col)
    df.to_csv('all_{}.csv'.format(sys.argv[2]), index=False)
    df['sqerror'] = np.square(df['error'])
    sum_sqerror = float(df['sqerror'].sum())
    average_error = sum_sqerror/int(df['code'].size)
    RMSE = str(math.sqrt(average_error))
    print(RMSE)

    RELRMSE = subprocess.check_output(['python3', 'RELRMSE.py', 'all_{}.csv'.format(sys.argv[2]), 'graph.dat', RMSE])

    return df, RELRMSE


# *************************************************************************
def plot_scatter(file, RELRMSE):
    file['angle'] = file['angle'].apply(lambda x: float(x))
    file['predicted'] = file['predicted'].apply(lambda y: float(y))
    x = file['angle']
    y = file['predicted']
    plt.scatter(x, y, s=2, color='rosybrown')
    plt.xlabel('Calculated Angle')
    plt.ylabel('Predicted Angle')
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, color='k', linestyle='dashed', linewidth=1)
    plt.plot(x, x + 0, '-b')
    plt.text(s='best fit: y={:.3f}x+{:.3f}'.format(m, b), x=-60, y=-33, fontsize=8)
    plt.text(s='blue line: y=x', x=-60, y=-31, fontsize=8)
    plt.text(s='RELRMSE: {:.3}'.format(float(RELRMSE)), x=-60, y=-35, fontsize=8)
    plt.suptitle('ML prediction of VHVL packing angle (HL = {})'.format(sys.argv[2]), fontsize=14)
    plt.tight_layout()
    plt.show()
    return


# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
frame, data = stats_to_df()

plot = plot_scatter(frame, data)
