# VHVL Packing Pipeline

## This file details the protocol for creating our machine learning model for calculating the packing angle between variable heavy and light chains in antibodies.

1. Dataset of complete (Light chain + heavy chain) antibodies with Chothia labelling was obtained from 
    [Dataset](http://www.abybank.org/abdb/)

2.  The first step in pre-processing the data is filtering all the structures to include those obtained by x-ray 
    crystallography within a desired resolution (we decided that 5Å was sufficient). 
    The program takes 2 commandline inputs: directory of pdb files with full path, maximum desired resolution in Å. 
    The output is a directory that only contains .pdb files obtained by x-ray crys and higher than 5Å resolution.

`filter_by_resolution.py /path/to/directory/ 5` 

3. The files in this directory are then run through a program which calculates the VH-VL packing angle 
    ([abpackingangle](https://github.com/ACRMGroup/abpackingangle)). The PDB code and calculated angle are then outputted 
    as a .csv file by the .py program. 
    Inputs: directory of PDBs, name of .csv file to be produced. 

`compile_angles.py xray_5A_pdbs VHVL_ang`

4. Once we have the actual packing angles calculated, we will extract information that will be used to train our 
neural network. A genetic anlorythm was used (as described: Abhinandan, K R, and Andrew C R Martin. 
“Analysis and prediction of VH/VL packing in antibodies.” Protein engineering, design & selection : PEDS vol. 23,9 
(2010): 689-97. doi:10.1093/protein/gzq043) to determine which residue positions in the VH-VL interface are most 
significant in packing angle determination. This program extracts the identities at these positions and puts them into
a .csv along with their PDB code. 
Inputs: directory of .pdb files, name of .csv output.

`find_VHVLres.py xray_5A_pdbs VHVL_res`

5. We create the inputs for the machine learning by encoding amino acids. In our pipeline we decided to use T-Scale, 
(Tian, F.; Zhou, P.; Li, Z. T-scale as a novel vector of topological descriptors for amino acids and its application 
in QSARs of peptides. J. Mol. Struct. 2007, 830, 106−115.) as it worked better than our previously used 4 dimensional
vectors. 
Inputs: the .csv files containing the amino acid identities, the calculated angles, a .dat file that
contains the column names that will be used to create the output, and a name for the output.

`encode_ts.py VHVL_res.csv VHVL_ang.csv ts.dat ts_enc`

6. We will process the .csv file of these encoded residues. The program will average angles if the PDB code and the 
amnio acid identities are identical, to remove repeats that come from the same PDB. 
Inputs: encoded .csv file, .dat file containing column names, output name.

`filter_dup.py ts_enc.csv ts.dat ts`

7. Convert the .csv file into an .arff file that Weka (machine learning framework) uses. 
([csv2arff](https://github.com/AndrewCRMartin/bioscripts/blob/master/csv2arff.pl))
Input: column names (excluding output, i.e. angle), specify output (i.e. angle), specify .csv file.

`csv2arff -ni in_ts.dat angle no_dup_ts.csv > ts.arff`

8. Split the .csv file with no duplicates individual files, where each line (PDB) becomes a separate file. 
(This is to prepare files for testing.)

`lines2files.py no_dup_ts.csv ts.dat /where/these/files/will/go`

9. All the newly made individual files will now be converted into arff files.

`direct_csv2arff.py directory_where_files_are in_ts.dat`

**OR**

7, 8, 9 & 10. All these steps can be done in a shell script, and then calls Weka, which is installed in-path. The
number of hidden layers can be adjusted in this script and multiple models can be produced.

```
export WEKA=/usr/local/apps/weka-3-8-3
export CLASSPATH=$WEKA/weka.jar

# Training option selection
BASEPATH=$(pwd)
DATA=${BASEPATH}/where/files/are
CSVFILES=${DATA}/*.csv
ARFFFILES=${DATA}/*.arff
INPUTS=${BASEPATH}/in_ts.dat
CLASSIFIER=weka.classifiers.functions.MultilayerPerceptron

# max number of hidden layers that we want to test (here 30)
LAYERS=30

# split lines into separate .csv files
lines2files.py no_dup_ts.csv ts.dat /where/these/files/will/go

echo '*** Converting training set to arff ***'
csv2arff for train file
csv2arff -v -ni $INPUTS angle ${BASEPATH}/no_dup_ts.csv > ts.arff

for file in ${CSVFILES}; do
        echo '*** Converting test file' $file 'to .arff ***'
        name=$(echo "$file" | cut -f 1 -d '.')
        csv2arff -v -ni $INPUTS angle $file > $name.arff
done

# i starts at the min number of hidden layers we want to test (here 20) and ends at the max specified before
for ((i=20;i<=LAYERS;i++)); do
    echo "*** Training with -H $i ***"
    # train
    java $CLASSIFIER -v -H $i -t ts.arff -d VHVL_$i.model > ${DATA}/$i_tra
in.log

    for file in ${ARFFFILES}; do
        echo '*** Testing' $file 'with' $i 'Hidden layers ***'
        name=$(echo "$file" | cut -f 1 -d '.')
        java $CLASSIFIER -v -T $file -p 0 -l VHVL_$i.model > ${name}_${i}_test.log
    done
done
```

11. The previous set will create log files that contain the predicated, actual and error values for each. 

=== Predictions on test data ===

| inst    | actual | predicted | error |
| :---: | :---: | :---: | :---: |
| 1 | -41.876 | -43.235|  -1.35 | 

This data is then plotted to show predicted vs. actual values, with the outliers having different coloring and 
RELRMSEs/lines of best fit being included for both the full dataset and the outliers. 
(We automate plotting data for all hidden layers we tested by using a shell script).

```
set -x

for ((i=30;i<=40;i++)); do
        ./log_stats2graph.py /home/veronica/VHVLPack/alphafold/af2data $i
done
```


         
