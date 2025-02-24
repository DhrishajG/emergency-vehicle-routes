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

        # Initialize pheromone values on the graph
        # for u, v, k in self.graph.edges(keys=True):
        #     self.graph[u][v][k]['pheromone'] = 1.0

    def heuristic(self, u, v, key):
        """Heuristic function: inverse of edge weight (travel time)."""
        return 1.0 / self.graph[u][v][key]['weight']

    def choose_next_node(self, current_node, visited):
        """Choose the next node for an ant based on pheromone and heuristic information."""
        neighbors = [v for _, v, _ in self.graph.edges(current_node, keys=True) if v not in visited]
        if not neighbors:
            return None  # Dead end

        probabilities = []
        for neighbor in neighbors:
            # Get the key for the edge with the minimum weight
            try:
                key = min(self.graph[current_node][neighbor], key=lambda x: self.graph[current_node][neighbor][x]['weight'])
                edge = (current_node, neighbor, key)
                pheromone = self.graph[current_node][neighbor][key]['pheromone'] ** self.alpha
                heuristic = self.heuristic(current_node, neighbor, key) ** self.beta
                probabilities.append(pheromone * heuristic)
            except KeyError as e:
                continue

        if not probabilities:
            return None  # Dead end

        probabilities = np.array(probabilities)
        if probabilities.sum() == 0:
            probabilities = np.ones_like(probabilities) / len(neighbors)  # Fallback to uniform distribution
        else:
            probabilities /= probabilities.sum()

        chosen_index = np.random.choice(len(neighbors), p=probabilities)
        chosen_node = neighbors[chosen_index]
        return chosen_node

    def find_path(self, start_node, end_node):
        """Find paths for all ants from start_node to end_node."""
        paths = []
        path_lengths = []
        for ant in range(self.num_ants):
            path = [start_node]
            visited = set([start_node])
            current_node = start_node
            while current_node != end_node:
                next_node = self.choose_next_node(current_node, visited)
                if next_node is None:
                    break
                # Check if the edge exists in the graph
                if next_node not in self.graph[current_node]:
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
                    try:
                        key = min(self.graph[u][v], key=lambda x: self.graph[u][v][x]['weight'])
                        path_length += self.graph[u][v][key]['weight']
                    except KeyError as e:
                        path_length = float('inf')
                        break
                paths.append(path)
                path_lengths.append(path_length)
            else:
                paths.append([])
                path_lengths.append(float('inf'))  # Penalize dead-end paths
        return paths, path_lengths

    def update_pheromones(self, paths, path_lengths):
        """Update pheromone levels on edges based on ant paths."""

        # Evaporate pheromones on all edges
        for u, v, k in self.graph.edges(keys=True):
            self.graph[u][v][k]['pheromone'] *= (1 - self.evaporation_rate)
            if self.graph[u][v][k]['pheromone'] <= 0:
                self.graph[u][v][k]['pheromone'] = 1e-10  # Reset to a small positive value

        # Update pheromones for valid paths
        for path, length in zip(paths, path_lengths):
            # Skip dead-end paths or paths with fewer than two nodes
            if length == float('inf') or len(path) < 2:
                continue

            # Update pheromones for each edge in the path
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
        
                # Get the key for the edge with the minimum weight
                try:
                    key = min(self.graph[u][v], key=lambda x: self.graph[u][v][x]['weight'])
                    self.graph[u][v][key]['pheromone'] += self.pheromone_deposit / length
                    if self.graph[u][v][key]['pheromone'] <= 0:
                        self.graph[u][v][key]['pheromone'] = 1e-10  # Reset to a small positive value
                except KeyError as e:
                    continue

    def validate_graph(self):
        """Validate the graph to ensure all edges have a 'weight' attribute."""
        for u, v, key in self.graph.edges(keys=True):
            if 'weight' not in self.graph[u][v][key]:
                print(f"Error: Edge ({u}, {v}, {key}) is missing 'weight' attribute.")

    def optimize(self, start_node, end_node):
        """Run the ACO algorithm to find the best path from start_node to end_node."""
        self.validate_graph()  # Validate the graph before starting
        best_path = None
        best_length = float('inf')
        for iteration in range(self.num_iterations):
            paths, path_lengths = self.find_path(start_node, end_node)

            if len(paths) > 0:  # Only proceed if paths are found

                # Filter out invalid paths (those with infinite length)
                valid_paths = [path for path, length in zip(paths, path_lengths) if length != float('inf')]
                valid_lengths = [length for length in path_lengths if length != float('inf')]

                if valid_lengths:  # Check if there are any valid paths
                    min_length = min(valid_lengths)
                    if min_length < best_length:
                        best_length = min_length
                        best_path = valid_paths[valid_lengths.index(min_length)]
                else:
                    print("No valid paths found in this iteration.")
            else:
                print("No valid paths found in this iteration.")

            self.update_pheromones(paths, path_lengths)

        return best_path, best_length