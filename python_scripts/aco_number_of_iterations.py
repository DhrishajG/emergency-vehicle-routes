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

NUM_ANTS = 90
BETA_VALUE = 2.0
AMBULANCE_ID = "ambulance_1"
NUM_ITERATIONS = list(range(50, 200, 10))
NUM_TRIALS = 5

def main():
    try:
        simulation_times = []
        
        for iter in NUM_ITERATIONS:
            trial_times = []
            for _ in range(NUM_TRIALS):
                traci.start(["sumo", "-c", CONFIG_FILE])
                graph, _ = extract_graph(NETWORK_FILE)
                edge_path = aco_shortest_path(graph, START_NODE, END_NODE, num_ants=NUM_ANTS, beta=BETA_VALUE, num_iterations=iter)
                add_ambulance(AMBULANCE_ID, edge_path, START_NODE, END_NODE)
                time = track_ambulance(AMBULANCE_ID, edge_path[-1], END_NODE)
                traci.close()
                trial_times.append(time)
            
            avg_time = sum(trial_times) / NUM_TRIALS
            simulation_times.append(avg_time)

            # Start the SUMO simulation
            # traci.start(["sumo", "-c", CONFIG_FILE])
            # graph, _ = extract_graph(NETWORK_FILE)
            # edge_path = aco_shortest_path(graph, START_NODE, END_NODE, num_ants=NUM_ANTS, beta=BETA_VALUE, num_iterations=iter)

            # end_edge = edge_path[-1]

            # # Add an ambulance to the simulation with the computed path
            # add_ambulance(AMBULANCE_ID, edge_path, START_NODE, END_NODE)

            # # Track the ambulance until it reaches its destination
            # time = track_ambulance(AMBULANCE_ID, end_edge, END_NODE)
            # traci.close()
            # simulation_times.append(time)

        with open('../outputs/simulation_times.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Number of Iterations', 'Average Simulation Time'])
            for iter, time in zip(NUM_ITERATIONS, simulation_times):
                csvwriter.writerow([iter, time])


        # Plot the simulation times for each beta value
        plt.figure(figsize=(10, 6))
        plt.plot(NUM_ITERATIONS, simulation_times, marker='o')
        plt.xlabel('Number of Iterations')
        plt.ylabel('Simulation Time')
        plt.title('Simulation Time vs Number of Iterations')
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
