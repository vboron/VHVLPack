set -x

# ./filter_by_resolution.py LH_Combined_Chothia 5

./compile_angles.py cleanpdbstructures VHVL_ang_xval

./find_VHVLres.py cleanpdbstructures VHVL_res_xval

./encode_ts.py VHVL_res_xval.csv VHVL_ang_xval.csv ts.dat ts_enc_xval

./filter_dup.py ts_enc_xval.csv ts.dat ts_xval

./split_10.py no_dup_ts_xval.csv ts.dat xval_cleanpdbstructures

# ./csv2arff_all.sh

# ./runWekaMLP10FXval.sh
