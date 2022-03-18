import requests
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_data import FlightData

TEQUILA_API_KEY = "b9Lpp3coo06X2pa09KI_hpRr3PvBB36n"
ORIGIN_CITY = "LON"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.datamanager = DataManager()

    def get_destination_code(self, city):
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

    def check_flight(self):
        self.sheet_data = self.datamanager.get_destination_data()
        self.flight_search_url = "https://tequila-api.kiwi.com/v2/search?"
        self.date_from = datetime.now() + timedelta(days=1)
        self.till_date = datetime.now() + timedelta(days=180)

        self.header = {
            "apikey": TEQUILA_API_KEY,
        }
        for each_row in self.sheet_data:
            self.params = {
                "fly_from": ORIGIN_CITY,
                "fly_to": each_row['iataCode'],
                "date_from": self.date_from.strftime('%d/%m/%Y'),
                "date_to": self.till_date.strftime('%d/%m/%Y'),
                "flight_type": "round",
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "curr": "GBP",
                "max_stopovers": 0,
                "one_for_city": 1,

            }

            self.response = requests.get(
                url=f"{self.flight_search_url}",
                headers=self.header,
                params=self.params,
            )
            try:
                data = self.response.json()["data"][0]

            except IndexError:
                print(f"No flights found for {each_row['iataCode']}.")
                return None

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
