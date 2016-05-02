import csv
from datetime import datetime
import random
import pandas
from numpy import isnan


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
    df = pandas.read_csv(data_path.format('real_time_data_with_time_live'))

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


def reset_live_data(congestion=0):
    df = pandas.read_csv(data_path.format('real_time_data_with_time'))
    df = introduce_congestion(df, congestion)
    df.to_csv(data_path.format('real_time_data_with_time_live'), index=False)


def introduce_congestion(df, congestion):
    if congestion >= 1 and congestion <= 10:
        return pandas.read_csv(data_path.format('real_time_data_with_time_c10_live'))
    elif congestion > 10 and congestion <= 20:
        return pandas.read_csv(data_path.format('real_time_data_with_time_c20_live'))
    elif congestion > 20 and congestion <= 30:
        return pandas.read_csv(data_path.format('real_time_data_with_time_c30_live'))
    elif congestion > 30 and congestion <= 60:
        return pandas.read_csv(data_path.format('real_time_data_with_time_c60_live'))
    total_spots = sum([i for i in df['available']])
    number_of_removed_spots = (congestion * total_spots) // 100
    new_df = pandas.DataFrame([], columns=df.columns)
    if congestion == 0:
        new_df = df
    else:
        for i in range(0, len(df)):
            row = df.iloc[i].copy()
            if row.available > 0:
                num = random.randint(0, row.available)
                row.available = row.available - num
                number_of_removed_spots -= num
            new_df = new_df.append(row)
    return new_df


def remove_block(block_id, timestamp):
    availability_df = get_availability()
    last_block = get_last_block_row(block_id, timestamp)
    availability = last_block.available - 1
    no_blocks = last_block.no_blocks
    block_availability_df = availability_df[availability_df['timestamp'] == timestamp]
    if not block_availability_df.empty:
        availability_df = availability_df[(availability_df['timestamp'] != timestamp) & (availability_df['block_id'] != block_id)]
    day = timestamp.day
    weekday = timestamp.weekday
    month = timestamp.month
    hour = timestamp.hour
    availability_df = availability_df.append({'block_id': block_id, 'timestamp': timestamp, 'day': day,
        'month': month, 'hour': hour, 'weekday': weekday, 'no_blocks': no_blocks, 'available': availability})
    availability_df.to_csv(data_path.format('real_time_data_with_time_live'))


def get_last_block_row(block_id, time):
    availability_df  = get_availability()
    block_availability_df = availability_df[availability_df['block_id'] == block_id]
    block_availability_timed_df = block_availability_df[block_availability_df['timestamp'] == time]
    if block_availability_timed_df.empty:
        block_availability_timed_df = block_availability_df[block_availability_df['timestamp'] < time]
    last_block = block_availability_timed_df.max()
    return last_block


def get_block_availability(block_id, time):
    last_block = get_last_block_row(block_id, time)
    return last_block.available


def get_adjacent_nodes(node_id):
    edges_df = get_edges()
    edges_df = edges_df[(edges_df['node_id_1'] == node_id) | (edges_df['node_id_2'] == node_id)]
    nodes_set = set()
    for row in edges_df.iterrows():
        node1 = row[1].node_id_1
        node2 = row[1].node_id_2
        nodes_set.add(node1)
        nodes_set.add(node2)
    nodes = [node for node in nodes_set if node != node_id]
    return nodes


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


def get_node_name(node_id):
    nodes_df = get_nodes()
    row = nodes_df[nodes_df['node_id'] == int(node_id)]
    node_name = row.iloc[0].block_name
    return node_name


def get_distance_from_block_to_node(block_id, node_id):
    node1, node2 = get_node_from_block(block_id)
    if node1 == node_id:
        block_distance = get_distance(node_id, node2)
        current_node = node2
    elif node2 == node_id:
        block_distance = get_distance(node_id, node1)
        current_node = node1
    else:
        block_distance_to_node1 = get_distance(node_id, node1)
        block_distance_to_node2 = get_distance(node_id, node2)
        if block_distance_to_node1 >= block_distance_to_node2:
            current_node = node1
            block_distance = block_distance_to_node1
        else:
            current_node = node2
            block_distance = block_distance_to_node2
    return current_node, block_distance


def get_distance(node1, node2):
    distance_df = get_distances()
    row = distance_df[(distance_df['node_id_1'] == node1) & (distance_df['node_id_2'] == node2)].iloc[0]
    distance = row.distance
    return distance


def get_distance_google_maps(origin, destination):
    
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
    availability_df = get_availability()
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
    if isnan(probability):
        probability = 0
    return probability


def format_results(data):
    fieldnames = ['input_no', 'distance', 'uninformed_search_distance', 'walking_distance', 'running_time']
    formatted_data = {'input_no': data['input_no'], 'distance': data['distance'], 'walking_distance': data['walking_distance'], \
        'uninformed_search_distance': data['uninformed_search_distance'], 'running_time': data['running_time']}
    # for row_num, row in enumerate(data):
    #     data_row = {'input_no': row_num + 1, 'distance': row['distance'], 'walking_distance': row['walking_distance'], \
    #     'uninformed_search_distance': row['uninformed_search_distance'], 'running_time': row['running_time']}
    #     formatted_data.append(data_row)
    return formatted_data, fieldnames


def write_results_to_file(data, fieldnames, file_name, header=False):
    formatted_data, new_fields = format_results(data)
    with open(file_name, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=new_fields)
        if header:
            writer.writeheader()
        writer.writerow(formatted_data)


def read_input_from_file(input_file, skip_rows):
    df = pandas.read_csv(input_file, skiprows=skip_rows)
    df.columns = ['origin', 'destination', 'time']

    def convert_to_datetime(date_time_str):
        date_str, time_str = date_time_str.split()
        year, month, day = [int(i) for i in date_str.split('-')]
        time_str, millisecond = time_str.split('.')
        hour, minute, second = [int(i) for i in time_str.split(':')]
        millisecond = int(millisecond)
        return datetime(year, month, day, hour, minute, second, millisecond)

    df['time'] = df['time'].apply(convert_to_datetime)

    input_data = df.to_dict('records')
    return input_data

def get_node_id_from_name(nodename):
    nodes_df = get_nodes()
    node = nodes_df[nodes_df['block_name'] == nodename]  
    return node.iloc[0].node_id

def convert_to_datetime_duplicate(date_time_str):
    print(date_time_str.split())
    date_str, time_str, clock_str = date_time_str.split()
    month, day, year = [int(i) for i in date_str.split('/')]
    
    hour, minute = [int(i) for i in time_str.split(':')]
    
    if clock_str == 'PM':
        if hour != 12:
            hour += 12

    if clock_str == 'AM':
        if hour == 12:
            hour = 0

    return datetime(year, month, day, hour, minute, 0, 0)
