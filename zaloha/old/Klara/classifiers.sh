#!/bin/bash

# -split-percentage <percentage>
#	Sets the percentage for the train/test set split, e.g., 66.
#
# -x <number of folds>
#	Sets number of folds for cross-validation (default: 10).
#
# -T <name of test file>
#	Sets test file. If missing, a cross-validation will be performed
#	on the training data.


WEKA_FILE="/home/klarka/DP/Klara/test.arff"

cd "/home/klarka/Stažené/weka-3-8-2"

java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron \
     -t ${WEKA_FILE} \
     -L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.trees.J48 \
     -t ${WEKA_FILE} \
     -C 0.25 -M 2

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.rules.ZeroR \
     -t ${WEKA_FILE} \

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.bayes.BayesNet \
     -t ${WEKA_FILE} \
     -D -Q weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES -E \
     weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5 

#########################
# zaciatok pre split
#########################
SPLIT=66

echo "+++++++++ split-percentage ${SPLIT} ++++++++++++"

java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron \
     -t ${WEKA_FILE} \
     -split-percentage ${SPLIT} \
     -L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a 

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.trees.J48 \
     -t ${WEKA_FILE} \
     -split-percentage ${SPLIT} \
     -C 0.25 -M 2 

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.rules.ZeroR \
     -t ${WEKA_FILE} \
     -split-percentage ${SPLIT}

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.bayes.BayesNet \
     -t ${WEKA_FILE} \
     -split-percentage ${SPLIT} \
     -D -Q weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES -E \
     weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5 

