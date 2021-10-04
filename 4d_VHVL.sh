set -x

compile_angles.py xray_5A_pdbs VHVL_ang

find_VHVLres.py xray_5A_pdbs VHVL_res

encode_4d.py VHVL_res.csv VHVL_ang.csv 4d.dat 4d_enc

filter_dup.py 4d_enc.csv 4d.dat 4d

csv2arff -ni in4d.dat angle no_dup_4d.csv > 4d.arff



