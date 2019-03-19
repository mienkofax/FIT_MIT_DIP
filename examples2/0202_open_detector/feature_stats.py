from os.path import dirname, abspath, join
import sys
import csv
import time
from datetime import timedelta
import logging

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.ConnectionUtil import ConnectionUtil
from dm.Performance import Performance
from dm.Attributes import *


processes = [
    '//DIP/clean/DecisionTree',
    '//DIP/clean/DeepLearning',
    '//DIP/clean/NaiveBayes',
    '//DIP/clean/RandomForest',
    '//DIP/clean/SVM',

    '//DIP/filter/correlation/DecisionTree',
    '//DIP/filter/correlation/DeepLearning',
    '//DIP/filter/correlation/NaiveBayes',
    '//DIP/filter/correlation/RandomForest',
    '//DIP/filter/correlation/SVM',

    '//DIP/filter/gain_ratio/DecisionTree',
    '//DIP/filter/gain_ratio/DeepLearning',
    '//DIP/filter/gain_ratio/NaiveBayes',
    '//DIP/filter/gain_ratio/RandomForest',
    '//DIP/filter/gain_ratio/SVM',

    '//DIP/filter/pca/DecisionTree',
    '//DIP/filter/pca/DeepLearning',
    '//DIP/filter/pca/NaiveBayes',
    '//DIP/filter/pca/RandomForest',
    '//DIP/filter/pca/SVM',

    '//DIP/filter/relief/DecisionTree',
    '//DIP/filter/relief/DeepLearning',
    '//DIP/filter/relief/NaiveBayes',
    '//DIP/filter/relief/RandomForest',
    '//DIP/filter/relief/SVM',

    '//DIP/filter/svm/DecisionTree',
    '//DIP/filter/svm/DeepLearning',
    '//DIP/filter/svm/NaiveBayes',
    '//DIP/filter/svm/RandomForest',
    '//DIP/filter/svm/SVM',

    '//DIP/clean/NeuralNet',
    '//DIP/filter/correlation/NeuralNet',
    '//DIP/filter/gain_ratio/NeuralNet',
    '//DIP/filter/pca/NeuralNet',
    '//DIP/filter/relief/NeuralNet',
    '//DIP/filter/svm/NeuralNet',

    # '//DIP/wrapper/backward/OptimizeSelectionDecisionTree',
    # '//DIP/wrapper/backward/OptimizeSelectionDeepLearning',
    # '//DIP/wrapper/backward/OptimizeSelectionNaiveBayes',
    # '//DIP/wrapper/backward/OptimizeSelectionNeuralNet',
    # '//DIP/wrapper/backward/OptimizeSelectionSVM',

    # '//DIP/wrapper/forward/OptimizeSelectionDecisionTree',
    # '//DIP/wrapper/forward/OptimizeSelectionDeepLearning',
    # '//DIP/wrapper/forward/OptimizeSelectionNaiveBayes',
    # '//DIP/wrapper/forward/OptimizeSelectionNeuralNet',
    # '//DIP/wrapper/forward/OptimizeSelectionSVM',
]

OUTPUT_FILENAME = 'out.csv'
BEFORE_TIME = 10 * 60
AFTER_TIME = 10 * 60

from subprocess import PIPE, run
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    logging.info('start')

    launcher = ConnectionUtil.rapid_miner()['launcher']
    out = {}
    header = '{0:40} '.format('               filter')
    header += '{0:8}   '.format('accuracy')
    header += '{0:12}   '.format('not_true_not')
    header += '{0:13}   '.format('open_true_not')
    header += '{0:14}   '.format('open_true_open')
    header += '{0:13}   '.format('not_true_open')

    header += '{0:8}   '.format('accuracy')
    header += '{0:12}   '.format('not_true_not')
    header += '{0:13}   '.format('open_true_not')
    header += '{0:14}   '.format('open_true_open')
    header += '{0:13}   '.format('not_true_open')

    header += '{0:9}  '.format('duration')
    header += '{0:9}  '.format('duration')

    logging.debug(header)

    for process in processes:
        if os.path.isfile('out.csv'):
            os.remove('out.csv')

        cmd = [
            launcher,
            process
        ]

        start_time = time.monotonic()
        result = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        end_time = time.monotonic()
        duration = timedelta(seconds=end_time - start_time)

        output = '{0:40} '.format(process)

        if os.path.isfile('out.csv'):
            start_time2 = time.monotonic()
            p = Performance(abspath(OUTPUT_FILENAME))
            _, _, p1 = p.simple()
            table2, wrong2, p2 = p.with_delay(BEFORE_TIME, AFTER_TIME)
            end_time2 = time.monotonic()
            duration2 = timedelta(seconds=end_time2 - start_time2)

            output += '{0:6.2f}%'.format(p1['accuracy'])
            output += '{0:12}   '.format(p1['nothing_as_true_nothing'])
            output += '{0:13}   '.format(p1['open_as_true_nothing'])
            output += '{0:14}   '.format(p1['open_as_true_open'])
            output += '{0:13}   '.format(p1['nothing_as_true_open'])
            output += '    {0:6.2f}%'.format(p2['accuracy'])
            output += '{0:12}   '.format(p2['nothing_as_true_nothing'])
            output += '{0:13}   '.format(p2['open_as_true_nothing'])
            output += '{0:14}   '.format(p2['open_as_true_open'])
            output += '{0:13}   '.format(p2['nothing_as_true_open'])
            output += '    {0}  {1}'.format(str(duration)[:9], str(duration2)[:9])
            logging.debug(output)
        else:
            logging.error('{0:190} {1}  0:00:00.0'.format(process, str(duration)[:9]))
