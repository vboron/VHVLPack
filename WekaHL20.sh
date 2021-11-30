# set -x 

export WEKA=/usr/local/apps/weka-3-8-3
export CLASSPATH=$WEKA/weka.jar

CLASSIFIER=weka.classifiers.functions.MultilayerPerceptron

BASEPATH=$(pwd)
DATASET=${BASEPATH}/
TEST=${DATASET}/testing_data
ARFFFILES=${TEST}'/'*.arff
TRAIN=
INPUTS=
MODEL=${DATASET}/

java $CLASSIFIER -v -x 3 -H 20 -t ${TRAIN} -d ${MODEL}.model > ${DATASET}_train.log

for file in ${ARFFFILES}; do
        name=$(echo "$file" | cut -f 1 -d '.')
        java $CLASSIFIER -v -T $file -p 0 -l ${MODEL}.model > ${name}_test.log
done