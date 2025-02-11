import networkx as nx
import numpy as np

class AntColonyOptimization:
    def __init__(self, graph, num_ants, num_iterations, alpha=1.0, beta=2.0, evaporation_rate=0.5, pheromone_deposit=1.0):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit
        self.pheromone = {(u, v, k): 1.0 for u, v, k in graph.edges(keys=True)}

    def heuristic(self, u, v, key):
        return 1.0 / self.graph[u][v][key]['weight']

    def choose_next_node(self, current_node, visited):
        neighbors = [v for _, v, _ in self.graph.edges(current_node, keys=True) if v not in visited]
        if not neighbors:
            return None
        probabilities = []
        for neighbor in neighbors:
            # Get the key for the edge with the minimum weight (you can change this logic if needed)
            key = min(self.graph[current_node][neighbor], key=lambda x: self.graph[current_node][neighbor][x]['weight'])
            edge = (current_node, neighbor, key)
            pheromone = self.pheromone[edge] ** self.alpha
            heuristic = self.heuristic(current_node, neighbor, key) ** self.beta
            probabilities.append(pheromone * heuristic)
        probabilities = np.array(probabilities)
        if probabilities.sum() == 0:
            probabilities = np.ones_like(probabilities) / len(neighbors)  # Fallback to uniform distribution
        else:
            probabilities /= probabilities.sum()
        chosen_index = np.random.choice(len(neighbors), p=probabilities)
        return neighbors[chosen_index]

    def find_path(self, start_node, end_node):
        paths = []
        path_lengths = []
        for _ in range(self.num_ants):
            path = [start_node]  # Start with the start node
            visited = set([start_node])
            current_node = start_node
            while current_node != end_node:
                next_node = self.choose_next_node(current_node, visited)
                if next_node is None:
                    break
                path.append(next_node)
                visited.add(next_node)
                current_node = next_node
            if current_node == end_node:
                # Calculate path length
                path_length = 0
                for i in range(len(path) - 1):
                    u = path[i]
                    v = path[i + 1]
                    # Get the key for the edge with the minimum weight (you can change this logic if needed)
                    key = min(self.graph[u][v], key=lambda x: self.graph[u][v][x]['weight'])
                    path_length += self.graph[u][v][key]['weight']
                paths.append(path)
                path_lengths.append(path_length)
            else:
                path_lengths.append(float('inf'))  # Penalize dead-end paths
        return paths, path_lengths

    def update_pheromones(self, paths, path_lengths):
        for edge in self.pheromone:
            self.pheromone[edge] *= (1 - self.evaporation_rate)
        for path, length in zip(paths, path_lengths):
            if length == float('inf'):
                continue  # Skip dead-end paths
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                # Get the key for the edge with the minimum weight (you can change this logic if needed)
                key = min(self.graph[u][v], key=lambda x: self.graph[u][v][x]['weight'])
                self.pheromone[(u, v, key)] += self.pheromone_deposit / length

    def optimize(self, start_node, end_node):
        best_path = None
        best_length = float('inf')
        for iteration in range(self.num_iterations):
            paths, path_lengths = self.find_path(start_node, end_node)
            if paths:
                min_length = min(path_lengths)
                if min_length < best_length:
                    best_length = min_length
                    best_path = paths[path_lengths.index(min_length)]
            self.update_pheromones(paths, path_lengths)
        return best_path, best_length

def aco_find_best_path(graph, start_node, end_node):
    # Initialize the ACO algorithm
    aco = AntColonyOptimization(graph, num_ants=10, num_iterations=100)

    # Find the shortest path using ACO
    best_path, best_length = aco.optimize(start_node, end_node)
    print(f"Best path found by ACO: {best_path} with length {best_length}")

    return best_path, best_length