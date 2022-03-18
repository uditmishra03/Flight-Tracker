import requests

SHEET_ENDPOINT = "https://api.sheety.co/ecf356f482c483019bec99c1e7e46d1a/flightDeals/prices"


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEET_ENDPOINT)
        self.destination_data = response.json()['prices']
        return self.destination_data

    def update_destination_data(self):
        for each in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": each['iataCode']
                }
            }
            update_endpoint = f"{SHEET_ENDPOINT}/{each['id']}"
            response = requests.put(url=update_endpoint, json=new_data)
            print(response.text)
