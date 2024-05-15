# WIP


import requests
import json

BASE_URL = 'http://rocketry.sidneypauly.me:5000'
VESSEL_NAME = 'Fayre Demo'
PART_NAME = 'Battery'
FLIGHT_NAME = 'Flight 2024-05-04T12:16:31.384663'


vessels_request = requests.get(f'{BASE_URL}/vessel/get_by_name/{VESSEL_NAME}')
vessels = vessels_request.json()
#print(vessels)
vessel = vessels[2]

parts_list = []
for each in vessel["parts"]:
    parts_list.append(each['name'])

print(parts_list)


for part in parts_list:
    part_part = [p for p in vessel["parts"] if (part in p["name"])][0]

    flights_request = requests.get(f'{BASE_URL}/flight/get_by_name/{vessel["_id"]}/{FLIGHT_NAME}')
    flights = flights_request.json()
    flight = flights[0]

    measurements_request = requests.get(f'{BASE_URL}/flight_data/get_range/{flight["_id"]}/{part_part["_id"]}/{flight["start"]}/{flight["end"]}')

    measurements = measurements_request.json()

    print(measurements)

"""
battery_part = [p for p in vessel["parts"] if (PART_NAME in p["name"])][0]

flights_request = requests.get(f'{BASE_URL}/flight/get_by_name/{vessel["_id"]}/{FLIGHT_NAME}')
flights = flights_request.json()
flight = flights[0]

measurements_request = requests.get(f'{BASE_URL}/flight_data/get_range/{flight["_id"]}/{battery_part["_id"]}/{flight["start"]}/{flight["end"]}')
measurements = measurements_request.json()

print(measurements)"""