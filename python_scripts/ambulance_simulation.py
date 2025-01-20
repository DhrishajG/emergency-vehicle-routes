import traci

def add_ambulance(vehicle_id, route, start_edge, end_edge):
    """Adds an ambulance to the simulation with a computed route."""
    # Use findRoute to calculate the route between start_edge and end_edge
    
    # Ensure the route contains valid edges
    if route.edges:
        # Add the ambulance to the simulation
        traci.vehicle.add(vehicle_id, routeID="", typeID="veh_emergency")
        # Set the computed route for the ambulance
        traci.vehicle.setRoute(vehicle_id, route.edges)
        print(f"Ambulance {vehicle_id} added with route from {start_edge} to {end_edge}.")
    else:
        print(f"No valid route found between {start_edge} and {end_edge}.")

def track_ambulance(vehicle_id, end_edge):
    """Tracks the ambulance's progress and terminates the simulation when it reaches the destination."""
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        current_edge = traci.vehicle.getRoadID(vehicle_id)
        print(f"Ambulance is on edge: {current_edge}")
        if current_edge == end_edge:
            print(f"Ambulance {vehicle_id} has reached its destination!")
            break
    traci.close()

def end_simulation():
    """Ends the SUMO simulation."""
    print("SUMO simulation ended.")
    traci.close()
