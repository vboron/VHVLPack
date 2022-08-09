#!/usr/bin/env python3
import os
import sys

cwd = os.getcwd()
for file in os.listdir(sys.argv[1]):
    # if file.endswith('.mar') or file.endswith('.cho'):
    #     src = os.path.join(cwd, sys.argv[1], file)
    #     dst = os.path.join(cwd, sys.argv[1], (file[2:-4].upper() + '.pdb'))
    if file.endswith('.pdb'):
        src = os.path.join(cwd, sys.argv[1], file)
        dst = os.path.join(cwd, sys.argv[1], (file[1:7] + '.pdb'))
        os.rename(src, dst)