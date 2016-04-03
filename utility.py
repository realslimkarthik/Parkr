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


def get_availability(with_time=False):
    if with_time:
        df = pandas.read_csv(data_path.format('real_time_data_with_time'))
    else:
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


def get_block_availability(block_id, time):
    availability_df  = get_availability()
    block_availability_df = availability_df[availability_df['block_id'] == block_id]
    block_availability_timed_df = block_availability_df[block_availability_df['timestamp'] == time]
    if block_availability_timed_df.empty:
        block_availability_timed_df = block_availability_df[block_availability_df['timestamp'] < time]
        last_block = block_availability_timed_df.max().available
    return last_block


def get_node_from_block(block_id):
    edges_df = get_edges()
    block = edges_df[edges_df['block_id'] == block_id].iloc[0]
    node1 = block.node_id_1
    node2 = block.node_id_2
    return node1, node2


def get_node_id_from_long_lat(longitude, latitude):
    nodes_df = get_nodes()
    long_df = nodes_df[nodes_df['longitude'] == longitude & nodes_df['latitude'] == latitude]
    long_lat_node = long_df.iloc[0]
    node_id = long_lat_node.block_id
    return node_id


def get_long_lat(node_id):
    nodes_df = get_nodes()
    row = nodes_df[nodes_df['node_id'] == node_id]
    longitude = row.longitude
    latitude = row.latitude
    long_lat = [float(longitude), float(latitude)]
    return long_lat


def get_distance(node1, node2):
    distance_df = get_distances()
    row = distance_df[(distance_df['node_id_1'] == node1) & (distance_df['node_id_2'] == node2)].iloc[0]
    distance = row.distance
    return distance


def _value_in_datetime(datetime_object, value, attribute):
    attribute = attribute.lower()
    value_in_datetime = False
    existing_value = getattr(datetime_object, attribute)
    
    if existing_value == value:
        value_in_datetime = True

    return value_in_datetime



def get_block_probability(block_id, time, fine_grained=True):
    day = time.day
    weekday = time.weekday()
    hour = time.hour
    minute = time.minute
    availability_df = get_availability(with_time=True)
    block_df = availability_df[availability_df['block_id'] == block_id]
    if fine_grained:
        day_df = block_df[block_df['weekday'] == weekday]
    else:
        working_days = range(0, 5)
        weekends = range(5, 7)
        if weekday in working_days:
            day_df = block_df[block_df['weekday'].isin(working_days)]
        else:
            day_df = block_df[block_df['weekday'].isin(weekends)]

    day_time_df = day_df[day_df['hour'] == hour]
    probability = (day_time_df['available'] / day_time_df['no_blocks']).mean()

    return probability

