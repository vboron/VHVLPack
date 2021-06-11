set -x

python3 filter_by_resolution.py LH_Combined_Chothia 5

python3 compile_angles.py xray_5A_pdbs VHVL_ang

python3 find_VHVLres.py xray_5A_pdbs VHVL_res

python3 encode_ts.py VHVL_res.csv VHVL_ang.csv ts.dat ts_enc

python3 filter_dup.py ts_enc.csv ts.dat ts

python3 remove_redundancy.py  no_dup_ts.csv ts.dat ts 

python3 column_sgpdb.py no_red_ts.csv ts.dat ts

python3 split_10.py final_no_red_ts.csv ts.dat xval_files

./csv2arff_all.sh

./runWekaMLP10FXval.sh

python3 getRELRMSEandCoeff.py xval_files final_no_red_ts.csv ts.dat 




