set -x 

export WEKA=/usr/local/apps/weka-3-8-3
export CLASSPATH=$WEKA/weka.jar

# Training option selection
BASEPATH=$(pwd)
DATA=${BASEPATH}/single_csv
CSVFILES=${DATA}'/*.csv'
ARFFFILES=${DATA}'/*.arff'
INPUTS=${BASEPATH}/in_ts.dat
CLASSIFIER=weka.classifiers.functions.MultilayerPerceptron

echo '*** Converting training set to arff ***'
# csv2arff for train file
csv2arff -v -ni $INPUTS angle ${BASEPATH}/final_no_red_ts.csv > VHVL_train.arff
echo "*** Training ***"
# train
java $CLASSIFIER -v -H 10 -t VHVL_train.arff -d VHVL.model > VHVL_train.log

for file in ${CSVFILES}; do
    echo '*** Converting test file' $file 'to .arff ***'
    name=$(echo "$file" | cut -f 1 -d '.')
    csv2arff -v -ni $INPUTS angle $file > $name.arff

    echo '*** Testing ' $file ' ***'
    # test
    done

for file in ${ARFFFILES}; do
    java $CLASSIFIER -v -T $file -p 0 -l VHVL.model >${DATA}/$file_test.log  
done



# To apply the predictor to one or more examples where you wish to
# make an actual prediction you create a .arff file containing the
# example(s) but with the output set to '?' and then run as in testing
# but add the flag -p 0
# i.e.
# java $CLASSIFIER -T myinputfile.arff -p 0 -l mytrained.model 