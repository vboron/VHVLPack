set -x

# echo "Launching CompileVHVLPackingAngles.py"
python3 CompileVHVLPackingAngles.py xray_5A_pdbs

# echo "Launching findVHVLResidues.py"
python3 findVHVLResidues.py xray_5A_pdbs

# echo "Launching combine_encoding_4dTScale.py"
python3 encode_4dts.py VHVL_Packing_Residues.csv VHVL_Packing_Angles.csv

# echo "Launching filter_duplicates_4d.py"
python3 filter_dup_4dTS.py VHVLres_and_angles_4dTS.csv

# echo "Launching csv2arff"
csv2arff -ni in3.dat angle no_duplicates_4dTSData.csv > 4dTS.arff

python3 norm_ts.py no_duplicates_4dTSData.csv

csv2arff -ni in3.dat angle norm_angles_ts.csv > norm4dTS.arff

