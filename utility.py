from datetime import datetime
import pandas

data_path = './data/{0}.csv'

def get_nodes():
    return pandas.read_csv(data_path.format('Nodes_FishermansWharf'))


def get_edges(distance=False):
    if distance:
        df = pandas.read_csv(data_path.format('Edges_FishermansWharf_with_Distance'))
    else:
        df = pandas.read_csv(data_path.format('Edges_FishermansWharf'))

    df = df[df['block_id'] != -1]
    return df


def get_block_list():
    nodes_df = pandas.read_csv(data_path.format('Edges_FishermansWharf'))
    block_ids = nodes_df[nodes_df['block_id'] != -1]
    return block_ids['block_id']


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


def get_distances():
    return pandas.read_csv(data_path.format('Nodes_FishermansWharf_Distances'))


def get_distance(origin, destination):
    
    dist_text = ""
    dist_value = 0 #in meters

    gmaps = googlemaps.Client(key="AIzaSyDPxsz5WxM_rqmM6ROL97Gthf48qEk5rs0")
    
    # ex: gmaps.distance_matrix(["37.808322,-122.419212"], ["37.808436,-122.414186"])
    dm_result = gmaps.distance_matrix(origin, destination)
    dm_rows = dm_result.get("rows",None)

    for a_dm_row in dm_rows:
        elem_list = a_dm_row.get("elements",None)
        # there should be only one elem since only one origin and destination is passed
        dist_text = elem_list[0].get("distance").get("text")
        dist_value = elem_list[0].get("distance").get("value")
            
    return dist_text, dist_value
