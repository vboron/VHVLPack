export WEKA=/usr/local/apps/weka-3-8-3
export CLASSPATH=$WEKA/weka.jar

# Training option selection
BASEPATH=$(pwd)
DATA=${BASEPATH}'/'xval_cleanpdbstructures
CLASSIFIER=weka.classifiers.functions.MultilayerPerceptron
FOLDS=10

for ((i=1;i<=FOLDS;i++)); do
       echo "*** Training on set $i ***"
       # train
       java $CLASSIFIER -v -x 10 -t ${DATA}/train_${i}.arff -d ${DATA}/fold_${i}.model > ${DATA}/${i}_train.log
       # test
       java $CLASSIFIER -v -T ${DATA}/test_${i}.arff -l ${DATA}/fold_${i}.model >${DATA}/${i}_test.log  
done
