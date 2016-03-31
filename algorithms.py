from datetime import datetime, timedelta
import googlemaps
from utility import get_nodes, get_edges, get_availability


def get_nodes_within_radius(dest, radius):
    pass


def get_block_availability(block_id, time):
    availability_df  = get_availability()
    block_availability_df = availability_df[availability_df['block_id'] == block_id]
    block_availability_timed_df = block_availability_df[block_availability_df['timestamp'] == time]
    if block_availability_timed_df.empty:
        block_availability_timed_df = block_availability_df[block_availability_df['timestamp'] < time]
        last_block = block_availability_timed_df.max()
    return last_block


def get_node_from_block(block_id):
    edges_df = get_edges()
    block = edges_df[edges_df['node_id'] == block_id].loc[0]
    node1 = block.node_id_1
    node2 = block.node_id_2
    return node1, node2


def get_node_id_from_long_lat(longitude, latitude):
    nodes_df = get_nodes()
    long_df = nodes_df[nodes_df['longitude'] == longitude & nodes_df['latitude'] == latitude]
    long_lat_node = long_df.loc[0]
    node_id = long_lat_node.block_id
    return node_id


def deterministic_grav_pull(block_list, origin, time):
    num_available_blocks = 0
    node_distances = {}
    node_availability = {}
    block_grav_force = {}
    chosen_block = None
    max_force = 0
    for block in block_list:
        node1, node2 = get_node_from_block(block)
        block_distance = min(get_distance(origin,node1), get_distance(origin,node2))
        availability = get_block_availability(block, time)
        block_grav_force[block] = availability / block_distance ** 2
        if max_force < block_grav_force[block]:
            max_force = block_grav_force[block]
            chosen_block = block

    return chosen_block


def get_distance(origin, destination):
    
    dist_text = ""
    dist_value = 0 #in meters

    gmaps = googlemaps.Client(key="AIzaSyDPxsz5WxM_rqmM6ROL97Gthf48qEk5rs0")
    
    # ex: gmaps.distance_matrix(["37.808322,-122.419212"], ["37.808436,-122.414186"])
    dm_result = gmaps.distance_matrix(origin,destination)
    dm_rows = dm_result.get("rows",None)

    for a_dm_row in dm_rows:
        elem_list = a_dm_row.get("elements",None)
        # there should be only one elem since only one origin and destination is passed
        dist_text = elem_list[0].get("distance").get("text")
        dist_value = elem_list[0].get("distance").get("value")
            
    return dist_text, dist_value


def get_long_lat(node_id):
    nodes_df = get_nodes()
    row = nodes_df[nodes_df['node_id'] == node_id]
    # row = nodes_df[nodes_df['node_id'] == node_id].head(n=1)
    longitude = row.longitude
    latitude = row.latitude
    long_lat = [float(longitude), float(latitude)]
    # long_lat = ['%.6f,%.6f' % (longitude, latitude)]
    return long_lat


def probabilistic_grav_pull(node_list):
    pass

def uninformed_search():
    pass


#
# Returned list would be of this form, need to extract and return only what is required once we decide
# 
# Same could be used for route_vehicle as well
#  
# [{'start_location': {'lng': -122.4192051, 'lat': 37.8083187}, 
#   'end_location': {'lng': -122.4191022, 'lat': 37.8078146}, 
#   'polyline': {'points': '_mweF`_ejVdBU'}, 
#   'html_instructions': 'Head <b>south</b> on <b>Leavenworth St</b> toward <b>Jefferson St</b>', 
#   'travel_mode': 'DRIVING', 
#   'distance': {'text': '187 ft', 'value': 57}, 
#   'duration': {'text': '1 min', 'value': 20}}, 
#  {'start_location': {'lng': -122.4191022, 'lat': 37.8078146}, 
#   'end_location': {'lng': -122.4141848, 'lat': 37.8084429}, 
#   'maneuver': 'turn-left', 
#   'html_instructions': 'Turn <b>left</b> at the 1st cross street onto <b>Jefferson St</b>', 
#   'travel_mode': 'DRIVING', 
#   'distance': {'text': '0.3 mi', 'value': 438}, 
#   'polyline': {'points': 'yiweFj~djVU{COsBEy@AMe@{GA]CWQoCQ}C'}, 
#   'duration': {'text': '3 mins', 'value': 157}}]
#


