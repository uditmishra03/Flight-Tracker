import os
import requests

SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
USERS_SHEET_ENDPOINT = "https://api.sheety.co/3035a5e901f624a4258bcdb560c3d9a3/flightDeals/users"


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

    def get_customer_emails(self):
        customers_endpoint = USERS_SHEET_ENDPOINT
        response = requests.get(url=customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data