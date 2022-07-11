#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing

if __name__ == '__main__':
    df = pd.read_csv('Everything/VHVL_res_expanded_unencoded.csv')
    data = df.isna().sum()
    print(data)
    
