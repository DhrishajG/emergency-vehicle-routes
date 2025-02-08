import traci
from ambulance_simulation import add_ambulance, track_ambulance, end_simulation
from algorithms import a_star, djikstra
from constants import ConfigFile, NetworkFile, StartNode, EndNode, CongestionPath, AccidentEdge
from traffic_simulations import toggle_scenario

CONFIG_FILE = ConfigFile.city_block.value
NETWORK_FILE = NetworkFile.city_block.value
START_NODE = StartNode.city_block.value
END_NODE = EndNode.city_block.value
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
        toggle_scenario('accident', enable=True, route=CONGESTION_ROUTE, accident_edge=ACCIDENT_EDGE, num_vehicles=7)

        edge_path = a_star(NETWORK_FILE, START_NODE, END_NODE)

        end_edge = edge_path[-1]

        # edge_path = traci.simulation.findRoute(START_EDGE, END_EDGE).edges
        # start_edge = START_EDGE
        # end_edge = END_EDGE

        # Add an ambulance to the simulation with the computed path
        add_ambulance(AMBULANCE_ID, edge_path, START_NODE, END_NODE)

        # Track the ambulance until it reaches its destination
        track_ambulance(AMBULANCE_ID, end_edge, END_NODE)
 
    except traci.exceptions.FatalTraCIError as e:
        print(f"TraCI error during simulation: {e}")
    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Ensure the simulation is closed
        end_simulation()

if __name__ == "__main__":
    main()
