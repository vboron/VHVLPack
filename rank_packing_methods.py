#!/usr/bin/python3

import itertools
import os
import pandas as pd
from pipeline_enums import *

def rank_methods():
    data = []
    data_o = []
    for ds, nr, meth, cr in itertools.product(Dataset, NonRedundantization, MLMethod, Correction):
        if meth == MLMethod.XvalWeka and nr == NonRedundantization.NR0:
            print(f'Skipping {meth.name}/{nr.name}...')
        else:
            try:
                name = unique_name(ds, nr, meth, cr)
                path = os.path.join(ds.name, f'{name}_stats_all.csv')
                col = [i.strip('\n')
                    for i in open('read_stats_csv.dat').readlines()]
                df = pd.read_csv(path, usecols=col)
                df.insert(0, 'name', name)
                data.append(df)
                path_o = os.path.join(ds.name, f'{name}_stats_out.csv')
                df_o = pd.read_csv(path_o, usecols=col)
                df_o.insert(0, 'name', name)
                data_o.append(df_o)
            except:
                print(
                    f'Dataset: {ds.name}, Method: {meth.name}, Correction: {cr.name} has no file')
    df = pd.concat(data)

    # Create a combined parameter which will allow sorting by 'all' parameters
    df['comb_para'] = (1/df['pearson']) + df['error'].abs() + df['RMSE'].abs() + \
        df['RELRMSE'].abs() + df['slope'].abs() + df['intercept'].abs()
    df = df.sort_values(by=['comb_para'], key=abs)
    top10 = df.head(10)

    df_o = pd.concat(data_o)
    df_o['comb_para'] = (1/df_o['pearson']) + df_o['error'].abs() + df_o['RMSE'].abs() + \
        df_o['RELRMSE'].abs() + df_o['slope'].abs() + df_o['intercept'].abs()
    df_o = df_o.sort_values(by=['comb_para'], key=abs)
    top10_o = df_o.head(10)

    top10.to_csv('top10.csv', index=False)
    top10_o.to_csv('top10_out.csv', index=False)

if __name__ == '__main__':
    rank_methods()