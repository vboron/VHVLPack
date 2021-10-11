FOLDS=10
export WEKA=/usr/local/apps/weka-3-8-3
export CLASSPATH=$WEKA/weka.jar

# Training option selection
BASEPATH=$(pwd)
DATA=${BASEPATH}/xval_files
CLASSIFIER=weka.classifiers.functions.MultilayerPerceptron

for ((i=1;i<=FOLDS;i++)); do
       echo "*** Training on set $i ***"
       # train
       java $CLASSIFIER -v -x 10 -t ${DATA}/VHVL_${i}_train.arff -d ${DATA}/VHVL_${i}_MP.model > ${DATA}/VHVL_${i}_MP_train.log
       # test
       java $CLASSIFIER -v -T ${DATA}/VHVL_${i}_test.arff -l ${DATA}/VHVL_${i}_MP.model >${DATA}/VHVL_${i}_MP_test.log  
done

r = `grep Correlation *test.log | awk '{print $3}'`

# To apply the predictor to one or more examples where you wish to
# make an actual prediction you create a .arff file containing the
# example(s) but with the output set to '?' and then run as in testing
# but add the flag -p 0
# i.e.
# java $CLASSIFIER -T myinputfile.arff -p 0 -l mytrained.model 
