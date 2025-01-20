import heapq

def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    predecessors = {}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances[end], predecessors

def a_star(graph, start, end, heuristic):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    predecessors = {}
    estimated_costs = {node: float('inf') for node in graph.nodes}
    estimated_costs[start] = heuristic(start, end)

    while queue:
        current_cost, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = distances[current_node] + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                estimated_cost = distance + heuristic(neighbor, end)
                estimated_costs[neighbor] = estimated_cost
                heapq.heappush(queue, (estimated_cost, neighbor))

    return distances[end], predecessors

def heuristic(node, end):
    # Implement your heuristic function here
    return 0