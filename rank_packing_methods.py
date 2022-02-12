#!/usr/bin/python3

import itertools
import os
import pandas as pd
from pipeline_enums import Dataset, NonRedundantization, MLMethod, unique_name

data = []
data_o = []
for ds, nr, meth in itertools.product(Dataset, NonRedundantization, MLMethod):
    name = unique_name(ds, nr, meth)
    path = os.path.join(ds.name, f'{name}_stats_all.csv')
    col = [i.strip('\n') for i in open('read_stats_csv.dat').readlines()]
    df = pd.read_csv(path, usecols=col)
    df.insert(0, 'name', name)
    data.append(df)
    path_o = os.path.join(ds.name, f'{name}_stats_out.csv')
    df_o = pd.read_csv(path_o, usecols=col)
    df_o.insert(0, 'name', name)
    data_o.append(df_o)

df = pd.concat(data)
df = df.sort_values(by=['RELRMSE'], key=abs)
top_10 = df.tail(10)
df_o = pd.concat(data_o)
df_o = df_o.sort_values(by=['RELRMSE'], key=abs)
top_10_o = df_o.tail(10)
df.to_csv('top10_relrmse.csv', index=False)
df_o.to_csv('top10_relrmse_out.csv', index=False)
print(top_10, top_10_o)
