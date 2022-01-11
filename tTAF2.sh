set -x
./compile_angles.py cleanpdbstructures VHVL_ang_tAF2TAF2
./find_VHVLres.py cleanpdbstructures VHVL_res_tAF2TAF2
./encode_ts.py VHVL_res_tAF2TAF2.csv VHVL_ang_tAF2TAF2.csv ts.dat ts_enc_tAF2TAF2
./filter_dup.py ts_enc_tAF2TAF2.csv ts.dat ts_tAF2TAF2
