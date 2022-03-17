#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager


# APP_ID =

# BEARER_TOKEN = 
SHEET_ENDPOINT = "https://api.sheety.co/d1c958dac821bf9335d44477eb417876/flightDeals/prices"

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


