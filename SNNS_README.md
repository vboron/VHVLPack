# Protocol for using the papa/newpapa snns programs

## Files need to be in the .seq format 
e.g.
L1 GLU
L2 ILE
L3 VAL
L4 LEU
L5 THR
L6 GLN

Convert .pdb file to .seq file using:
`./pdb2seq.py name/of/directory/with/pdb/files`

## newpapa or papa trained snns are deployed on the .seq files
`newpapa_on_directory.sh`:

```
set -x
BASE=$(pwd)
DIRECTORY=${BASE}/af2seq
FILES=${DIRECTORY}'/*.seq'

echo 'code' >> af2_newpapa_pdbcodes.csv
echo 'pred' >> af2_newpapa_predictions.csv
for seqfile in ${FILES}; do
    name=$(basename ${seqfile})
    name="${name%*}"
    echo ${name} >> af2_newpapa_pdbcodes.csv
    ~/newpapa/papa -q $seqfile >> af2_newpapa_predictions.csv

```

## Analysis is performed

`./stats2graph.py SNNS/newpapa_af2.csv newpapa_af2 graph_snns.dat newpapa`
