set -x
BASEPATH=$(pwd)
DATA=${BASEPATH}'/'cleanpdbstructures
CSVFILES=${DATA}'/'*.csv
INPUTS=${BASEPATH}/in_ts.dat

for file in ${CSVFILES}; do
     echo '*** Converting test file' $file 'to .arff ***'
     name=$(echo "$file" | cut -f 1 -d '.')
     csv2arff -v -ni $INPUTS angle $file > $name.arff
done
