import os
import csv
from pathlib import Path
import pandas as pd

BASE_FOLDER = Path.home() / "WiggleBin"
DATA_FOLDER = BASE_FOLDER / "sensor-data"

def create_directory():
    os.makedirs(DATA_FOLDER, exist_ok=True)

def remove_columns_from_csv(filename, columns_to_remove):
    """Remove columns from a CSV file"""
    file_path = DATA_FOLDER / f"{filename}.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Drop the specified columns
    df.drop(columns=columns_to_remove, inplace=True)
    
    # Save the modified DataFrame back to the same CSV file
    df.to_csv(file_path, index=False)

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

        # Write a single row
        writer.writerow(sensor_data)

def write_rows_to_csv(sensor_data, filename, fieldnames):
    """Write data to a CSV file"""
    DATA_FILE = DATA_FOLDER / f"{filename}.csv"

    create_directory()

    with open(DATA_FILE, "a", newline="") as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        if os.stat(DATA_FILE).st_size == 0:
            writer.writeheader()

        # Write multiple rows
        writer.writerows(sensor_data)