import sumolib
import traci
import networkx as nx
import matplotlib.pyplot as plt

def extract_graph(network_file):
    graph = nx.MultiDiGraph()
    net = sumolib.net.readNet(network_file)

    pos = {}
    for node in net.getNodes():
        pos[node.getID()] = (node.getCoord()[0], node.getCoord()[1])

    edge_labels = {}
    for edge in net.getEdges():
        # Exclude footpaths and other non-allowed edges
        if edge.allows("emergency"):
            edge_id = edge.getID()
            from_node = edge.getFromNode().getID()
            to_node = edge.getToNode().getID()
            weight = edge.getLength() / edge.getSpeed()
        
            if traci.edge.getLaneNumber(edge_id) == 1:
                weight *= 1.3  # Narrow road penalty

            graph.add_edge(from_node, to_node, key=edge_id, weight=weight)
            edge_labels[(from_node, to_node)] = f"{weight:.2f}"
    
    # Draw the graph representation of the road network
    draw_graph = input("Do you want to draw the graph? (y/n): ")
    if draw_graph.lower() == "y":
        nx.draw(graph, pos, with_labels=False, node_size=50)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
        plt.show()
    return graph, pos

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