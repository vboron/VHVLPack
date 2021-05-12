set -x

python3 compile_angles.py xray_5A_pdbs VHVL_ang

python3 find_VHVLres.py xray_5A_pdbs VHVL_res

python3 encode_ts.py VHVL_res.csv VHVL_ang.csv ts.dat ts_enc

python3 filter_dup.py ts_enc.csv ts.dat no_dup_ts

csv2arff -ni in_ts.dat angle no_dup_ts.csv > ts.arff

python3 normalize.py no_dup_ts.csv ts.dat ts

csv2arff -ni in_ts.dat angle norm_ts.csv > normts.arff


