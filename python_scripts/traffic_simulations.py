import traci
import random

def add_random_congestion(route, num_vehicles, speed=2):
    for i in range(num_vehicles):
        vehicle_id = f"congestion_{i}"
        traci.vehicle.add(vehicle_id, routeID="", typeID="veh_passenger")
        traci.vehicle.setRoute(vehicle_id, route)
        traci.vehicle.setSpeed(vehicle_id, speed)

def simulate_accident(accident_edge, route, num_vehicles, duration, prefix="accident"):
    crash_vehicle = f"{prefix}_1"
    for i in range(num_vehicles):
        vehicle_id = f"{prefix}_{i}"
        traci.vehicle.add(vehicle_id, routeID="", typeID="veh_passenger")
        traci.vehicle.setRoute(vehicle_id, route)
    traci.vehicle.setStop(crash_vehicle, edgeID=accident_edge, pos=random.uniform(0, traci.lane.getLength(accident_edge + "_0")), laneIndex=0, duration=duration)

def toggle_scenario(scenario, enable, **kwargs):
    if scenario == 'congestion':
        if enable:
            add_random_congestion(**kwargs)
    elif scenario == 'accident':
        if enable:
            simulate_accident(**kwargs)
