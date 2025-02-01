import math
import networkx as nx
import traci
from graph_utils import extract_graph, get_edge_path

def euclidean_distance(node1, node2, pos):
    # For A* algorithm, we need a heuristic function that estimates the cost of the cheapest path from the current node to the goal node
    pos1 = pos[node1]
    pos2 = pos[node2]
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def real_time_traffic_heuristic(graph, pos, goal):
    # For A* algorithm, we need a heuristic function that estimates the cost of the cheapest path from the current node to the goal node
    def avg_heuristic(node, goal=goal):
        # Calculate the average heuristic value for all edges connected to the current node
        edge_ids = [key for _, _, key in graph.edges(node, keys=True)]
        max_speed = max(traci.lane.getMaxSpeed(edge_id + "_0") for edge_id in edge_ids)
        euclidean_dist = euclidean_distance(node, goal, pos)
        
        # Calculate congestion penalty for each edge individually
        congestion_penalties = [traci.edge.getLastStepOccupancy(edge_id) for edge_id in edge_ids]
        
        # Calculate the average congestion penalty
        avg_congestion_penalty = sum(congestion_penalties) / len(congestion_penalties) if congestion_penalties else 0
        
        return euclidean_dist / max_speed + avg_congestion_penalty
    
    def minimum_heuristic(node, goal=goal):
        # Calculate the minimum heuristic value for all edges connected to the current node
        edge_ids = [key for _, _, key in graph.edges(node, keys=True)]
        min_heuristic = float('inf')
        
        for edge_id in edge_ids:
            max_speed = traci.lane.getMaxSpeed(edge_id + "_0")
            euclidean_dist = euclidean_distance(node, goal, pos)
            congestion_penalty = traci.edge.getLastStepOccupancy(edge_id)
            
            heuristic_value = euclidean_dist / max_speed + congestion_penalty
            if heuristic_value < min_heuristic:
                min_heuristic = heuristic_value
        
        return min_heuristic
    return avg_heuristic

def calculate_turn_penalty(prev_edge, current_edge):
    # Calculate the turn penalty based on the angle difference between the previous edge and the current edge
    if prev_edge is None:
        return 0
    prev_edge_angle = traci.edge.getAngle(prev_edge)
    current_edge_angle = traci.edge.getAngle(current_edge)
    angle_diff = abs(current_edge_angle - prev_edge_angle)
    return angle_diff / 180  # Adjust the turn penalty based on the sharpness of the turn

def a_star(network_file, start_node, end_node):
    # Extract the graph from the network file
    graph, pos = extract_graph(network_file)

    # Initialize the previous edge
    prev_edge = None

    def update_weights(u, v, d):
        # Update the edge weights with the real-time traffic information and turn penalty
        nonlocal prev_edge
        current_edge = list(d.keys())[0]  # Get the edge key
        weight = d[current_edge]['weight']
        turn_penalty = calculate_turn_penalty(prev_edge, current_edge)
        prev_edge = current_edge
        return weight + turn_penalty

    # Compute the shortest path using A* algorithm with the real-time traffic heuristic and custom edge weight
    heuristic = real_time_traffic_heuristic(graph, pos, end_node)
    node_path = nx.astar_path(graph, start_node, end_node, heuristic=heuristic, weight=update_weights)

    print(f"Computed node path: {node_path}")

    # Convert the node path to an edge path
    edge_path = get_edge_path(graph, node_path)

    print(f"Computed edge path: {edge_path}")

    return edge_path

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