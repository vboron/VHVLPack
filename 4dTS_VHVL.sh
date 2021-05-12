set -x

python3 compile_angles.py xray_5A_pdbs VHVL_ang

python3 find_VHVLres.py xray_5A_pdbs VHVL_res

python3 encode_4dts.py VHVL_res.csv VHVL_ang.csv 4dts.dat 4dts_enc

python3 filter_dup.py 4dts_enc.csv 4dts.dat no_dup_4dts

csv2arff -ni in4dts.dat angle no_dup_4dts.csv > 4dts.arff

python3 normalize.py no_dup_4dts.csv 4dts.dat 4dts

csv2arff -ni in4dts.dat angle norm_4dts.csv > norm4dts.arff
