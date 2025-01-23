import sumolib
import networkx as nx

def extract_graph(network_file):
    graph = nx.MultiDiGraph()
    net = sumolib.net.readNet(network_file)

    for edge in net.getEdges():
        # Exclude footpaths and other non-vehicle edges
        if edge.allows("passenger"):
            edge_id = edge.getID()
            from_node = edge.getFromNode().getID()
            to_node = edge.getToNode().getID()
            weight = edge.getLength() / edge.getSpeed()
        
            graph.add_edge(from_node, to_node, key=edge_id, weight=weight)

    return graph

def get_edge_path(graph, node_path):
    # Convert the node path to an edge path
    edge_path = []
    for i in range(len(node_path) - 1):
        for _, v, key in graph.edges(node_path[i], keys=True):
            if v == node_path[i + 1]:
                edge_path.append(key)
                break
    return edge_path
    

def reconstruct_path(predecessors, start, end):
    if start == end:
        return [start]
    if start not in predecessors or end not in predecessors:
        raise ValueError("Start or end node not in predecessors, path cannot be reconstructed.")
    
    path = []
    current = end
    while current != start:
        if current not in predecessors:
            raise ValueError(f"Node {current} not in predecessors, path cannot be reconstructed.")
        path.append(current)
        current = predecessors[current]
    path.append(start)
    path.reverse()
    return path