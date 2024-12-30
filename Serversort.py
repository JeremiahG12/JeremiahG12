import os
import csv
from datetime import datetime

# Paths
input_file = r"D:\AHDATA\test\processedah.csv"
output_folder = r"D:\AHDATA"  # Folder where separated files will be stored

# List of servers for categorization
servers = [
    "West America FL", "Eastern America FL", "Europe FL", "South America FL", "Japan, Oceania FL",
    "EARLY ACCESS West America", "EARLY ACCESS Eastern America", "EARLY ACCESS Europe", 
    "EARLY ACCESS South America", "EARLY ACCESS Japan, Oceania"
]

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to format server names for the file name
def format_server_name(server):
    if "EARLY ACCESS" in server:
        return "ea_" + server.replace("EARLY ACCESS", "").strip().replace(" ", "_")
    return server.replace(" ", "_")

# Read the input CSV file
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Process data for each server
for server in servers:
    # Filter rows that belong to the current server
    server_rows = [row for row in rows if row['server'] == server]
    
    if server_rows:
        # Create folder for server if it doesn't exist
        server_folder = os.path.join(output_folder, format_server_name(server))
        os.makedirs(server_folder, exist_ok=True)
        
        # Create a CSV file name with current timestamp
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(server_folder, f"{format_server_name(server)}_{current_datetime}.csv")
        
        # Write filtered rows into the corresponding CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            fieldnames = reader.fieldnames  # Use the same fieldnames as the original CSV
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()  # Write header row
            writer.writerows(server_rows)  # Write server-specific data

        print(f"Data for {server} has been written to {output_file}")

print("Processing complete.")
