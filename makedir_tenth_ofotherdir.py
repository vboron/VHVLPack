#!/usr/bin/env python3

import argparse
import os
import shutil

def compare_dirs(dir1, dir2):
    dir1_files = os.listdir(dir1)

    new_files = []
    i=0
    while i <= len(dir1_files)//10:
        new_files.append(dir1_files[i])
        i+=1
    os.mkdir(dir2)
    print(len(new_files))

    for file in new_files:
        print(file)
        src = os.path.join(dir1, file)
        dst = os.path.join(dir2, file)
        shutil.copy2(src, dst)


parser = argparse.ArgumentParser(description='Program for compiling angles')
parser.add_argument('--dir1', required=True, help='Directory which is used as base')
parser.add_argument('--dir2', required=True, help='Directory from which files will be copied into new directory')

args = parser.parse_args()

compare_dirs(args.dir1, args.dir2)