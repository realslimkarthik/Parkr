import pandas
import googlemaps
from utility import get_nodes
from algorithms import get_distance, get_long_lat


def main():
    gmaps = googlemaps.Client(key="AIzaSyDPxsz5WxM_rqmM6ROL97Gthf48qEk5rs0")
    nodes_df = get_nodes()
    nodes = nodes_df['node_id']
    distances = []

    for node1 in nodes:
        print(node1)
        for node2 in nodes:
            dist_object = {}
            if node1 == node2:
                continue
            dist_object['node_id_1'] = node1
            dist_object['node_id_2'] = node2
            node1_long_lat = get_long_lat(node1)
            node2_long_lat = get_long_lat(node2)
            _, dist_object['distance'] = get_distance([node1_long_lat], [node2_long_lat])
            distances.append(dist_object)

    df = pandas.DataFrame(distances)
    df.to_csv('./data/NodesDishermansWharf_Distances.csv')



if __name__ == '__main__':
    main()