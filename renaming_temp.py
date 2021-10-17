#!/usr/bin/env python3

import os
import sys

def filenames_to_upper():
	for file in os.listdir(sys.argv[1]):
		if str(file).endswith('.pdb'):
			ext = file[-4:]
			name = file[3:-4]
			file2 = name.upper() + ext
			os.rename(sys.argv[1] + '/' + file, sys.argv[1] + '/' + file2)
			print(name)
result = filenames_to_upper()
