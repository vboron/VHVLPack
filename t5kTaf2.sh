set -x
./compile_angles.py clean_LHChothia VHVL_ang_5k
./find_VHVLres.py clean_LHChothia VHVL_res_5k
./encode_ts.py VHVL_res_5k.csv VHVL_ang_5k.csv ts.dat ts_enc_5k
./filter_dup.py ts_enc_5k.csv ts.dat ts_5k
./compile_angles.py clean_unique_af2 VHVL_ang_af2
./find_VHVLres.py clean_unique_af2 VHVL_res_af2
./encode_ts.py VHVL_res_af2.csv VHVL_ang_af2.csv ts.dat ts_enc_af2
./filter_dup.py ts_enc_af2.csv ts.dat ts_af2
./run_Weka_on_varied_HL.sh