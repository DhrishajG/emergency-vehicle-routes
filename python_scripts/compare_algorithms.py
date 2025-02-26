import traci
import csv
import psutil
import time
from algorithms import a_star, djikstra, aco_shortest_path, a_star_euclidean, a_star_traffic_pheromone
from constants import ConfigFile, NetworkFile, AmbulanceRoutes
from ambulance_simulation import add_ambulance, end_simulation, track_ambulance
from graph_utils import extract_graph

CONFIG_FILE = ConfigFile.more_kyoto.value
NETWORK_FILE = NetworkFile.more_kyoto.value
AMBULANCES = AmbulanceRoutes.more_kyoto.value
CSV_FILE = "../outputs/algorithm_comparison_results.csv"

def run_algorithm(algorithm, algorithm_name, graph, pos):
    results = []
    ambulance_index = 0
    total_ambulances = len(AMBULANCES)
    continueACO = True

    aco_time_overhead = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if traci.simulation.getTime() % 100 == 0 and algorithm == a_star_traffic_pheromone and continueACO:
            aco_time_start = time.time()
            old_graph = graph
            print("Copied old graph")
            graph, pos = extract_graph(NETWORK_FILE, old_graph=old_graph)
            print("Extracted new graph")
            _ = aco_shortest_path(graph, start_node, end_node, num_ants=100)
            print("Ran ACO")
            aco_time_end = time.time()
            aco_time_overhead += (aco_time_end - aco_time_start)
        if traci.simulation.getTime() % 500 == 0 and ambulance_index < total_ambulances:
            ambulance_id, start_node, end_node = AMBULANCES[ambulance_index]
            if ambulance_id == AMBULANCES[-1][0]:
                continueACO = False
            start_time = time.time()

            if algorithm_name == "Dijkstra":
                edge_path = djikstra(graph, start_node, end_node)
            elif algorithm_name == "A*":
                edge_path = a_star(graph, pos, start_node, end_node)
            elif algorithm_name == "A* Euclidean":
                edge_path = a_star_euclidean(graph, pos, start_node, end_node)
            elif algorithm_name == "A* ACO":
                edge_path = a_star_traffic_pheromone(graph, pos, start_node, end_node)
            else:
                raise ValueError(f"Unknown algorithm: {algorithm_name}")

            end_time = time.time()

            computation_time = end_time - start_time

            end_edge = edge_path[-1]
            ambulance_start_time = traci.simulation.getTime()
            add_ambulance(f"{ambulance_id}_{algorithm_name}", edge_path, start_node, end_node)
            ambulance_index += 1

        for ambulance_id, start_node, end_node in AMBULANCES:
            vehicle_id = f"{ambulance_id}_{algorithm_name}"
            if vehicle_id in traci.vehicle.getIDList():
                current_edge = traci.vehicle.getRoadID(vehicle_id)
                if current_edge == end_edge:
                    sim_time = traci.simulation.getTime()
                    results.append((ambulance_id, algorithm_name, sim_time - ambulance_start_time, computation_time, aco_time_overhead))
                    aco_time_overhead = 0 
                    traci.vehicle.remove(vehicle_id)
                    if ambulance_id == AMBULANCES[-1][0]:
                        continueACO = False

    return results

def main():
    try:
        results = []

        algorithms = [
            (djikstra, "Dijkstra"),
            (a_star, "A*"),
            (a_star_euclidean, "A* Euclidean"),
            (a_star_traffic_pheromone, "A* ACO")
        ]

        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ambulance_ID", "Algorithm", "Travel_Time", "Computation_Time", "ACO_Time_Overhead"])

        for algorithm, algorithm_name in algorithms:
            traci.start(["sumo", "-c", CONFIG_FILE])
            print(f"SUMO simulation started successfully for {algorithm_name}!")

            graph, pos = extract_graph(NETWORK_FILE)

            algorithm_results = run_algorithm(algorithm, algorithm_name, graph, pos)
            results.extend(algorithm_results)

            traci.close()

            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                for ambulance_id, algorithm_name, sim_time, computation_time, aco_time_overhead in algorithm_results:
                    writer.writerow([ambulance_id, algorithm_name, sim_time, computation_time, aco_time_overhead])
 
    except traci.exceptions.FatalTraCIError as e:
        print(f"TraCI error during simulation: {e}")
    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        end_simulation()

if __name__ == "__main__":
    main()
