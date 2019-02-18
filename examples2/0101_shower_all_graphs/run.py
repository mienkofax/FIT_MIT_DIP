import logging
import sys
from os.path import dirname, abspath, join

CODE_DIR = abspath(join(dirname(__file__), '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.Graph import Graph
from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.Storage import Storage


def fill_start_end(events):
    for i in range(0, len(events)):
        event = events[i]

        values = []

        duration = event['start_shift'] * (-1) + event['end_shift']
        duration += event['e_end']['timestamp'] - event['e_start']['timestamp']
        for j in range(0, duration):
            time = event['e_start']['timestamp'] + j + event['start_shift']

            if time < event['e_start']['timestamp']:
                values.append(0)
            elif time > event['e_end']['timestamp']:
                values.append(0)
            else:
                values.append(1)

        event['measured']['open_close'] = values

    return events


def generate_file(con, start_shift, end_shift, output_file):
    logging.info('start: ' + output_file)

    graphs = Graph("./../../src/graph")

    # stiahnutie dat
    storage = Storage('examples/events_klarka_shower.json', 0, 'measured_klarka_shower')
    d = storage.load_data(con, start_shift, end_shift, 'temperature_in_celsius')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    logging.info('events after applying the filter: %d' % len(filtered))

    fill_start_end(filtered)

    logging.info('start generating graphs')
    gr = []
    for event in filtered:
        t = DateTimeUtil.utc_timestamp_to_str(event['e_start']['timestamp'], '%d.%m. %H:%M:%S')
        t += ' - '
        t += DateTimeUtil.utc_timestamp_to_str(event['e_end']['timestamp'], '%H:%M:%S')

        g = {
            'title': t,
            'group': 'one',
            'graphs': [
                Graph.db_to_simple_graph(event, 'temperature_in_celsius', 'blue',
                                         'Temperature', 75),
                Graph.db_to_simple_graph(event, 'open_close', 'orange', 'Open', 75),
            ]
        }
        gr.append(g)

        g = {
            'title': t,
            'group': 'two',
            'graphs': [
                Graph.db_to_simple_graph(event, 'rh_in_percentage', 'red',
                                         'Relative humidity [%]', 75),
                Graph.db_to_simple_graph(event, 'open_close', 'orange', 'Open', 75),
            ]
        }
        gr.append(g)

        g = {
            'title': t,
            'group': 'tree',
            'graphs': [
                Graph.db_to_simple_graph(event, 'rh_in_absolute_g_m3', 'green',
                                         'Absolute humidity [g/m3]', 75),
                Graph.db_to_simple_graph(event, 'open_close', 'orange', 'Open', 75),
            ]
        }
        gr.append(g)

        g = {
            'title': t,
            'group': 'four',
            'graphs': [
                Graph.db_to_simple_graph(event, 'rh_in_specific_g_kg', 'purple',
                                         'Specific humidity [g/kg]', 75),
                Graph.db_to_simple_graph(event, 'open_close', 'orange', 'Open', 75),
            ]
        }
        gr.append(g)

    graphs.gen(gr, output_file + '.html', 0, 0, global_range=True)
    logging.info('end generating graphs')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s', )

    con = ConnectionUtil.create_con()

    generate_file(con, 0, 0, 'shower')
    generate_file(con, -900, +900, 'shower_with_shift')