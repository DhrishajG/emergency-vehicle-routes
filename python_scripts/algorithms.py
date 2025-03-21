import math
import networkx as nx
import traci
from aco import AntColonyOptimization
from graph_utils import extract_graph, get_edge_path

def euclidean_distance(node1, node2, pos):
    pos1 = pos[node1]
    pos2 = pos[node2]
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def real_time_traffic_heuristic(graph, pos, goal):
    def avg_heuristic(node, goal=goal):
        edge_ids = [key for _, _, key in graph.edges(node, keys=True)]
        if not edge_ids:
            return float('inf')  # Avoid dead-end nodes
        
        congestion_penalties = [traci.edge.getLastStepOccupancy(edge_id) for edge_id in edge_ids]
        avg_congestion_penalty = sum(congestion_penalties) / len(congestion_penalties) if congestion_penalties else 0
        
        # Calculate the travel time based on real-time speed
        travel_times = [traci.lane.getLength(edge_id + "_0") / max(traci.edge.getLastStepMeanSpeed(edge_id), 0.1) for edge_id in edge_ids]
        avg_travel_time = sum(travel_times) / len(travel_times) if travel_times else float('inf')
        
        return avg_travel_time + avg_congestion_penalty
    return avg_heuristic

def real_time_traffic_pheromone_heuristic(graph, pos, goal):
    def heuristic(node, goal=goal):
        edge_ids = [key for _, _, key in graph.edges(node, keys=True)]
        
        if not edge_ids:
            return float('inf')  # Avoid dead-end nodes
        
         # Calculate congestion penalty for each edge individually
        congestion_penalties = [traci.edge.getLastStepOccupancy(edge_id) for edge_id in edge_ids]
        avg_congestion_penalty = sum(congestion_penalties) / len(congestion_penalties) if congestion_penalties else 0
        
        # Calculate the travel time based on real-time speed
        travel_times = [traci.lane.getLength(edge_id + "_0") / max(traci.edge.getLastStepMeanSpeed(edge_id), 0.1) for edge_id in edge_ids]
        avg_travel_time = sum(travel_times) / len(travel_times) if travel_times else float('inf')
        
        # Get pheromone values, default to 1.0 if not initialized
        pheromone_values = [graph[node][neighbor][edge_id].get('pheromone', 1.0) for _, neighbor, edge_id in graph.edges(node, keys=True)]
        avg_pheromone = sum(pheromone_values) / len(pheromone_values) if pheromone_values else 0

        weight = avg_travel_time + avg_congestion_penalty
        alpha = 2
        
        # Higher pheromones should reduce cost (preferred paths)
        return weight/(1 + alpha*avg_pheromone)
    
    return heuristic

def calculate_turn_penalty(prev_edge, current_edge):
    if prev_edge is None:
        return 0
    prev_edge_angle = traci.edge.getAngle(prev_edge)
    current_edge_angle = traci.edge.getAngle(current_edge)
    angle_diff = abs(current_edge_angle - prev_edge_angle)
    return angle_diff / 180  # Adjust the turn penalty based on the sharpness of the turn

def a_star(graph, pos, start_node, end_node):
    prev_edge = None

    def update_weights(u, v, d):
        nonlocal prev_edge
        current_edge = list(d.keys())[0] 
        weight = d[current_edge]['weight']
        turn_penalty = calculate_turn_penalty(prev_edge, current_edge)
        prev_edge = current_edge
        return weight + turn_penalty

    heuristic = real_time_traffic_heuristic(graph, pos, end_node)
    node_path = nx.astar_path(graph, start_node, end_node, heuristic=heuristic, weight=update_weights)

    print(f"Computed node path: {node_path}")

    edge_path = get_edge_path(graph, node_path)

    print(f"Computed edge path: {edge_path}")

    return edge_path

def a_star_traffic_pheromone(graph, pos, start_node, end_node):
    prev_edge = None

    def update_weights(u, v, d):
        nonlocal prev_edge
        current_edge = list(d.keys())[0]  # Get the edge key
        weight = d[current_edge]['weight']
        turn_penalty = calculate_turn_penalty(prev_edge, current_edge)
        prev_edge = current_edge
        return weight + turn_penalty


    heuristic = real_time_traffic_pheromone_heuristic(graph, pos, end_node)
    node_path = nx.astar_path(graph, start_node, end_node, heuristic=heuristic, weight=update_weights)

    print(f"Computed node path with pheromones: {node_path}")

    edge_path = get_edge_path(graph, node_path)
    print(f"Computed edge path with pheromones: {edge_path}")

    return edge_path


def a_star_euclidean(graph, pos, start_node, end_node):
    # Compute the shortest path using A* algorithm with euclidean distance
    heuristic = lambda u, v: euclidean_distance(u, v, pos)
    node_path = nx.astar_path(graph, start_node, end_node, heuristic=heuristic, weight='weight')

    print(f"Computed node path: {node_path}")

    # Convert the node path to an edge path
    edge_path = get_edge_path(graph, node_path)

    print(f"Computed edge path: {edge_path}")

    return edge_path

def djikstra(graph, start_node, end_node):
    # Compute the shortest path using Dijkstra's algorithm
    node_path = nx.dijkstra_path(graph, start_node, end_node)

    print(f"Computed node path: {node_path}")

    # Convert the node path to an edge path
    edge_path = get_edge_path(graph, node_path)

    print(f"Computed edge path: {edge_path}")

    return edge_path

def aco_shortest_path(graph, start_node, end_node, num_ants=30, beta=2.0, num_iterations=100):
    # Find the best path using ACO
    aco = AntColonyOptimization(graph, num_ants=num_ants, num_iterations=num_iterations, beta=beta)
    aco_path, aco_length = aco.optimize(start_node, end_node)
    # print(f"Best path: {aco_path}, Cost: {aco_length}")

    edge_path = get_edge_path(graph, aco_path)

    return edge_path