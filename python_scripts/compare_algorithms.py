import traci
import matplotlib.pyplot as plt
from algorithms import a_star, djikstra
from constants import ConfigFile, NetworkFile, AmbulanceRoutes
from ambulance_simulation import add_ambulance, end_simulation, track_ambulance
from graph_utils import extract_graph

CONFIG_FILE = ConfigFile.city_block.value
NETWORK_FILE = NetworkFile.city_block.value
AMBULANCES = AmbulanceRoutes.city_block.value

def main():
    try:
        djikstra_times = []
        a_star_times = []
        for ambulance_id, start_node, end_node in AMBULANCES:
            # Start the SUMO simulation
            traci.start(["sumo", "-c", CONFIG_FILE])
            graph, pos = extract_graph(NETWORK_FILE)
            edge_path = djikstra(graph, start_node, end_node)

            end_edge = edge_path[-1]

            # Add an ambulance to the simulation with the computed path
            add_ambulance(ambulance_id, edge_path, start_node, end_node)

            # Track the ambulance until it reaches its destination
            time = track_ambulance(ambulance_id, end_edge, end_node)
            traci.close()
            djikstra_times.append(time)
        
        for ambulance_id, start_node, end_node in AMBULANCES:
            # Start the SUMO simulation
            print("ambulance", ambulance_id)
            traci.start(["sumo", "-c", CONFIG_FILE])
            graph, pos = extract_graph(NETWORK_FILE)
            edge_path = a_star(graph, pos, start_node, end_node)

            end_edge = edge_path[-1]

            # Add an ambulance to the simulation with the computed path
            add_ambulance(ambulance_id, edge_path, start_node, end_node)

            # Track the ambulance until it reaches its destination
            time = track_ambulance(ambulance_id, end_edge, end_node)
            traci.close()
            a_star_times.append(time)

        # Plot the results
        ambulance_indices = range(len(AMBULANCES))
        bar_width = 0.35

        plt.figure(figsize=(10, 5))
        plt.bar(ambulance_indices, djikstra_times, width=bar_width, label='Dijkstra', align='center')
        plt.bar([i + bar_width for i in ambulance_indices], a_star_times, width=bar_width, label='A*', align='center')
        plt.xlabel('Ambulance Index')
        plt.ylabel('Time (s)')
        plt.title('Comparison of Dijkstra and A* Algorithms')
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
