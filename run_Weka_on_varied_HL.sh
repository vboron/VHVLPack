# set -x 

export WEKA=/usr/local/apps/weka-3-8-3
export CLASSPATH=$WEKA/weka.jar

# Training option selection
BASEPATH=$(pwd)
DATA=${BASEPATH}/clean_unique_af2
CSVFILES=${DATA}'/'*.csv
ARFFFILES=${DATA}'/'*.arff
INPUTS=${BASEPATH}/in_ts.dat
CLASSIFIER=weka.classifiers.functions.MultilayerPerceptron
LAYERS=30

# split lines into separate .csv files
./lines2files.py no_dup_ts_af2.csv ts.dat clean_unique_af2

echo '*** Converting training set to arff ***'
# csv2arff for train file
csv2arff -v -ni $INPUTS angle ${BASEPATH}/no_dup_ts_5k.csv > af2_train_5Kfiles.arff

for file in ${CSVFILES}; do
	echo '*** Converting test file' $file 'to .arff ***'
	name=$(echo "$file" | cut -f 1 -d '.')
	csv2arff -v -ni $INPUTS angle $file > $name.arff
done

# i starts at the min number of hidden layers we want to test (here 20) and ends at the max specified before
for ((i=10;i<=LAYERS;i++)); do
    echo "*** Training with -H $i ***"
    # train
    java $CLASSIFIER -v -H $i -t af2_train_5Kfiles.arff -d VHVL_$i.model > ${DATA}/$i_train.log

    for file in ${ARFFFILES}; do
        echo '*** Testing' $file 'with' $i 'Hidden layers ***'
        name=$(echo "$file" | cut -f 1 -d '.')
        java $CLASSIFIER -v -T $file -p 0 -l VHVL_$i.model > ${name}_${i}_test.log
    done
done
