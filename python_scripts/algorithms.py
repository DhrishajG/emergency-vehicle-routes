import math
import networkx as nx
from graph_utils import extract_graph, get_edge_path

def euclidean_distance(node1, node2, pos):
    pos1 = pos[node1]
    pos2 = pos[node2]
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def djikstra(network_file, start_node, end_node):
    # Extract the graph from the network file
    graph, _ = extract_graph(network_file)
            
    # Compute the shortest path using Dijkstra's algorithm
    node_path = nx.dijkstra_path(graph, start_node, end_node)

    print(f"Computed node path: {node_path}")

    # Convert the node path to an edge path
    edge_path = get_edge_path(graph, node_path)

    print(f"Computed edge path: {edge_path}")

    return edge_path

def a_star(network_file, start_node, end_node):
    # Extract the graph from the network file
    graph, pos = extract_graph(network_file)

    # Compute the shortest path using A* algorithm with the Euclidean distance heuristic
    heuristic = lambda u, v: euclidean_distance(u, v, pos)
    node_path = nx.astar_path(graph, start_node, end_node, heuristic=heuristic, weight='weight')

    print(f"Computed node path: {node_path}")

    # Convert the node path to an edge path
    edge_path = get_edge_path(graph, node_path)

    print(f"Computed edge path: {edge_path}")

    return edge_path