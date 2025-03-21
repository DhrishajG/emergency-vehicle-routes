import traci
import csv
import time
from algorithms import a_star, djikstra, aco_shortest_path, a_star_euclidean, a_star_traffic_pheromone
from constants import ConfigFile, NetworkFile, AmbulanceRoutes
from ambulance_simulation import add_ambulance, end_simulation
from graph_utils import extract_graph

CONFIG_FILE = ConfigFile.kyoto.value
NETWORK_FILE = NetworkFile.kyoto.value 
AMBULANCES = AmbulanceRoutes.kyoto_24_hours.value # Using fewer ambulances for testing
CSV_FILE = "../outputs/algorithm_comparison_week.csv"

# Simulation constants
SIM_SECONDS_PER_HOUR = 3600
TOTAL_SIM_TIME = 604800  # 7 days
ACO_UPDATE_INTERVAL = 720

def run_algorithm(algorithm, algorithm_name, graph, pos):
    results = []
    hour = 0
    active_ambulances = {} 
    
    while traci.simulation.getTime() < TOTAL_SIM_TIME:
        current_time = traci.simulation.getTime()

        # Run ACO updates
        if algorithm == a_star_traffic_pheromone and current_time % ACO_UPDATE_INTERVAL == 0 and current_time % SIM_SECONDS_PER_HOUR != 0 and hour < 168:
            print(f"\nUpdating pheromones at time {current_time}")
            graph, pos = extract_graph(NETWORK_FILE, old_graph=graph)
            for aid, start_node, end_node in AMBULANCES:
                print(f"Running ACO for {aid}")
                _ = aco_shortest_path(graph, start_node, end_node, num_ants=120, beta=2.5)
        
        # Dispatch new ambulances every hour
        if current_time >= hour * SIM_SECONDS_PER_HOUR and hour < 168:
            print(f"\nHour {hour}: Dispatching ambulances")
            
            for amb_id, start_node, end_node in AMBULANCES:
                vehicle_id = f"{amb_id}_{algorithm_name}_{hour}"
                try:
                    if algorithm_name == "Dijkstra":
                        edge_path = djikstra(graph, start_node, end_node)
                    elif algorithm_name == "A* Real Time":
                        edge_path = a_star(graph, pos, start_node, end_node)
                    elif algorithm_name == "A* Euclidean":
                        edge_path = a_star_euclidean(graph, pos, start_node, end_node)
                    elif algorithm_name == "A* ACO":
                        edge_path = a_star_traffic_pheromone(graph, pos, start_node, end_node)

                    if not edge_path:
                        print(f"No path found for {vehicle_id}")
                        continue

                    print(f"Adding {vehicle_id} with path: {edge_path}")
                    add_ambulance(vehicle_id, edge_path, start_node, end_node)
                    active_ambulances[vehicle_id] = (edge_path[-1], current_time, edge_path)
                    
                except Exception as e:
                    print(f"Error dispatching {vehicle_id}: {e}")
            
            hour += 1
        
        # Track ambulances
        finished = []
        for vehicle_id, (end_edge, start_time, edge_path) in active_ambulances.items():
            try:
                if vehicle_id in traci.vehicle.getIDList():
                    current_edge = traci.vehicle.getRoadID(vehicle_id)
                    
                    if current_edge == end_edge:
                        travel_time = current_time - start_time
                        amb_id = vehicle_id.split('_')[0]
                        dispatch_hour = int(vehicle_id.split('_')[-1])
                        results.append((amb_id, algorithm_name, travel_time, dispatch_hour))
                        print(f"{vehicle_id} completed route in {travel_time}s")
                        traci.vehicle.remove(vehicle_id)
                        finished.append(vehicle_id)
                    
            except traci.exceptions.TraCIException as e:
                print(f"Error tracking {vehicle_id}: {e}")
                finished.append(vehicle_id)
        
        for vehicle_id in finished:
            if vehicle_id in active_ambulances:
                active_ambulances.pop(vehicle_id)
        
        traci.simulationStep()
    
    print(f"\nSimulation ended. Processing {len(active_ambulances)} remaining ambulances")
    for vehicle_id, (_, start_time, _) in active_ambulances.items():
        amb_id = vehicle_id.split('_')[0]
        dispatch_hour = int(vehicle_id.split('_')[-1])
        results.append((amb_id, algorithm_name, TOTAL_SIM_TIME - start_time, dispatch_hour))
    
    return results

def main():
    try:
        results = []
        algorithms = [
            (djikstra, "Dijkstra"),
            (a_star, "A* Real Time"),
            (a_star_euclidean, "A* Euclidean"),
            (a_star_traffic_pheromone, "A* ACO"),
        ]

        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ambulance_ID", "Algorithm", "Travel_Time", "Hour"])

        for algorithm, algorithm_name in algorithms:
            print(f"\nStarting 1-week simulation for {algorithm_name}")
            traci.start(["sumo", "-c", CONFIG_FILE])
            
            graph, pos = extract_graph(NETWORK_FILE)
            algorithm_results = run_algorithm(algorithm, algorithm_name, graph, pos)
            results.extend(algorithm_results)
            
            traci.close()

            print(results)
            print(algorithm_results)
            
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                for amb_id, algorithm_name, travel_time, dispatch_hour in algorithm_results:
                    writer.writerow([amb_id, algorithm_name, travel_time, dispatch_hour])

    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        end_simulation()

if __name__ == "__main__":
    main()
