import os
import requests
import csv

BASE_URL = 'https://api.uoarocketry.org/'

def make_request(route,payload):
    url = BASE_URL + route
    print(url)
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("GET", url, headers=headers, data = payload)

    return response


# Get the correct flight
VESSEL_ID = '41a0a99c-2b26-4a92-9ed7-fa38e8a969ef'

FLIGHT_ID = '6caa6cf3-9e54-4832-9402-781a45c37f1a'

resolution = 'second'

# Note: the above values can be found in the url of the front end client. app.uoarocketry.org/flights/VESSEL_ID/FLIGHT_ID

all_flights = make_request(f"flight/get_all/{VESSEL_ID}",{}).json()

# Get the flight where the _id = FLIGHT_ID
for flight in all_flights:
    if flight['_id'] == FLIGHT_ID:
        flight_data = flight
        break

# Get the csv data

if not flight_data:
    print("Flight not found")
    exit()

#print(flight_data)

# get the beginning and end times of the flight
flight_start = flight_data['start']
flight_end = flight_data['end']

parts_arr = []

# Get the part ids

for part in flight_data['measured_parts']:
    parts_arr.append(part)

#print(parts_arr)

parts_data = {}

for part in parts_arr:
    print(part)
    part_data = make_request(f"flight_data/get_aggregated_range/{FLIGHT_ID}/{part}/{resolution}/{flight_start}/{flight_end}",{})
    parts_data[part] = part_data.json()

print(parts_data)
this_dir = os.path.dirname(os.path.realpath(__file__))

# Create the 'csv' directory if it doesn't exist
csv_dir = os.path.join(this_dir, 'csv')
os.makedirs(csv_dir, exist_ok=True)

csv_file = os.path.join(csv_dir, 'flight_data.csv')

# Write the parts_data to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Part', 'Data'])  # Write the header row
    for part, data in parts_data.items():
        writer.writerow([part, data])

print(f"CSV file created successfully at: {csv_file}")