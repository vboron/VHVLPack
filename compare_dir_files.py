#!/usr/bin/env python3

import argparse
import os
import shutil

def compare_dirs(dir1, dir2):
    dir1_files = os.listdir(dir1)
    dir2_files = os.listdir(dir2)
    new_files = []
    for file in dir2_files:
        if file not in dir1_files:
            new_files.append(file)
    new_dir = 'new_files'
    for file in new_files:
        src = os.path.join(dir2, file)
        dst = os.path.join(new_dir, file)
        shutil.copy2(src, dst)


parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--dir1', required=True)
parser.add_argument('--dir2', required=True)

args = parser.parse_args()

compare_dirs(args.dir1, args.dir2)