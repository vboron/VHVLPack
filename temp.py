#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import numpy as np 
import utils
import math
import matplotlib.pyplot as plt
import graphing
import stats2graph

def run_correction():
    datafile = None
    m, c = None, None
    for i in range(1, 6):
        file_name = f'NR2_GBReg_correction_{i}'
        csv_name = f'{file_name}.csv'
        path_name = os.path.join(args.directory, csv_name)
        cmds = ['./datarot.py', '-o', path_name]
        if m != None and c != None and datafile != None:
            cmds.extend(['-m', m, '-c', c, '--dataFile', datafile])
        utils.run_cmd(cmds, False)
        df = pd.read_csv(path_name)
        df['abs_err'] = df['error'].abs()
        df['sqerror'] = df['error'].pow(2)
        df['sq_angle'] = df['angle'].pow(2)
        sum_sqe = df['sqerror'].sum()
        n = df['angle'].count()
        meanabserror = (df['abs_err'].sum())/n
        rmsd = math.sqrt(sum_sqe/n)
        relrmse = utils.calc_relemse(path_name, rmsd)
        print(df, sum_sqe, n, meanabserror, rmsd, relrmse)

        graphing.error_distribution(path_name, f'error_dist_correction_{i}.jpg')
        m, c = stats2graph.create_stats_and_graph(args.directory, csv_name, file_name, file_name)
        datafile = path_name
        data = [meanabserror, rmsd, relrmse, m, c]
        df2 = pd.DataFrame(data=data, columns=['meanabserror', 'rmsd', 'relrmse', 'm', 'c'])
        print(df2)
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for applying a rotational correction factor recursively')
    
    parser.add_argument('--directory', help='Directory', required=True)
    args = parser.parse_args()
    run_correction()