FOLDS=10
export WEKA=${HOME}/weka-3-8-3/
export CLASSPATH="$WEKA/weka.jar"

# Training option selection
BASEPATH=$(pwd)
INPUTS=${BASEPATH}/in_ts.dat
DATA=${BASEPATH}/xval_files
CLASSIFIER=weka.classifiers.functions.MultilayerPerceptron

for ((i=1;i<=FOLDS;i++)); do
   csv2arff -v -norm -ni -skip $INPUTS dataset $DATA/train${i}.csv > VHVL_${i}_train.arff
   csv2arff -v -norm -ni -skip $INPUTS dataset $DATA/test${i}.csv  > VHVL_${i}_test.arff
       echo "*** Training on set $i ***"
       # train
       java $CLASSIFIER -attribute-importance -x 10 -t VHVL_${i}_train.arff -d VHVL_${i}_MP.model
       # test
       java $CLASSIFIER -T VHVL_${i}_test.arff -l VHVL_${i}_MP.model >VHVL_${i}.out   
done

# To apply the predictor to one or more examples where you wish to
# make an actual prediction you create a .arff file containing the
# example(s) but with the output set to '?' and then run as in testing
# but add the flag -p 0
# i.e.
# java $CLASSIFIER -T myinputfile.arff -p 0 -l mytrained.model 
