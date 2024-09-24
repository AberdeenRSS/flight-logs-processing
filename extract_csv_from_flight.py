from datetime import datetime, timedelta
import os
from pathlib import Path
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

REQUEST_INTERVAL = timedelta(minutes=5)

resolution = 'decisecond'

export_dir = os.path.dirname(os.path.realpath(__file__)) + '/data'

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

vessel = make_request(f'vessel/get/{VESSEL_ID}/{flight_data["_vessel_version"]}', {}).json()

# get the beginning and end times of the flight
flight_start = datetime.fromisoformat(flight_data['start'])
flight_end = datetime.fromisoformat(flight_data['end'])

print(f'Exporting data for flight {flight["name"]} between {flight_start} and {flight_end}')


#print(parts_arr)

print(f'Creating export folder at {export_dir}')

Path(export_dir).mkdir(parents=True, exist_ok=True)

for part in vessel['parts']:
    
    print(f'Aquiring data for part {part["name"]}')

    series = ['Time']
    data_series = []

    for s in flight["measured_parts"][part["_id"]]:
        data_series.append(s['name'])
        series.append(s["name"])

    # Create the 'csv' directory if it doesn't exist
    csv_dir = os.path.join(export_dir, flight["name"])
    os.makedirs(csv_dir, exist_ok=True)

    csv_file = os.path.join(csv_dir, f'{part["name"]}.csv')

    # Write the parts_data to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(series)  # Write the header row

        cur = flight_start

        while cur < flight_end:


            part_data = make_request(f'flight_data/get_range/{FLIGHT_ID}/{part["_id"]}/{cur.isoformat()}/{(cur + REQUEST_INTERVAL).isoformat()}',{})
            part_data_json = part_data.json()

            part_data_json.sort(key = lambda o: o["_start_time"] )


            for data in part_data_json:

                for s in data["measurements"]:

                    row = [datetime.fromtimestamp(s[0]).isoformat()]
                    row.extend(s[1])

                    writer.writerow(row)
            
            cur += REQUEST_INTERVAL

    print(f"CSV file created successfully at: {csv_file}")