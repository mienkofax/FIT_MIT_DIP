#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as dp
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    client = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=True)
    client.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(client, dp.WeatherData(cache=True))
    storage.read_meta_data('../devices_examples.json', '../events_examples.json')

    dw1 = storage.download_data_for_normalization(['co2'])
    client.logout()

    norm = dp.norm_all(dw1)

    graphs = []
    for item in norm:
        one_values = dp.filter_one_values(item, 'co2')

        g = {
            'title': 'Estimate of measured values',
            'graphs': [
                dp.value_estimate(item, 2, 'red', 'Odhadnuta hodnota 2', 'norm'),
                dp.value_estimate(item, 5, 'blue', 'Odhadnuta hodnota 5', 'norm'),
                dp.value_estimate(item, 12, 'silver', 'Odhadnuta hodnota 12', 'norm'),
                dp.value_estimate(item, 20, 'orange', 'Odhadnuta hodnota 20', 'norm'),
                dp.value_estimate(item, 31, 'purple', 'Odhadnuta hodnota 31', 'norm'),
                dp.gen_simple_graph(one_values, 'green', 'Namerana hodnota', 'norm')
            ]
        }
        graphs.append(g)

        g = {
            'title': 'Estimate of measured values',
            'graphs': [
                dp.value_estimate(item, 2, 'red', 'Odhadnuta hodnota 2', 'value'),
                dp.value_estimate(item, 5, 'blue', 'Odhadnuta hodnota 5', 'value'),
                dp.value_estimate(item, 12, 'silver', 'Odhadnuta hodnota 12', 'value'),
                dp.value_estimate(item, 20, 'orange', 'Odhadnuta hodnota 20', 'value'),
                dp.value_estimate(item, 31, 'purple', 'Odhadnuta hodnota 31', 'value'),
                dp.gen_simple_graph(one_values, 'green', 'Namerana hodnota', 'value')
            ]
        }
        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
