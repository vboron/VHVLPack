set -x
BASEPATH=$(pwd)
DATA=${BASEPATH}/clean_unique_af2
INPUTS=${BASEPATH}/in_ts.dat
CSVFILES=${DATA}'/'*.csv
DST=${BASEPATH}/SNNS/af2_snns
ARFFFILES=${DST}'/'*.arff
mkdir ${DST}
for file in ${CSVFILES}; do
        echo '*** Converting test file' $file 'to .arff ***'
        name=$(basename ${file})
	name="${name%.*}"
        csv2arff -v -norm -ni ${INPUTS} angle ${file} > ${DST}/${name}.arff
done

for file in ${ARFFFILES}; do
        echo '*** Converting test file ${file} to .pat ***'
        name=$(basename ${file})
	name="${name%*}"
        arff2snns ${file} > ${DST}/${name}.pat
done
