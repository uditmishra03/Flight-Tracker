import os
from pprint import pprint

import requests
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_data import FlightData

TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")
ORIGIN_CITY = "LON"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.datamanager = DataManager()

    @staticmethod
    def get_destination_code(city):
        request_url = "https://tequila-api.kiwi.com/locations/query"
        header = {
            "apikey": TEQUILA_API_KEY,
        }
        request_params = {
            "term": city,
            "location_types": "city"
        }

        response = requests.get(url=request_url, params=request_params, headers=header)
        code = response.json()['locations'][0]['code']
        return code

    @staticmethod
    def check_flight(destination_code):
        flight_search_url = "https://tequila-api.kiwi.com/v2/search?"
        date_from = datetime.now() + timedelta(days=1)
        till_date = datetime.now() + timedelta(days=180)

        header = {
            "apikey": TEQUILA_API_KEY,
        }
        # for each_row in self.sheet_data:
        params = {
            "fly_from": ORIGIN_CITY,
            "fly_to": destination_code,
            "date_from": date_from.strftime('%d/%m/%Y'),
            "date_to": till_date.strftime('%d/%m/%Y'),
            "flight_type": "round",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "curr": "GBP",
            "max_stopovers": 0,
            "one_for_city": 1,

        }

        response = requests.get(
            url=flight_search_url,
            headers=header,
            params=params,
        )
        try:
            data = response.json()["data"][0]
        except IndexError:
            params["max_stopovers"] = 1
            response = requests.get(
                url=flight_search_url,
                headers=header,
                params=params,
            )
            data = response.json()["data"][0]
            pprint(data)
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            # print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
