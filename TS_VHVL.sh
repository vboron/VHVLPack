set -x

# echo "Launching CompileVHVLPackingAngles.py"
python3 CompileVHVLPackingAngles.py xray_5A_pdbs

# echo "Launching findVHVLResidues.py"
python3 findVHVLResidues.py xray_5A_pdbs

# echo "Launching encodingbyTScale.py"
python3 encodingbyTScale.py VHVL_Packing_Residues.csv VHVL_Packing_Angles.csv

# echo "Launching filter_duplicates_4d.py"
python3 filter_dup_ts.py VHVLres_and_angles_t.csv

# echo "Launching csv2arff"
csv2arff -ni in2.dat angle no_duplicates_TScaleData.csv > TScale.arff

python3 norm_ts.py no_duplicates_TScaleData.csv 

csv2arff -ni in2.dat angle norm_angles_ts.csv > normTS.arff


