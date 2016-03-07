from datetime import datetime
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
    block = edges_df[edges_df['block_id'] == block_id].loc[0]
    node1 = block.node_id_1
    node2 = block.node_id_2
    return node1, node2


def deterministic_grav_pull(block_list, origin, time):
    num_available_blocks = 0
    node_distances = {}
    node_availability = {}
    block_grav_force = {}
    chosen_block = None
    max_force = 0
    for block in block_list:
        node1, node2 = get_node_from_block(block)
        
        #block_distance = min(googlemaps.road_distance(origin, node1),
        #    googlemaps.road_distance(origin, node2))

        block_distance = min(get_distance(origin,node1), get_distance(origin,node2))

        availability = get_block_availability(block, time)
        block_grav_force[block] = availability / block_distance ** 2
        if max_force < block_grav_force[block]:
            max_force = block_grav_force[block]
            chosen_block = block

    return chosen_block, block_grav_force

# TODO handle exceptions
def get_distance(origin, destination):
    
    dist_text = "";
    dist_value = 0; #in meters

    gmaps = googlemaps.Client(key="AIzaSyDPxsz5WxM_rqmM6ROL97Gthf48qEk5rs0")
    
    # ex: gmaps.distance_matrix(["37.808322,-122.419212"], ["37.808436,-122.414186"])
    dm_result = gmaps.distance_matrix(get_lat_long(origin),get_lat_long(destination))
    dm_rows = ds_result.get("rows",None)

    for a_dm_row in dm_rows:
        elem_list = a_dm_row.get("elements",None)
        #there should be only one elem since only one origin and destination is passed
        for an_elem in elem_list
            dist_text = an_elem.get("distance").get("text")
            dist_value = an_elem.get("distance").get("value")
            break            
            
    return dist_text, dist_value

def get_lat_long(location):
    pass

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
def get_turn_by_turn_directions(origin, destination):
    
    dir_list = [];
    gmaps = googlemaps.Client(key="AIzaSyDPxsz5WxM_rqmM6ROL97Gthf48qEk5rs0")

    dir_result = gmaps.directions(get_lat_long(origin),get_lat_long(destination), 
        mode = "driving", departure_time = datetime.now())
    dir_result_legs = dir_result.get("legs",None)

    #there should be only one since there are no waypoints sent in the request
    if len(dir_result_legs) > 0:
        dir_result_a_leg = dir_result_legs[0]
        dir_list = dir_result_a_leg.get("steps",None)

    return dir_list    


def route_vehicle(origin, destination, time):
    pass

