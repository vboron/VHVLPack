#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing

if __name__ == '__main__':
    df = pd.read_csv('Everything/Everything_NR2_GBReg.csv')
    directory = 'Everything'
    file_name = 'Everything_NR2_GBReg'
    graphing.actual_vs_predicted_from_df(df, directory, file_name, file_name)