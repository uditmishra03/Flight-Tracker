#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager

SHEET_ENDPOINT = "https://api.sheety.co/ecf356f482c483019bec99c1e7e46d1a/flightDeals/prices"

# Creating objects of imported classes.
flightSearch = FlightSearch()
datamanager = DataManager()
# header = {
#     "x-app-id": APP_ID,
#     "x-app-key": API_KEY,
#     "Authorization": f"Bearer {BEARER_TOKEN}"
# }

sheet_data = datamanager.get_destination_data()
# pprint(sheet_data)

for data in sheet_data:
    if data['iataCode'] == "":
        data['iataCode'] = flightSearch.get_destination_code(data['city'])
datamanager.update_destination_data()
flightSearch.check_flight()
