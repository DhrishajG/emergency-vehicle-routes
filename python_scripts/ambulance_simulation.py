import traci

def add_ambulance(vehicle_id, route, start_node, end_node):
    """Adds an ambulance to the simulation with a computed route."""
    # Ensure the route contains valid edges
    try:
        # Add the ambulance to the simulation
        traci.vehicle.add(vehicle_id, routeID="", typeID="emergency")
        # Set the computed route for the ambulance
        traci.vehicle.setRoute(vehicle_id, route)
        # Allow the ambulance to pass through red lights
        traci.vehicle.setSpeedMode(vehicle_id, 39)
        print(f"Ambulance {vehicle_id} added with route from {start_node} to {end_node}.")
    except traci.exceptions.TraCIException as e:
        print(f"No valid route found between {start_node} and {end_node}.", e)

def track_ambulance(vehicle_id, end_edge, to_position):
    """Tracks the ambulance's progress and terminates the simulation when it reaches the destination."""
    reached_destination = False
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if vehicle_id in traci.vehicle.getIDList():
            current_edge = traci.vehicle.getRoadID(vehicle_id)
            vehicle_position = traci.vehicle.getPosition(vehicle_id)
            print(f"Ambulance is on edge: {current_edge}, position: {vehicle_position}")
            if current_edge == end_edge and vehicle_position == to_position:
                print(f"Ambulance {vehicle_id} has reached the destination node!")
                reached_destination = True
                break
        else:
            print(f"Vehicle {vehicle_id} is not found in the simulation. Possibly because it has reached destination")
            break
    if reached_destination:
        print("Ambulance reached the destination.")
        traci.close()

def end_simulation():
    """Ends the SUMO simulation."""
    print("SUMO simulation ended.")
    traci.close()