def get_turn_by_turn_directions(origin, destination, departure_time):
    
    dir_list = [];
    gmaps = googlemaps.Client(key="AIzaSyDPxsz5WxM_rqmM6ROL97Gthf48qEk5rs0")

    dir_result = gmaps.directions(origin, destination,
        mode="driving", departure_time=datetime.now())
    # dir_result = gmaps.directions(origin, destination,
    #     mode="driving", departure_time=departure_time)
    dir_result_legs = dir_result[0].get("legs",None)
    #there should be only one since there are no waypoints sent in the request
    if len(dir_result_legs) > 0:
        dir_result_a_leg = dir_result_legs[0]
        dir_list = dir_result_a_leg.get("steps",None)

    return dir_list
 

def get_parking_spot(origin, destination, time, radius):
    block_list = get_nodes()
    if algorithm == 'd':
        chosen_block = deterministic_grav_pull(block_list, origin, time)
    # elif algorithm == 'p':
    #     chosen_block = probabilistic_grav_pull(block_list, origin, time)
    else:
        print('algorithm should be d for deterministic_grav_pull or p for probabilistic_grav_pull')
        chosen_block = -1
    
    return chosen_block


def route_vehicle(origin, destination, time):
    origin_long_lat = get_long_lat(origin)
    destination_long_lat = get_long_lat(destination)
    directions = get_turn_by_turn_directions(origin_long_lat, destination_long_lat, time)

    distance = 0
    
    for step in directions:
        seconds = step['duration']['value']
        time = time + timedelta(seconds=seconds)
        block_availability = get_block_availability(chosen_block['block_id'], time)
        if block_availability.available == 0:
            chosen_block['block_id'] = get_parking_spot(origin, destination, time)
            
            if chosen_block['block_id'] == -1:
                print('No available parking spots')
                distance = -1
                break
            else:
                step_node = get_node_id_from_long_lat(step['end_location']['lng'],
                    step['end_location']['lat'])
                node1, node2 = get_node_from_block(chosen_block['block_id'])
                node1_long_lat = get_long_lat(node1)
                node2_long_lat = get_long_lat(node2)

                if get_distance(origin_long_lat, node1_long_lat) < get_distance(origin_long_lat, node2_long_lat):
                    chosen_block['node_id'] = node1
                else:
                    chosen_block['node_id'] = node2
                new_distance = route_vehicle(step_node, chosen_block['node_id'], time)
                if new_distance != -1:
                    distance += new_distance
                    break
        distance += step['distance']['value']

    return distance


def simulate(origin, destination, time, algorithm):
    chosen_block = {}
    radius = 100
    chosen_block['block_id'] = None
    origin_long_lat = get_long_lat(origin)
    destination_long_lat = get_long_lat(destination)

    origin_dest_distance = get_distance(origin_long_lat, destination_long_lat)
    
    while chosen_block['block_id'] is None:
        chosen_block['block_id'] = get_parking_spot(origin, destination, time, radius)
        if radius > origin_dest_distance:
            break
        radius += 50
    
    node1, node2 = get_node_from_block(chosen_block['block_id'])
    node1_long_lat = get_long_lat(node1)
    node2_long_lat = get_long_lat(node2)

    if get_distance(origin_long_lat, node1_long_lat) < get_distance(origin_long_lat, node2_long_lat):
        chosen_block['node_id'] = node1
    else:
        chosen_block['node_id'] = node2

    distance = route_vehicle(origin, chosen_block['node_id'], time)

    return distance


def simulate(origin, destination, time):
    chosen_block = {}
    chosen_block['block_id'] = None
    origin_long_lat = get_long_lat(origin)
    destination_long_lat = get_long_lat(destination)

    origin_dest_distance = get_distance(origin_long_lat, destination_long_lat)
    
    chosen_block['block_id'] = get_parking_spot(origin, destination, time)
    
    node1, node2 = get_node_from_block(chosen_block['block_id'])
    node1_long_lat = get_long_lat(node1)
    node2_long_lat = get_long_lat(node2)

    if get_distance(origin_long_lat, node1_long_lat) < get_distance(origin_long_lat, node2_long_lat):
        chosen_block['node_id'] = node1
    else:
        chosen_block['node_id'] = node2

    distance = route_vehicle(origin, chosen_block['node_id'], time)

    return distance