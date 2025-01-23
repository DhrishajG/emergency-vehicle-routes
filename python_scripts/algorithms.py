import heapq

def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {edge: float('inf') for edge in graph.edges(keys=True)}
    distances[start] = 0
    predecessors = {}

    while queue:
        current_distance, current_edge = heapq.heappop(queue)
        print(f"Visiting edge: {current_edge} with current distance: {current_distance}")

        if current_edge == end:
            break

        for _, neighbor, key in graph.edges(current_edge[1], keys=True):
            weight = graph[current_edge[1]][neighbor][key]['weight']
            distance = current_distance + weight
            print(f"Checking neighbor edge: ({current_edge[1]}, {neighbor}, {key}) with weight: {weight} and distance: {distance}")

            if distance < distances[(current_edge[1], neighbor, key)]:
                distances[(current_edge[1], neighbor, key)] = distance
                predecessors[(current_edge[1], neighbor, key)] = current_edge
                heapq.heappush(queue, (distance, (current_edge[1], neighbor, key)))
                print(f"Updated distance for edge: ({current_edge[1]}, {neighbor}, {key}) to: {distance}")

    return distances[end], predecessors

def a_star(graph, start, end, heuristic):
    queue = [(0, start)]
    distances = {edge: float('inf') for edge in graph.edges(keys=True)}
    distances[start] = 0
    predecessors = {}
    estimated_costs = {edge: float('inf') for edge in graph.edges(keys=True)}
    estimated_costs[start] = heuristic(start, end)

    while queue:
        current_cost, current_edge = heapq.heappop(queue)
        print(f"Visiting edge: {current_edge} with current cost: {current_cost}")

        if current_edge == end:
            break

        for _, neighbor, key in graph.edges(current_edge[1], keys=True):
            weight = graph[current_edge[1]][neighbor][key]['weight']
            distance = distances[current_edge] + weight
            print(f"Checking neighbor edge: ({current_edge[1]}, {neighbor}, {key}) with weight: {weight} and distance: {distance}")

            if distance < distances[(current_edge[1], neighbor, key)]:
                distances[(current_edge[1], neighbor, key)] = distance
                predecessors[(current_edge[1], neighbor, key)] = current_edge
                estimated_cost = distance + heuristic((current_edge[1], neighbor, key), end)
                estimated_costs[(current_edge[1], neighbor, key)] = estimated_cost
                heapq.heappush(queue, (estimated_cost, (current_edge[1], neighbor, key)))
                print(f"Updated distance for edge: ({current_edge[1]}, {neighbor}, {key}) to: {distance}")

    print(f"Final distances: {distances}")
    print(f"Predecessors: {predecessors}")
    return distances[end], predecessors

def heuristic(edge, end):
    # Implement your heuristic function here
    return 0