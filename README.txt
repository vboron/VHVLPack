VHVL Packing Prediction Pipeline

Description:
This set of programs is designed to evaluate build a predictive model of packing angles between the variable light and variable heavy chains in antibodies.
The programs start with cleaning up data from a directory of antibody PDB files numbered using the Chothia numbering scheme (which can be found here: http://www.abybank.org/abdb/). The packing angles are then calculated and the relevant residues are located using known positions as reference (Abhinandan KR, Martin AC. Analysis and prediction of VH/VL packing in antibodies. Protein Eng Des Sel. 2010 Sep;23(9):689-97. doi: 10.1093/protein/gzq043. Epub 2010 Jun 30. PMID: 20591902.). One of several encoding schemes is then applied to the residues to prepare them for conversion into .arff file format. 10-fold cross validation is then used to process the data using machine learning.

#*****************************************************************
filter_by_resolution.py

Description:
The program will look at PDB files and take the ones that have a resolution up to a desired Å
and move them to a new directory.

Commandline inputs: 1) directory of pdb files with full path 
                    2) maximum desired resolution in Å

e.g python3 filter_by_resolution.py directory_path 5

#*****************************************************************
compile_angles.py

Descritption:
The program takes a directory of Chothia numbered PDB files of antibodies and uses the coordinates to calculate
the packing angle between the VH and VL domains and outputs a .csv file containing columns with the pdb code and the packing angle
e.g.
      pdb       angle
   6NOV_2  -44.016817

The program uses another external program called abpackingangle, which needs to be installed and in the path. 
For more information on abpackingangle: https://github.com/ACRMGroup/abpackingangle

Commandline inputs: 1) directory which contains .pdb files for processing
                    2) name of outputted .csv file

e.g python3 compile_angles.py directory_path VHVL_angles


#*****************************************************************
find_VHVLres.py

Description:
The program will take PDB files and extract a string of one letter residue codes for the VH-VL-Packing relevant region
and deposit it into csv file
e.g.
      code L/H position residue
    5DMG_2          L38       Q
    5DMG_2          L40       P
    5DMG_2          L41       G
    5DMG_2          L44       P

Commandline inputs: 1) directory path for where the .pdb files are stored
                    2) name of outputted .csv file

e.g. python3 find_VHVLres.py directory_path VH_res

#*****************************************************************
encode_4d.py/ encode_ts.py/ encode_4dts.py

Description:
Program uses the residue identities for VH/VL relevant residues and encodes them using x method library then appends the packing angle to produce a data table:
e.g.

code	L38a	L38b	L38c	L38d	L40a	...     angle
12E8_1	0	       5	   4	-0.69	   0            -54.9
12E8_2	0	       5	   4	-0.69	   0            -48.5
15C8_1	0	       5	   4	-0.69	   0            -42.3
1A0Q_1	0.5	       6	   4	-0.4	   0            -45.6

Note: for this and the subsequent programs, a .dat file will need to be created that contains all of the names for the columns that will be created.
e.g
code
L38a
L38b
L38c
L38d
L38e
L40a
L40b
...
angle

Commandline inputs: 1) .csv file containing the identities of residues at the VHVL positions
                    2) file containing the packing angles for each .pdb
                    3) the .dat file that contains all of the names for the encoded columns e.g. code, L38a, L38b, ..., H105e, angle.
                    4) name of outputted .csv file

e.g python3 encode_4d.py VHVL_res.csv VHVL_ang.csv 4d.dat 4d_enc

#*****************************************************************
filter_dup.py

Description:
The program will take take the output .csv file that contains encoded sequence and angles and if the sequence of
residues are the same for a pdb, it'll average the angle to produce one angle per sequence.

Commandline input: 1) encoded .csv file
                   2) .dat file with column names
                   3) outtput name for no_dup_{}.csv

e.g. python3 filter_dup.py 4d_enc.csv 4d.dat no_dup_4d

#*****************************************************************
csv2arff

Description:
The program takes a .csv file containing the encoded residues and angles and converts it into an .arff file.
The program must be installed and in the path. 
For more information: https://github.com/AndrewCRMartin/bioscripts/blob/master/csv2arff.pl

e.g. csv2arff -ni input.dat angle norm_4d.csv > norm4d.arff

#*****************************************************************
normalize.py

Description:
Program takes the .csv files containing encoded residues and angles and normalizes the angle to be between -1 and 1.

Commandline inputs: 1) .csv file with angles and encoded residues
                    2) .dat file with column headers
                    3) name of .csv file that will be outputted

e.g. python3 normalize.py no_dup_4d.csv 4d.dat 4d