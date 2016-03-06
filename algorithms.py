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
        block_distance = min(googlemaps.road_distance(origin, node1),
            googlemaps.road_distance(origin, node2))
        availability = get_block_availability(block, time)
        block_grav_force[block] = availability / block_distance ** 2
        if max_force < block_grav_force[block]:
            max_force = block_grav_force[block]
            chosen_block = block

    return chosen_block, block_grav_force


def probabilistic_grav_pull(node_list):
    pass


def uninformed_search():
    pass


def get_turn_by_turn_directions(origin, destination):
    pass


def route_vehicle(origin, destination, time):

    pass

