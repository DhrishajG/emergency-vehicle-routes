import traci
import csv
import matplotlib.pyplot as plt
from algorithms import aco_shortest_path
from constants import ConfigFile, NetworkFile, StartNode, EndNode
from ambulance_simulation import add_ambulance, end_simulation, track_ambulance
from graph_utils import extract_graph

CONFIG_FILE = ConfigFile.kyoto.value
NETWORK_FILE = NetworkFile.kyoto.value
START_NODE = StartNode.kyoto.value
END_NODE = EndNode.kyoto.value

NUM_ANTS = list(range(50, 101, 10)) 
BETA_VALUES = [2.0, 3.0, 4.0, 5.0]
AMBULANCE_ID = "ambulance_1"
CSV_FILE = "../outputs/parameter_testing_results.csv"

def main():
    try:
        simulation_times = {beta: [] for beta in BETA_VALUES}
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Num_Ants", "Beta", "Simulation_Time"])

            for ants in NUM_ANTS:
                for beta in BETA_VALUES:
                    traci.start(["sumo", "-c", CONFIG_FILE])
                    graph, _ = extract_graph(NETWORK_FILE)
                    edge_path = aco_shortest_path(graph, START_NODE, END_NODE, num_ants=ants, beta=beta)

                    end_edge = edge_path[-1]

                    # Add an ambulance to the simulation with the computed path
                    add_ambulance(AMBULANCE_ID, edge_path, START_NODE, END_NODE)

                    # Track the ambulance until it reaches its destination
                    time = track_ambulance(AMBULANCE_ID, end_edge, END_NODE)
                    traci.close()
                    simulation_times[beta].append(time)

                    # Write the results to the CSV file
                    writer.writerow([ants, beta, time])

        # Plot the individual simulation times for each beta value
        plt.figure(figsize=(10, 6))
        for beta, times in simulation_times.items():
            plt.plot(NUM_ANTS, times, marker='o', label=f'Beta {beta}')
        plt.xlabel('Number of Ants')
        plt.ylabel('Simulation Time')
        plt.title('Simulation Time vs Number of Ants for Each Beta Value')
        plt.legend()
        plt.grid(True)
        plt.show()
 
    except traci.exceptions.FatalTraCIError as e:
        print(f"TraCI error during simulation: {e}")
    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Ensure the simulation is closed
        end_simulation()

if __name__ == "__main__":
    main()
