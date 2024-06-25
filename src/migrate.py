import os
import json
from datetime import datetime

# Configuration for the directory to store vessel data
VESSEL_DATA_DIR = 'thames-london'
KNOWN_VESSELS_FILE = 'thames-london.json'

# Ensure the directory exists
if not os.path.exists(VESSEL_DATA_DIR):
    os.makedirs(VESSEL_DATA_DIR)

# Function to read known vessels data from the JSON file
def read_known_vessels(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to create individual vessel files in the new format
def migrate_vessel_data(known_vessels):
    for mmsi, last_seen in known_vessels.items():
        filename = os.path.join(VESSEL_DATA_DIR, f"{mmsi}.json")
        date_seen = last_seen.split('T')[0]
        vessel_data = {
            "last_seen": last_seen,
            "dates_seen": [date_seen],
            "last_full_data": {}
        }
        with open(filename, 'w') as file:
            json.dump(vessel_data, file, sort_keys=True, indent=2)
        print(f"Migrated data for vessel MMSI {mmsi}")

# Read the known vessels from the original file
known_vessels = read_known_vessels(KNOWN_VESSELS_FILE)

# Migrate the data to the new format
migrate_vessel_data(known_vessels)

print("Migration completed.")