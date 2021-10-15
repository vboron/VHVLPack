#!/usr/bin/env python3

import sys
import os
import shutil

def move_old_files_out():
    old_file_dir = os.listdir(sys.argv[1])

    print(old_file_dir)
