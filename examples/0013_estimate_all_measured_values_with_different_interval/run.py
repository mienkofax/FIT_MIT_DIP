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

    dw1 = storage.download_data_for_normalization(type_id='co2')
    client.logout()

    graphs = []
    for i in range(0, len(dw1)):
        one_values = dw1[i]['data'][0]['values'][0]['measured']

        g = {
            'title': 'Estimate of measured values',
            'graphs': [
                dp.value_estimate(dw1[i], 2, 'red', 'Odhadnuta hodnota 2', 'norm'),
                dp.value_estimate(dw1[i], 5, 'blue', 'Odhadnuta hodnota 5', 'norm'),
                dp.value_estimate(dw1[i], 12, 'silver', 'Odhadnuta hodnota 12', 'norm'),
                dp.value_estimate(dw1[i], 20, 'orange', 'Odhadnuta hodnota 20', 'norm'),
                dp.value_estimate(dw1[i], 31, 'purple', 'Odhadnuta hodnota 31', 'norm'),
                dp.gen_simple_graph(one_values, 'green', 'Namerana hodnota', 'norm')
            ]
        }
        graphs.append(g)

        g = {
            'title': 'Estimate of measured values',
            'graphs': [
                dp.value_estimate(dw1[i], 2, 'red', 'Odhadnuta hodnota 2'),
                dp.value_estimate(dw1[i], 5, 'blue', 'Odhadnuta hodnota 5'),
                dp.value_estimate(dw1[i], 12, 'silver', 'Odhadnuta hodnota 12'),
                dp.value_estimate(dw1[i], 20, 'orange', 'Odhadnuta hodnota 20'),
                dp.value_estimate(dw1[i], 31, 'purple', 'Odhadnuta hodnota 31'),
                dp.gen_simple_graph(one_values, 'green', 'Namerana hodnota')
            ]
        }
        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)