#!/usr/bin/env python3

import os
import sys
import pandas as pd
import numpy as np
import itertools
import shutil
from utils import one_letter_code


# ************************************************************************* 
def extract_seqs():
    
    pdb_seq={}
    for file in os.listdir(direct):
        fname=file[:-4]
        file=os.path.join(cwd, direct, file)
        
        if not str(file).endswith('.pdb'):
            continue

        with open(file, 'r') as f:
            seq=[]
            file_lines=f.readlines()

            for line in file_lines:
                line=line.split()
                
                if line[0]=='ATOM' and line[2]=='CA':
                    seq.append(one_letter_code(fname, line[3]))
            seq=''.join(seq)
            
            if seq not in pdb_seq:
                pdb_seq[seq]=fname

    return pdb_seq

# ************************************************************************* 
def move_into_dir(dictionary):

    new_dir=sys.argv[2]
    try:
        os.mkdir(new_dir)
    except OSError:
        print("Creation of the directory %s failed" % new_dir)
    else:
        print("Successfully created the directory %s " % new_dir)
    
    for seq, pdb in dictionary.items():
        old_path=os.path.join(cwd, direct, '{}.pdb'.format(pdb))
        new_path=os.path.join(cwd, new_dir, pdb)
        # Make a copy of the file and put it into the second directory
        shutil.copy(old_path, new_path)
    return
# *************************************************************************
# *** Main program                                                      ***
# *************************************************************************
direct=sys.argv[1]
cwd=os.getcwd()
sequences=extract_seqs()
result=move_into_dir(sequences)