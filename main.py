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
    if flight is None:
        continue
    try:
        if flight.price < destination['lowestPrice']:
            users = datamanager.get_customer_emails()
            emails = [row["email"] for row in users]
            names = [row["firstName"] for row in users]

            message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}" \
                      f"-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}," \
                      f" from {flight.out_date} to {flight.return_date}."

            if flight.stop_overs > 0:
                message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

            link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}." \
                   f"{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}." \
                   f"{flight.origin_airport}.{flight.return_date}"

            notificationmanager.send_emails(emails, message, link)

    except AttributeError as error:
        print(error)

