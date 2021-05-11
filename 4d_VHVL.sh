set -x

# echo "Launching CompileVHVLPackingAngles.py"
python3 CompileVHVLPackingAngles.py xray_5A_pdbs

# echo "Launching findVHVLResidues.py"
python3 findVHVLResidues.py xray_5A_pdbs

# echo "Launching encodingbyTScale.py"
python3 encode_4d.py VHVL_Packing_Residues.csv VHVL_Packing_Angles.csv

# echo "Launching filter_duplicates_4d.py"
python3 filter_duplicates_4d.py VHVL_res_and_angles_4d.csv

# echo "Launching csv2arff"
csv2arff -ni input.dat angle no_duplicates_4dData.csv > 4d.arff

python3 norm_4d.py no_duplicates_4dData.csv

csv2arff -ni input.dat angle norm_angles_4d.csv > norm4d.arff


