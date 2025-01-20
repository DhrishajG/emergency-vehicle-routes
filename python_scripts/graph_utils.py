import sumolib
import networkx as nx

def extract_graph(network_file):
    graph = nx.DiGraph()
    net = sumolib.net.readNet(network_file)

    for edge in net.getEdges():
        from_node = edge.getFromNode().getID()
        to_node = edge.getToNode().getID()
        weight = edge.getLength() / edge.getSpeed()
        graph.add_edge(from_node, to_node, weight=weight)

    return graph

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