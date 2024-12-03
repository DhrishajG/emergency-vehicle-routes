import sumolib

def extract_graph(network_file):
    # Load the SUMO network
    net = sumolib.net.readNet(network_file)
    graph = {}

    # Extract nodes and edges
    for edge in net.getEdges():
        start_node = edge.getFromNode()
        end_node = edge.getToNode()
        length = edge.getLength()  # This could be used as the edge weight

        if start_node.getID() not in graph:
            graph[start_node.getID()] = []
        if end_node.getID() not in graph:
            graph[end_node.getID()] = []

        graph[start_node.getID()].append((end_node.getID(), length))
        graph[end_node.getID()].append((start_node.getID(), length))

    return graph
