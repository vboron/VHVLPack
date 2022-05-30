#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import numpy as np
import datarot 

import utils
import math
import matplotlib.pyplot as plt

def run_correction():
    for i in range(0, 1):
        datarot('--name', f'NR2_GBReg_correction_{i}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for applying a rotational correction factor recursively')
    
    parser.add_argument('--directory', help='Directory', required=True)
    args = parser.parse_args()