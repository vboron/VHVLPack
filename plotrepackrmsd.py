#!/usr/bin/env python3

from graphing import *
import pandas as pd
import argparse
import os

def readandplot(file):
    df_ = pd.read_csv(file)
    plotgraphs(df_, 'abYmod', 'RMSD abYmod')
    plotgraphs(df_, 'repacked', 'RMSD Repacked abYmod')

    def plotgraphs(df, dataset, column):
        plt.figure()

        df = df.round({column: 1})

        df_count=df[column].value_counts().sort_index()
        plt.plot(df_count)
        axes = plt.gca()
        axes.set_xlim([0, 6])
        axes.set_ylim([0, 250])
        plt.xlabel('RMSD')
        plt.ylabel('Frequency')

        plt.tight_layout()
        plt.savefig(f'{dataset}.jpg', format='jpg')
        plt.close()

parser = argparse.ArgumentParser(description='Program for extracting VH/VL relevant residues')
parser.add_argument('--csv', required=True)
args = parser.parse_args()

readandplot(args.csv)
