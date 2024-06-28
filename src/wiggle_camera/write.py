import os
import csv
from pathlib import Path

BASE_FOLDER = Path.home() / "WiggleBin"
DATA_FOLDER = BASE_FOLDER / "sensor-data"

def create_directory():
    os.makedirs(DATA_FOLDER, exist_ok=True)

def write_to_csv(sensor_data, filename, fieldnames):
    """Write data to a CSV file"""
    DATA_FILE = DATA_FOLDER / f"{filename}.csv"

    create_directory()

    with open(DATA_FILE, "a", newline="") as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        if os.stat(DATA_FILE).st_size == 0:
            writer.writeheader()

        # Write the sensor data
        writer.writerow(sensor_data)