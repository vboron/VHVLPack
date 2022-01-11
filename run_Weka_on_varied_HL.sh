# set -x 

export WEKA=/usr/local/apps/weka-3-8-3
export CLASSPATH=$WEKA/weka.jar

# Training option selection
BASEPATH=$(pwd)
DATA=${BASEPATH}/PostAF2/testing_data
CSVFILES=${DATA}'/'*.csv
ARFFFILES=${DATA}'/'*.arff
INPUTS=${BASEPATH}/in4d.dat
CLASSIFIER=weka.classifiers.functions.MultilayerPerceptron
TRAIN=PreAF2/Da2_4d.arff
MODEL=${DATA}/Ea.model
SETNAME=Ea
SETPATH=${DATA}/${SETNAME}

LAYERS=20

# split lines into separate .csv files
./lines2files.py PostAF2/Ea.csv 4d.dat ${DATA}

# echo '*** Converting training set to arff ***'
# csv2arff for train file
# csv2arff -v -ni $INPUTS angle ${BASEPATH}/no_dup_ts_5k.csv > af2_train_5Kfiles.arff

for file in ${CSVFILES}; do
	echo '*** Converting test file' $file 'to .arff ***'
	name=$(echo "$file" | cut -f 1 -d '.')
	csv2arff -v -ni $INPUTS angle $file > $name.arff
done

# i starts at the min number of hidden layers we want to test (here 20) and ends at the max specified before
# for ((i=20;i<=LAYERS;i++)); do
echo "*** Training with -H 20 ***"
# train
java $CLASSIFIER -v -H 20 -t ${TRAIN} -d ${MODEL} > ${SETPATH}_train.log

for file in ${ARFFFILES}; do
    echo '*** Testing' $file 'with' $i 'Hidden layers ***'
    name=$(echo "$file" | cut -f 1 -d '.')
    java $CLASSIFIER -v -T $file -p 0 -l ${MODEL} > ${name}_Ea_test.log
done
# done
