import math
import networkx as nx
import traci
from graph_utils import extract_graph, get_edge_path

def euclidean_distance(node1, node2, pos):
    pos1 = pos[node1]
    pos2 = pos[node2]
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def real_time_traffic_heuristic(graph, pos, goal):
    def heuristic(node, goal=goal):
        edge_ids = [key for _, _, key in graph.edges(node, keys=True)]
        max_speed = max(traci.lane.getMaxSpeed(edge_id + "_0") for edge_id in edge_ids)
        euclidean_dist = euclidean_distance(node, goal, pos)
        congestion_penalty = sum(traci.edge.getLastStepOccupancy(edge_id) for edge_id in edge_ids)
        return euclidean_dist / max_speed + congestion_penalty
    return heuristic

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

    # Compute the shortest path using A* algorithm with the real-time traffic heuristic
    # heuristic = euclidean_distance(end_node, start_node, pos)  ## This is the default heuristic
    heuristic = real_time_traffic_heuristic(graph, pos, end_node)  ## This is the real-time traffic heuristic
    node_path = nx.astar_path(graph, start_node, end_node, heuristic=heuristic, weight='weight')

    print(f"Computed node path: {node_path}")

    # Convert the node path to an edge path
    edge_path = get_edge_path(graph, node_path)

    print(f"Computed edge path: {edge_path}")

    return edge_path