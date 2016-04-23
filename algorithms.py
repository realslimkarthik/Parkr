from time import time as time_fn
from datetime import datetime, timedelta
import googlemaps
from utility import get_nodes, get_edges, get_block_list, get_availability, get_node_from_block, \
    get_long_lat, get_block_availability, get_distance, get_distance_from_block_to_node, get_block_probability, \
    get_adjacent_nodes, reset_live_data, read_input_from_file, write_results_to_file


def deterministic_grav_pull(block_list, destination, time):
    block_grav_force = {}
    chosen_block = None
    chosen_node = None
    current_node = None
    max_force = 0
    for block in block_list:
        availability = get_block_availability(block, time)
        if availability != 0:
            node1, node2 = get_node_from_block(block)
            current_node, block_distance = get_distance_from_block_to_node(block, destination)
            block_grav_force[block] = availability / block_distance ** 2
        else:
            block_grav_force[block] = 0
        # print(block_grav_force[block])
        if max_force < block_grav_force[block]:
            max_force = block_grav_force[block]
            chosen_block = block
            chosen_node = current_node
    return chosen_block, chosen_node


def probabilistic_grav_pull(block_list, destination, time, fine_grained=True):
    block_grav_force = {}
    chosen_block = None
    chosen_node = None
    current_node = None
    max_force = 0
    for block in block_list:
        probability = get_block_probability(block, time, fine_grained)
        if probability != 0:
            node1, node2 = get_node_from_block(block)
            current_node, block_distance = get_distance_from_block_to_node(block, destination)
            block_grav_force[block] = probability / block_distance ** 2
        else:
            block_grav_force[block] = 0
        # print(block_grav_force[block])
        if max_force < block_grav_force[block]:
            max_force = block_grav_force[block]
            chosen_block = block
            chosen_node = current_node
    return chosen_block, chosen_node


def uninformed_search(origin, destination, worst_case=False):
    distance = get_distance(origin, destination)
    extra_distance = 0
    adjacent_nodes = get_adjacent_nodes(destination)
    for node in adjacent_nodes:
        extra_distance += get_distance(destination, node)

    if not worst_case:
        extra_distance /= 2
    return distance + extra_distance


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
    dir_result_legs = dir_result[0].get("legs",None)
    #there should be only one since there are no waypoints sent in the request
    if len(dir_result_legs) > 0:
        dir_result_a_leg = dir_result_legs[0]
        dir_list = dir_result_a_leg.get("steps",None)

    return dir_list
 

def get_parking_spot(destination, time, algorithm):
    block_list = get_block_list()
    if algorithm == 'd':
        chosen_block, chosen_node = deterministic_grav_pull(block_list, destination, time)
    elif algorithm.startswith('p'):
        if algorithm == 'p'
            chosen_block, chosen_node = probabilistic_grav_pull(block_list, destination, time)
        else:
            chosen_block, chosen_node = probabilistic_grav_pull(block_list, destination, time, fine_grained=False)
    else:
        print('algorithm should be d for deterministic_grav_pull or p for probabilistic_grav_pull')
        chosen_block = -1
    
    return chosen_block, chosen_node


def get_directions(origin, destination, time):
    if isinstance(origin, list):
        origin_long_lat = origin
    else:
        origin_long_lat = get_long_lat(origin)
    
    if isinstance(destination, list):
        destination_long_lat = destination
    else:
        destination_long_lat = get_long_lat(destination)
    
    directions = get_turn_by_turn_directions(origin_long_lat, destination_long_lat, time)
    return directions


def check_sample(seed):
    i = 1
    while True:
        try:
            sample_value = i / seed
        except ZeroDivisionError:
            sample_value = 1.1
        if sample_value == int(sample_value):
            yield True
        else:
            yield False


def route_vehicle(origin, destination, time, algorithm, sampling_rate):
    chosen_block = {}
    chosen_block['block_id'], chosen_block['node_id'] = get_parking_spot(destination, time, algorithm)
    if not chosen_block.get('block_id'):
        return None
    directions = get_directions(origin, chosen_block['node_id'], time)
    sampler = check_sample(sampling_rate)
    distance = 0
    step_index = 0
    current_location = None
    routing_data = {}
    routing_data['success'] = True
    routing_data['points'] = [get_long_lat(origin)]


    while True:
        step = directions[step_index]
        distance += step['distance']['value']
        seconds = step['duration']['value']
        time = time + timedelta(seconds=seconds)
        if next(sampler):
            block_availability = get_block_availability(chosen_block['block_id'], time)
            if block_availability == 0:
                chosen_block['block_id'], chosen_block['node_id'] = get_parking_spot(destination, time, algorithm)
                
                if chosen_block['block_id'] == -1:
                    distance = -1
                    break
                intermediate_point = [float(step['end_location']['lng']), float(step['end_location']['lat'])]
                current_location = intermediate_point
                routing_data['points'].append(intermediate_point)
                new_node1, new_node2 = get_node_from_block(chosen_block['block_id'])
                if get_distance(origin, new_node1) < get_distance(origin, new_node2):
                    chosen_block['node_id'] = new_node1
                else:
                    chosen_block['node_id'] = new_node2
                directions == get_directions(current_location, chosen_block['node_id'], time)
                step_index = 0

        step_index += 1
        if step_index == len(directions):
            _, walking_distance = get_distance_from_block_to_node(chosen_block['block_id'], destination)
            break

    block_availability = get_block_availability(chosen_block['block_id'], time)
    if block_availability == 0:
        routing_data['success'] = False
        walking_distance = None
    current_location = [float(step['end_location']['lng']), float(step['end_location']['lat'])]
    routing_data['walking_distance'] = walking_distance
    routing_data['time'] = time
    routing_data['distance'] = distance
    routing_data['current_location'] = current_location
    
    return routing_data


def simulate(origin, destination, time, algorithm, sampling_rate):
    route_result = {'distance': 0, 'success': False, 'current_location': origin, 'time': time, 'points': []}
    while not route_result['success']:
        time1 = time_fn()
        new_result = route_vehicle(route_result['current_location'], destination, route_result['time'], algorithm, sampling_rate)
        time2 = time_fn()
        running_time = time2 - time1
        if new_result is None:
            route_result['distance'] = 'NA'
            route_result['success'] = 'NA'
            route_result['current_location'] = None
            route_result['time'] = None
            route_result['points'] = None
            route_result['walking_distance'] = 'NA'
        elif new_result['success']:
            route_result['distance'] += new_result['distance']
            route_result['walking_distance'] = new_result['walking_distance']
            route_result['success'] = new_result['success']
            route_result['current_location'] = new_result['current_location']
            route_result['time'] = new_result['time']
            route_result['points'].extend(new_result['points'])
            route_result['points'].append(new_result['current_location'])
        route_result['running_time'] = running_time
        print(route_result['running_time'])
        print(route_result['walking_distance'])

    return route_result


def run_simulation(input_file, algorithm, sampling_rate, congestion, output_file_name):
    reset_live_data(congestion)
    input_data = read_input_from_file(input_file)
    output_data = []

    for i in input_data:
        result = simulate(i['origin'], i['destination'], i['time'], algorithm, sampling_rate)
        uninformed_search_distance = uninformed_search(i['origin'], i['destination'])
        result['uninformed_search_distance'] = uninformed_search_distance
        print(result['uninformed_search_distance'])
        output_data.append(result)

    fieldnames = output_data[0].keys()
    write_results_to_file(output_data, fieldnames, output_file_name)
    return output_data


