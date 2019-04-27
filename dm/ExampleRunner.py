#!/usr/bin/env bash

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from subprocess import run
from dm.Performance import Performance
from dm.ConnectionUtil import ConnectionUtil


class ExampleRunner:
    @staticmethod
    def detector(before, after, script_name, process, enable_training):
        launcher = ConnectionUtil.rapid_miner()['launcher']

        if enable_training:
            run(['python3', script_name], universal_newlines=True)

        run([launcher, process], universal_newlines=True)

        p = Performance(abspath('out.csv'))

        table, _, _ = p.simple()
        print(table)

        table, wrong, _ = p.with_delay(before, after)
        print(table)

        for row in wrong:
            print(row)

        run(['notify-send', 'PyCharm', 'Koniec generovania'])

    @staticmethod
    def feature_stats(script_name, enable_training):
        if enable_training:
            run(['python3', script_name], universal_newlines=True)

        run(['python3', 'feature_stats.py'], universal_newlines=True)
        run(['notify-send', 'PyCharm', 'Koniec generovania'])
