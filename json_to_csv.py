import os
import json
import csv
# Filepath of Raw Data Folder
# Should have numbered json files inside it
raw_data_path = "flight4may2024"

output_file_path = raw_data_path + "/" + "output.csv"

file_data = []

# Read all files in the folder
for filename in os.listdir(raw_data_path):
    if filename.endswith(".json"):
        print(filename)
        with open(raw_data_path + "/" + filename) as f:
            # Find ][ and insert , between them
            text = f.read()
            text = text.replace("][", "],[")
            text = "[" + text + "]"
    

            # Once checked then load
            data = json.loads(text)
            file_data.extend(data)

new_file_data = []
for data in file_data:
    new_file_data.extend(data)
# file_data is now a flat array
file_data = new_file_data

csv_data = {}

header = set(['timestamp'])

for entry in file_data:
    part_id = entry['part_id']
    field_names = entry['field_names']
    measurements = entry['measurements']

    for measurement in measurements:
        # Get the Timestamp for this measurement
        timestamp = measurement[0]
        values = measurement[1]

        # Initialise the dictionary for this timestamp
        if timestamp not in csv_data:
            csv_data[timestamp] = {'timestamp': timestamp}
        
        # Append data under correct column name

        for i, value in enumerate(values):
            column_name = f"{part_id}_{field_names[i]}"
            header.add(column_name)
            csv_data[timestamp][column_name] = value
    
# Write to CSV
header = list(header)

with open(output_file_path, mode='w',newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    for timestamp in sorted(csv_data.keys()):
        writer.writerow(csv_data[timestamp])

print("Output written to", output_file_path)