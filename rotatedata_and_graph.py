#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing

def run_correction(directory):
    datafile = None
    m, c = None, None
    summary_stats = []
    file = 'NR2_GBReg_correction'
    for i in range(1, 6):
        file_name = f'{file}_{i}'
        csv_name = f'{file_name}.csv'
        path_name = os.path.join(directory, csv_name)
        cmds = ['./datarot.py', '-o', path_name]
        if m != None and c != None and datafile != None:
            cmds = cmds + ['-m', str(m), '-c', str(c), '--dataFile', datafile]
        utils.run_cmd(cmds, False)
        df = pd.read_csv(path_name)
        df['abs_err'] = df['error'].abs()
        df['sqerror'] = df['error'].pow(2)
        df['sq_angle'] = df['angle'].pow(2)
        sum_sqe = df['sqerror'].sum()
        print(df)
        n = df['angle'].count()
        meanabserror = (df['abs_err'].sum())/n
        rmsd = math.sqrt(sum_sqe/n)
        relrmse = utils.relrmse_from_df(df, rmsd)
        # print(df, sum_sqe, n, meanabserror, rmsd, relrmse)

        graphing.error_distribution(directory, csv_name, f'error_dist_correction_{i}')
        m, c = graphing.actual_vs_predicted_from_df(df, directory, file_name, file_name)
        datafile = path_name
        print(datafile)
        stats = [meanabserror, rmsd, relrmse, m, c]
        summary_stats.append(stats)

    stats_df = pd.DataFrame(data=[summary_stats], columns=['meanabserror', 'rmsd', 'relrmse', 'm', 'c'])
    stats_df.to_csv(os.path.join(directory, f'{file}_stats_summary.csv'), index=False)
    print(stats_df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for applying a rotational correction factor recursively')
    
    parser.add_argument('--directory', help='Directory', required=True)
    args = parser.parse_args()
    run_correction(args.directory)