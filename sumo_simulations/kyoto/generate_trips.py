import subprocess
import xml.etree.ElementTree as ET
import os

# Define paths
sumo_home = os.environ.get("SUMO_HOME", "")  # Get SUMO_HOME environment variable
if not sumo_home:
    raise Exception("SUMO_HOME environment variable is not set. Please set it to the root of your SUMO installation.")

random_trips_path = os.path.join(sumo_home, "tools", "randomTrips.py")  # Path to randomTrips.py
network_file = "osm.net.xml.gz"  # Your SUMO network file
output_dir = "trip_files"  # Directory to store intermediate trip files
combined_file = "osm.passenger.trips.week.xml"  # Final combined trip file

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define insertion rates and time periods for each day
traffic_patterns = {
    "Sunday": [
        {"start": "00:00", "end": "05:00", "rate": 10, "description": "Very Light"},
        {"start": "05:00", "end": "07:00", "rate": 20, "description": "Light to Moderate"},
        {"start": "07:00", "end": "12:00", "rate": 40, "description": "Moderate"},
        {"start": "12:00", "end": "17:00", "rate": 60, "description": "Heavy (Peak)"},
        {"start": "17:00", "end": "21:00", "rate": 40, "description": "Moderate"},
        {"start": "21:00", "end": "00:00", "rate": 15, "description": "Very Light"}
    ],
    "Monday": [
        {"start": "00:00", "end": "02:00", "rate": 10, "description": "Very Light"},
        {"start": "02:00", "end": "05:00", "rate": 5, "description": "Quietest"},
        {"start": "05:00", "end": "07:00", "rate": 20, "description": "Light to Moderate"},
        {"start": "07:00", "end": "08:00", "rate": 30, "description": "Moderate"},
        {"start": "08:00", "end": "10:00", "rate": 60, "description": "Heavy (Peak)"},
        {"start": "10:00", "end": "14:00", "rate": 40, "description": "Moderate"},
        {"start": "14:00", "end": "19:00", "rate": 50, "description": "Heavy (Lunch + Evening Rush)"},
        {"start": "19:00", "end": "21:00", "rate": 30, "description": "Light to Moderate"},
        {"start": "21:00", "end": "00:00", "rate": 15, "description": "Very Light"}
    ],
    "Tuesday": [
        {"start": "00:00", "end": "02:00", "rate": 10, "description": "Very Light"},
        {"start": "02:00", "end": "05:00", "rate": 5, "description": "Quietest"},
        {"start": "05:00", "end": "07:00", "rate": 20, "description": "Light to Moderate"},
        {"start": "07:00", "end": "08:00", "rate": 30, "description": "Moderate"},
        {"start": "08:00", "end": "10:00", "rate": 60, "description": "Heavy (Peak)"},
        {"start": "10:00", "end": "14:00", "rate": 40, "description": "Moderate"},
        {"start": "14:00", "end": "19:00", "rate": 50, "description": "Heavy (Lunch + Evening Rush)"},
        {"start": "19:00", "end": "21:00", "rate": 30, "description": "Light to Moderate"},
        {"start": "21:00", "end": "00:00", "rate": 15, "description": "Very Light"}
    ],
    "Wednesday": [
        {"start": "00:00", "end": "02:00", "rate": 10, "description": "Very Light"},
        {"start": "02:00", "end": "05:00", "rate": 5, "description": "Quietest"},
        {"start": "05:00", "end": "07:00", "rate": 20, "description": "Light to Moderate"},
        {"start": "07:00", "end": "08:00", "rate": 30, "description": "Moderate"},
        {"start": "08:00", "end": "10:00", "rate": 60, "description": "Heavy (Peak)"},
        {"start": "10:00", "end": "14:00", "rate": 40, "description": "Moderate"},
        {"start": "14:00", "end": "19:00", "rate": 50, "description": "Heavy (Lunch + Evening Rush)"},
        {"start": "19:00", "end": "21:00", "rate": 30, "description": "Light to Moderate"},
        {"start": "21:00", "end": "00:00", "rate": 15, "description": "Very Light"}
    ],
    "Thursday": [
        {"start": "00:00", "end": "02:00", "rate": 10, "description": "Very Light"},
        {"start": "02:00", "end": "05:00", "rate": 5, "description": "Quietest"},
        {"start": "05:00", "end": "07:00", "rate": 20, "description": "Light to Moderate"},
        {"start": "07:00", "end": "08:00", "rate": 30, "description": "Moderate"},
        {"start": "08:00", "end": "10:00", "rate": 60, "description": "Heavy (Peak)"},
        {"start": "10:00", "end": "14:00", "rate": 40, "description": "Moderate"},
        {"start": "14:00", "end": "19:00", "rate": 50, "description": "Heavy (Lunch + Evening Rush)"},
        {"start": "19:00", "end": "21:00", "rate": 30, "description": "Light to Moderate"},
        {"start": "21:00", "end": "00:00", "rate": 15, "description": "Very Light"}
    ],
    "Friday": [
        {"start": "00:00", "end": "02:00", "rate": 10, "description": "Very Light"},
        {"start": "02:00", "end": "05:00", "rate": 5, "description": "Quietest"},
        {"start": "05:00", "end": "07:00", "rate": 20, "description": "Light to Moderate"},
        {"start": "07:00", "end": "08:00", "rate": 30, "description": "Moderate"},
        {"start": "08:00", "end": "10:00", "rate": 60, "description": "Heavy (Peak)"},
        {"start": "10:00", "end": "14:00", "rate": 40, "description": "Moderate"},
        {"start": "14:00", "end": "19:00", "rate": 50, "description": "Heavy (Lunch + Evening Rush)"},
        {"start": "19:00", "end": "21:00", "rate": 30, "description": "Light to Moderate"},
        {"start": "21:00", "end": "00:00", "rate": 15, "description": "Very Light"}
    ],
    "Saturday": [
        {"start": "00:00", "end": "05:00", "rate": 10, "description": "Very Light"},
        {"start": "05:00", "end": "07:00", "rate": 20, "description": "Light to Moderate"},
        {"start": "07:00", "end": "12:00", "rate": 40, "description": "Moderate"},
        {"start": "12:00", "end": "16:00", "rate": 70, "description": "Heavy (Peak)"},
        {"start": "16:00", "end": "21:00", "rate": 50, "description": "Moderate"},
        {"start": "21:00", "end": "00:00", "rate": 20, "description": "Very Light"}
    ]
}

