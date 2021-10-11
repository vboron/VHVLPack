set -x
./compile_angles.py xray_5A_pdbs_5Ksamples VHVL_ang_5k
./find_VHVLres.py xray_5A_pdbs_5Ksamples VHVL_res_5k
./encode_ts.py VHVL_res_5k.csv VHVL_ang_5k.csv ts.dat ts_enc_5k
./filter_dup.py ts_enc_5k.csv ts.dat ts_5k
./compile_angles.py xray_5A_files_unique_to_af2data VHVL_ang_af2
./find_VHVLres.py xray_5A_files_unique_to_af2data VHVL_res_af2
./encode_ts.py VHVL_res_af2.csv VHVL_ang_af2.csv ts.dat ts_enc_af2
./filter_dup.py ts_enc_af2.csv ts.dat ts_af2
./run_Weka_on_varied_HL.sh
