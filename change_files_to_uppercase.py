#!/usr/bin/env python3
import os
import sys
import subprocess

cwd = os.getcwd()
for file in os.listdir(sys.argv[1]):
    if file.endswith('.PDB') or file.endswith('.pdb'):
        path1 = os.path.join(cwd, sys.argv[1], file)
        path2 = os.path.join(cwd, sys.argv[1], (file[:-4].upper() + '.pdb'))
        subprocess.run(['mv', path1, path2])