# Function to convert time to seconds
def time_to_seconds(day, time_str):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    day_offset = days.index(day) * 86400  # 86400 seconds in a day
    hh, mm = map(int, time_str.split(":"))
    return day_offset + hh * 3600 + mm * 60

# Generate trip files for each day and time period
trip_files = []
vehicle_counter = 0

for day, periods in traffic_patterns.items():
    for period in periods:
        start_time = time_to_seconds(day, period["start"])
        end_time = time_to_seconds(day, period["end"])
        rate = period["rate"]
        # Replace colons with underscores in filenames
        trip_file = os.path.join(output_dir, f"trips_{day}_{period['start'].replace(':', '_')}_{period['end'].replace(':', '_')}.xml")

        # Generate trips using randomTrips.py
        subprocess.run([
            "python", random_trips_path,
            "-n", network_file,
            "-o", trip_file,
            "-b", str(start_time),
            "-e", str(end_time),
            "--insertion-density", str(rate),
            "--trip-attributes", "departLane=\"best\"",  # Trip attributes
            "--fringe-start-attributes", "departSpeed=\"max\"",  # Fringe start attributes
            "--validate",  # Validate trips
            "--remove-loops",  # Remove loops
            "--via-edge-types", "highway.motorway,highway.motorway_link,highway.trunk_link,highway.primary_link,highway.secondary_link,highway.tertiary_link",  # Via edge types
            "--vehicle-class", "passenger",  # Vehicle class
            "--vclass", "passenger",  # Vehicle class (alternative)
            "--prefix", "veh",  # Prefix for vehicle IDs
            "--min-distance", "300",  # Minimum distance between trips
            "--min-distance.fringe", "10",  # Minimum distance for fringe trips
            "--allow-fringe.min-length", "1000",  # Minimum length for fringe trips
            "--lanes"  # Use lanes
        ])

        trip_files.append(trip_file)
        print(f"Generated {trip_file} with insertion rate {rate} vehicles/hour")

# Combine trip files into a single file
combined_root = ET.Element("routes")

for trip_file in trip_files:
    tree = ET.parse(trip_file)
    root = tree.getroot()
    for trip in root:
        # Assign a new unique ID
        trip.set("id", f"veh_{vehicle_counter}")
        vehicle_counter += 1
        combined_root.append(trip)

# Write the combined trips to a new file
combined_tree = ET.ElementTree(combined_root)
combined_tree.write(combined_file, encoding="utf-8", xml_declaration=True)
print(f"Combined trip files into {combined_file} with {vehicle_counter} unique vehicle IDs")

# Delete intermediate trip files
for trip_file in trip_files:
    os.remove(trip_file)
print("Deleted intermediate trip files")

# Optionally, delete the output directory
os.rmdir(output_dir)
print(f"Deleted output directory {output_dir}")