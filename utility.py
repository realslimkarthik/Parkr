import pandas

data_path = './data/{0}.csv'

def get_nodes():
    return pandas.read_csv(data_path.format('Nodes_FishermansWharf'))


def get_edges(distance=False):
    if distance:
        return pandas.read_csv(data_path.format('Edges_FishermansWharf_with_Distance'))
    else:
        return pandas.read_csv(data_path.format('Edges_FishermansWharf'))

