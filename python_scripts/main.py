import traci
from ambulance_simulation import add_ambulance, track_ambulance, end_simulation
from algorithms import djikstra

CONFIG_FILE = "../sumo_simulations/small_block/osm.sumocfg"
NETWORK_FILE = "../sumo_simulations/small_block/osm.net.xml.gz"
START_NODE = "25445347"  # for small block
END_NODE = "cluster_12485172228_30763597"  # for small block
AMBULANCE_ID = "ambulance_1"

def main():
    """Main entry point for the simulation."""
    try:
        edge_path = djikstra(NETWORK_FILE, START_NODE, END_NODE)

        start_edge = edge_path[0]
        end_edge = edge_path[-1]
        
        # Start the SUMO simulation
        traci.start(["sumo-gui", "-c", CONFIG_FILE])
        print("SUMO simulation started successfully!")

        # Add an ambulance to the simulation with the computed path
        add_ambulance(AMBULANCE_ID, edge_path, start_edge, end_edge)

        # Track the ambulance until it reaches its destination
        track_ambulance(AMBULANCE_ID, end_edge)
 
    except traci.exceptions.FatalTraCIError as e:
        print(f"TraCI error during simulation: {e}")
    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Ensure the simulation is closed
        end_simulation()

if __name__ == "__main__":
    main()
