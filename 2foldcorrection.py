#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import utils
import math
import graphing
import stats2graph


def find_norms_and_outliers(csv_file):
    df = pd.read_csv(csv_file)

    min_norm = -48
    max_norm = -42

    # extract data where the predicted angle is within the normal range into a new dataframe
    df_normal = df[df['angle'].between(min_norm, max_norm)]

    # extract data where predicted angles are outside of the normal range and add into a new dataframe
    outliers_max = df[df['angle'] >= max_norm]
    outliers_min = df[df['angle'] <= min_norm]

    df_outliers = pd.concat([outliers_max, outliers_min])

    return df_normal, df_outliers

def run_norm_correction(df_normal):
    
