#!/usr/bin/python3

import itertools
import os
import pandas as pd
from pipeline_enums import *

def rank_methods():
    data = []
    data_o = []

    # def extract_data(ds: Dataset, nr: NonRedundantization, meth: MLMethod, cr: Correction):
    #     name = unique_name(ds, nr, meth, cr)
    def extract_data(ds: Dataset, nr: NonRedundantization, meth: MLMethod):
        name = f'{ds.name}_{nr.name}_{meth.name}'
        name_latex_friendly = name.replace('_', '-')

        path = os.path.join(ds.name, f'{name}_stats_all.csv')
        df = pd.read_csv(path)
        df.insert(0, 'name', name_latex_friendly)
        data.append(df)

        path_o = os.path.join(ds.name, f'{name}_stats_out.csv')
        df_o = pd.read_csv(path_o)
        df_o.insert(0, 'name', name_latex_friendly)
        data_o.append(df_o)

    # for ds, nr, cr in itertools.product(Dataset, NonRedundantization, Correction):
    #     if nr == NonRedundantization.NR0:
    #         print(f'Skipping {ds.name}/{MLMethod.XvalWeka.name}/{nr.name}/{cr.name}...')
    #         continue
    #     extract_data(ds, nr, MLMethod.XvalWeka, cr)

    # for tt, nr, meth, cr in itertools.product(get_all_testtrain(), NonRedundantization, MLMethod, Correction):
    for tt, nr, meth, in itertools.product(get_all_testtrain(), NonRedundantization, MLMethod):
        # if nr != NonRedundantization.NR0 and tt.testing.name != 'Everything':
        #     extract_data(tt.testing, nr, meth, cr)
        extract_data(tt.testing, nr, meth)

    # Create a combined parameter which will allow sorting by 'all' parameters
    def process_combined_para(df, top10_csv_name):
        # Column name
        combined_para = 'combined-para'

        df[combined_para] = (1/df['pearson'].abs()) + df['error'].abs() + df['RMSE'].abs() + \
            df['RELRMSE'].abs()
        df = df.sort_values(by=[combined_para], key=abs)
        top10 = df.head(20)
        top10.to_csv(top10_csv_name, index=False)

    df = pd.concat(data)
    process_combined_para(df, 'top10.csv')

    df_o = pd.concat(data_o)
    process_combined_para(df_o, 'top10_out.csv')

if __name__ == '__main__':
    rank_methods()