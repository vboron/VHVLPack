#!/usr/bin/env python3

from graphing import *
import pandas as pd
import argparse
import os

def readandplot(file):
    df_ = pd.read_csv(file)
    plt.figure()
    axes = plt.gca()
    axes.set_xlim([0, 4])
    axes.set_ylim([0, 120])
    plt.xlabel('RMSD')
    plt.ylabel('Frequency')
    def plotgraphs(df, label, column, color, y):
        df = df.round({column: 1})
        df_count=df[column].value_counts().sort_index()
        plt.plot(df_count, label=label, color=color)
        sd = df[column].std()
        mean = df[column].mean()
        plt.text(x = 3, y = y, s = f'mean: {mean}, StDev: {sd}', color = color)
  
    plotgraphs(df_, 'abYmod', 'RMSD abYmod', 'aquamarine', 100)
    plotgraphs(df_, 'repacked', 'RMSD Repacked abYmod', 'mediumpurple', 95)
    plt.tight_layout()
    plt.legend()
    plt.savefig(f'repack.jpg', format='jpg')
    plt.close()

parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--csv', required=True)
args = parser.parse_args()

readandplot(args.csv)
