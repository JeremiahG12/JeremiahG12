import csv
import json
import os

# Paths
input_sales_data = r"D:\AHDATA\sales_data.csv"
traits_file = r"C:\Users\jerem\Desktop\java\traits.csv"
regions_file = r"D:\AHDATA\regions_definitions.txt"
output_file = r"D:\AHDATA\test\processedah.csv"

# Load traits into a dictionary (extract trait names from the 'value' field)
traits_map = {}
with open(traits_file, mode='r', newline='', encoding='utf-8') as traits_csv:
    traits_reader = csv.DictReader(traits_csv)
    for row in traits_reader:
        # Load the 'value' field as JSON and extract the 'name'
        trait_data = json.loads(row['value'])
        traits_map[row['trait']] = trait_data['name']

# Load server names into a dictionary from regions_definitions.txt (format "server_id = server_name")
regions_map = {}
with open(regions_file, mode='r', newline='', encoding='utf-8') as regions_txt:
    for line in regions_txt:
        # Split by '=' and strip spaces
        parts = line.strip().split('=', 1)
        if len(parts) == 2:
            regions_map[parts[0].strip()] = parts[1].strip()

# Process the sales_data.csv file
with open(input_sales_data, mode='r', newline='', encoding='utf-8') as infile, \
        open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = ['server', 'auctionData', 'quantity', 'price', 'sales']  # Specify the new column order
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    for row in reader:
        # Replace auctionData "id" with the name
        try:
            auction_data = json.loads(row['auctionData'])  # Parse the JSON string
            for i, item in enumerate(auction_data):
                # Replace the ID in auctionData with the name of the item
                item_name = item.get('auctionData', 'No match')  # In case 'auctionData' key is missing
                auction_data[i]['name'] = item_name
            row['auctionData'] = json.dumps(auction_data)  # Convert back to JSON string
        except (json.JSONDecodeError, KeyError, TypeError):
            # Log or handle malformed auctionData
            print(f"Skipping malformed auctionData in row: {row}")
            row['auctionData'] = row['auctionData']  # Keep original auctionData if parsing fails
        
        # Replace traits in the sales field
        try:
            sales = json.loads(row['sales'])  # Parse the sales JSON string
            formatted_sales = []
            for sale in sales:
                if 't' in sale:  # Check if 't' key exists (trait ID)
                    trait_id = str(sale['t'])  # Convert trait ID to string
                    trait_name = traits_map.get(trait_id, trait_id)  # Replace if found, else keep original
                    formatted_sales.append(f"[{trait_name}, {sale['c']}, {sale['p']}]")
            
            # Join the formatted sales entries with commas
            row['sales'] = ", ".join(formatted_sales)
        except (json.JSONDecodeError, KeyError, TypeError):
            # Log or handle malformed sales data
            print(f"Skipping malformed sales data in row: {row}")
            row['sales'] = row['sales']  # Keep original sales data if parsing fails

        # Replace server ID with server name
        server_id = row['server']
        row['server'] = regions_map.get(server_id, server_id)  # Replace with name if found
        
        # Write updated row (id is removed here)
        row.pop('id', None)  # Remove the 'id' field from the row
        # Write row with formatted sales data
        writer.writerow(row)

print(f"Output written to {output_file}")
