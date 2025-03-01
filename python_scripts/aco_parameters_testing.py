import traci
import csv
import matplotlib.pyplot as plt
from algorithms import aco_shortest_path
from constants import ConfigFile, NetworkFile, AmbulanceRoutes
from ambulance_simulation import add_ambulance, end_simulation, track_ambulance
from graph_utils import extract_graph

CONFIG_FILE = ConfigFile.kyoto.value
NETWORK_FILE = NetworkFile.kyoto.value
AMBULANCES = AmbulanceRoutes.kyoto.value

NUM_ANTS = list(range(50, 201, 10)) 
BETA_VALUES = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
AMBULANCE_ID = "ambulance_1"
ANTS_CSV_FILE = "../outputs/ants_testing_results.csv"
BETA_CSV_FILE = "../outputs/beta_testing_results.csv"

def main():
    try:
        with open(BETA_CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ambulance_ID", "Beta", "Route_Time"])

            for ambulance_id, start_node, end_node in AMBULANCES[:5]:
                for beta in BETA_VALUES:
                    traci.start(["sumo", "-c", CONFIG_FILE])
                    graph, _ = extract_graph(NETWORK_FILE)
                    edge_path = aco_shortest_path(graph, start_node, end_node, num_ants=100, beta=beta)

                    end_edge = edge_path[-1]

                    # Add an ambulance to the simulation with the computed path
                    add_ambulance(ambulance_id, edge_path, start_node, end_node)

                    # Track the ambulance until it reaches its destination
                    time = track_ambulance(ambulance_id, end_edge, end_node)
                    traci.close()

                    # Write the results to the CSV file
                    writer.writerow([ambulance_id, beta, time])

        with open(ANTS_CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ambulance_ID", "Num_Ants", "Route_Time"])

            for ambulance_id, start_node, end_node in AMBULANCES:
                for ant in NUM_ANTS:
                    traci.start(["sumo", "-c", CONFIG_FILE])
                    graph, _ = extract_graph(NETWORK_FILE)
                    edge_path = aco_shortest_path(graph, start_node, end_node, num_ants=ant, beta=2.0)

                    end_edge = edge_path[-1]

                    # Add an ambulance to the simulation with the computed path
                    add_ambulance(ambulance_id, edge_path, start_node, end_node)

                    # Track the ambulance until it reaches its destination
                    time = track_ambulance(ambulance_id, end_edge, end_node)
                    traci.close()

                    # Write the results to the CSV file
                    writer.writerow([ambulance_id, ant, time])

    except traci.exceptions.FatalTraCIError as e:
        print(f"TraCI error during simulation: {e}")
    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Ensure the simulation is closed
        end_simulation()

if __name__ == "__main__":
    main()
