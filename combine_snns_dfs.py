#!/usr/bin/env python3

# 1) snns pdb codes .csv
# 2) snns calculated angles .csv
# 3) actual angles .csv
# 4) name for output .csv
import sys
import pandas as pd
import numpy as np
import math
import subprocess

col1 = ['code']
col2 = ['pred']
col3 = ['code', 'angle']
code_f = pd.read_csv(sys.argv[1], usecols=col1) 
code_f['code'] = code_f['code'].apply(lambda x: x[:-4])
pred_f = pd.read_csv(sys.argv[2], usecols=col2)

code_f['pred'] = pred_f['pred']


actual_ang_f = pd.read_csv(sys.argv[3], usecols=col3)

full_df = pd.merge(code_f, actual_ang_f, how='right', on=['code'], sort=True)

full_df['error'] = full_df['pred']-full_df['angle']
full_df['sqerror'] = np.square(full_df['error'])

full_df.to_csv('{}.csv'.format(sys.argv[4]), index=False)
