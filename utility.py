from datetime import datetime
import pandas

data_path = './data/{0}.csv'

def get_nodes():
    return pandas.read_csv(data_path.format('Nodes_FishermansWharf'))


def get_edges(distance=False):
    if distance:
        return pandas.read_csv(data_path.format('Edges_FishermansWharf_with_Distance'))
    else:
        return pandas.read_csv(data_path.format('Edges_FishermansWharf'))


def get_availability():
    df = pandas.read_csv(data_path.format('real_time_data'))

    def convert_to_datetime(date_time_str):
        date_str, time_str = date_time_str.split()
        year, month, day = [int(i) for i in date_str.split('-')]
        time_str, millisecond = time_str.split('.')
        hour, minute, second = [int(i) for i in time_str.split(':')]
        millisecond = int(millisecond)
        return datetime(year, month, day, hour, minute, second, millisecond)

    df['timestamp'] = df['timestamp'].apply(convert_to_datetime)
    return df
