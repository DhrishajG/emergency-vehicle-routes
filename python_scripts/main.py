import traci
from ambulance_simulation import add_ambulance, track_ambulance, end_simulation
from algorithms import a_star, djikstra, aco_shortest_path, a_star_traffic_pheromone
from constants import ConfigFile, NetworkFile, StartNode, EndNode, CongestionPath, AccidentEdge
from graph_utils import extract_graph
from traffic_simulations import toggle_scenario

CONFIG_FILE = ConfigFile.kyoto.value
NETWORK_FILE = NetworkFile.kyoto.value
START_NODE = StartNode.kyoto.value
END_NODE = EndNode.kyoto.value
AMBULANCE_ID = "ambulance_1"
CONGESTION_ROUTE = CongestionPath.city_block.value
ACCIDENT_EDGE = AccidentEdge.city_block.value

def main():
    """Main entry point for the simulation."""
    try:
        # Start the SUMO simulation
        traci.start(["sumo-gui", "-c", CONFIG_FILE])
        print("SUMO simulation started successfully!")

        # Add random congestion to the specified edge
        toggle_scenario('accident', enable=False, route=CONGESTION_ROUTE, accident_edge=ACCIDENT_EDGE, num_vehicles=15, duration=300)

        # Run some initial steps
        for step in range(200):  # Simulate for 200 steps
            traci.simulationStep()  # Advance the simulation by one step

        graph, pos = extract_graph(NETWORK_FILE)

        # edge_path = djikstra(graph, START_NODE, END_NODE)
        # edge_path = a_star(graph, pos, START_NODE, END_NODE)
        _ = aco_shortest_path(graph, START_NODE, END_NODE, num_ants=100)
        edge_path = a_star_traffic_pheromone(graph, pos, START_NODE, END_NODE)
        # edge_path = aco_shortest_path(graph, START_NODE, END_NODE, num_ants=90, beta=2.0)

        end_edge = edge_path[-1]

        ambulance_start_time = traci.simulation.getTime()

        # Add an ambulance to the simulation with the computed path
        add_ambulance(AMBULANCE_ID, edge_path, START_NODE, END_NODE)

        # Track the ambulance until it reaches its destination
        sim_time = track_ambulance(AMBULANCE_ID, end_edge, END_NODE)
        ambulance_time = sim_time - ambulance_start_time
        print(f"Ambulance reached the destination in {ambulance_time} seconds.")
 
    except traci.exceptions.FatalTraCIError as e:
        print(f"TraCI error during simulation: {e}")
    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Ensure the simulation is closed
        end_simulation()

if __name__ == "__main__":
    main()
