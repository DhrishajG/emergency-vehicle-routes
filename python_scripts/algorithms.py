import networkx as nx
from graph_utils import extract_graph, get_edge_path

def djikstra(network_file, start_node, end_node):
    # Extract the graph from the network file
    graph = extract_graph(network_file)
            
    # Compute the shortest path using Dijkstra's algorithm
    node_path = nx.dijkstra_path(graph, start_node, end_node)

    # Convert the node path to an edge path    
    edge_path = get_edge_path(graph, node_path)

    return edge_path