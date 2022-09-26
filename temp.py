#!/usr/bin/env python3
from itertools import product
file = open('expanded_residues.dat', 'r')
res = file.readlines()
letters = ['a', 'b', 'c', 'd']
c = []
for r in res:
    for l in letters:
        c.append(f'{r.strip()}{l}')
with open('in_expanded_res.dat', 'w') as f:
        for l in c:
            f.write(f'{l}\n')
