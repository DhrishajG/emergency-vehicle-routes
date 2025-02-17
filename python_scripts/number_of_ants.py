import traci
import matplotlib.pyplot as plt
from algorithms import aco_shortest_path
from constants import ConfigFile, NetworkFile, AmbulanceRoutes
from ambulance_simulation import add_ambulance, end_simulation, track_ambulance
from graph_utils import extract_graph

CONFIG_FILE = ConfigFile.kyoto.value
NETWORK_FILE = NetworkFile.kyoto.value
AMBULANCES = AmbulanceRoutes.kyoto.value

NUM_ANTS = list(range(10, 101, 5))

def main():
    try:
        simulation_times = []
        for ants in NUM_ANTS:
            # Start the SUMO simulation
            sim_time = []

            for ambulance_id, start_node, end_node in AMBULANCES:
                traci.start(["sumo", "-c", CONFIG_FILE])
                graph, _ = extract_graph(NETWORK_FILE)
                edge_path = aco_shortest_path(graph, start_node, end_node, num_ants=ants)

                end_edge = edge_path[-1]

                # Add an ambulance to the simulation with the computed path
                add_ambulance(ambulance_id, edge_path, start_node, end_node)

                # Track the ambulance until it reaches its destination
                time = track_ambulance(ambulance_id, end_edge, end_node)
                traci.close()
                sim_time.append(time)
            simulation_times.append(sim_time)

        # Calculate the average simulation time for each number of ants
        avg_simulation_times = [sum(times) / len(times) for times in simulation_times]

        # Plot the results
        plt.figure(figsize=(10, 6))
        plt.plot(NUM_ANTS, avg_simulation_times, marker='o')
        plt.xlabel('Number of Ants')
        plt.ylabel('Average Simulation Time')
        plt.title('Average Simulation Time vs Number of Ants')
        plt.grid(True)
        plt.show()
        # Plot the individual simulation times for each ambulance
        plt.figure(figsize=(10, 6))
        for i, times in enumerate(zip(*simulation_times)):
            plt.plot(NUM_ANTS, times, marker='o', label=f'Ambulance {i+1}')
        plt.xlabel('Number of Ants')
        plt.ylabel('Simulation Time')
        plt.title('Simulation Time vs Number of Ants for Each Ambulance')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Plot the average simulation time
        plt.figure(figsize=(10, 6))
        plt.plot(NUM_ANTS, avg_simulation_times, marker='o')
        plt.xlabel('Number of Ants')
        plt.ylabel('Average Simulation Time')
        plt.title('Average Simulation Time vs Number of Ants')
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
