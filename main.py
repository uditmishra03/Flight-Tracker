# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

SHEET_ENDPOINT = "https://api.sheety.co/ecf356f482c483019bec99c1e7e46d1a/flightDeals/prices"

# Creating objects of imported classes.
flightsearch = FlightSearch()
datamanager = DataManager()
notificationmanager = NotificationManager()

sheet_data = datamanager.get_destination_data()


if sheet_data[0]["iataCode"] == "":
    for data in sheet_data:
        data['iataCode'] = flightsearch.get_destination_code(data['city'])
    datamanager.update_destination_data()
    datamanager.destination_data = sheet_data

for destination in sheet_data:
    flight = flightsearch.check_flight(destination["iataCode"])
    try:
        if flight.price < destination['lowestPrice']:
            message = f"Low price alert! On ₤{flight.price} to fly from " \
                      f"{flight.origin_city}-{flight.origin_airport}" \
                      f"to {flight.destination_city}-{flight.destination_airport}," \
                      f" from {flight.out_date} to {flight.return_date}."
            notificationmanager.send_sms(message)
    except AttributeError as error:
        print(error)
        #
        # print(f"{flight.origin_city}'s flight is cheaper at price ₤{flight.price}")
        # print("Send notification with relevant details.")
