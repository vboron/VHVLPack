# Predicting the torsion angle between VH and VL domains of the variable region of the antibody

The torsion angle which was defined as part of Abhinadan and Martin's<sup>1</sup> paper, can be used to define the position of VH and VL regions relative to each other. This can then be integrated into structure predicting software to improve the accuracy of the biding region modeling.  

## Using regression models to predict the torsion angle
The main program is run in the following way:  

`./gbr_angle_prediction.py --trainset [name of directory with training pdb files] --testset [name of directory with testing pdb files] --modelname [name which will be applied to the final model] --graphname [name for graph output .jpg] --res [.dat file containing the feature residues] --useloops [True/False]`  

Here a gradient boosted regression model is trained by using defined sets of pdb files as test and train data. The defined .dat file contains a list of residues which are used as features with(out) including the lengths of the CDR L1, L2, and H3. The output of the file is a series of graphs showing the predicted vs actual angles, the squared error vs actual angle, and frequency vs errors in prediction. Also outputted are .csv files with the pdb name, actual angle, predicted angle and error, and summarised statistics for the run.  

<sup>1</sup> Abhinandan KR, Martin AC. Analysis and prediction of VH/VL packing in antibodies. Protein Eng Des Sel. 2010;23(9):689-697. doi:10.1093/protein/gzq043

### Other modules
The main `gbr_angle_prediction.py` is dependent on the following modules in this repo:
`encode_res_calc_angles.py`, `utils.py`, `erca_noloops.py`, `sklearn_methods.py`, `nonred.py`, and `graphing.py`.

## Running a single sequence file
Input file e.g.<br>
      L2 SER<br>
      L3 ALA<br>
      L4 LEU<br>
      L5 THR...<br>
To run single file use: `./abYpack_singfile.py --resfile [path of the .seq file for which an angle is to be predicted] --model [path for the .pkl model (here jul2sept_expres.pkl is the most complete model, used for testing the independent set)]`

