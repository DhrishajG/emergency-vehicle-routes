import xml.etree.ElementTree as ET

# List of trip files to combine
trip_files = [
    "trips_0000_0500.xml",
    "trips_0500_0700.xml",
    "trips_0700_0900.xml",
    "trips_0900_1200.xml",
    "trips_1200_1400.xml",
    "trips_1400_1700.xml",
    "trips_1700_1900.xml",
    "trips_1900_2100.xml",
    "trips_2100_0000.xml"
]

# Create a new root element for the combined trips
combined_root = ET.Element("routes")

# Counter to ensure unique IDs
vehicle_counter = 0

# Iterate through each trip file and add its trips to the combined root
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
combined_tree.write("osm.passenger.trips.24h.xml", encoding="utf-8", xml_declaration=True)

print(f"Combined trip files into osm.passenger.trips.24h.xml with {vehicle_counter} unique vehicle IDs.")