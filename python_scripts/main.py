import traci
from ambulance_simulation import add_ambulance, track_ambulance, end_simulation

CONFIG_FILE = "../sumo_simulations/city_block/osm.sumocfg"
START_EDGE = "1128395118"  
END_EDGE = "200574632"    
AMBULANCE_ID = "ambulance_1"

def main():
    """Main entry point for the simulation."""
    try:
        # Start the SUMO simulation
        traci.start(["sumo-gui", "-c", CONFIG_FILE])
        print("SUMO simulation started successfully!")

        # Add an ambulance to the simulation
        add_ambulance(AMBULANCE_ID, START_EDGE, END_EDGE)

        # Track the ambulance until it reaches its destination
        track_ambulance(AMBULANCE_ID, END_EDGE)

    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Ensure the simulation is closed
        end_simulation()

if __name__ == "__main__":
    main()
