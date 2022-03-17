import requests
from data_manager import DataManager



TEQUILA_API_KEY = "b9Lpp3coo06X2pa09KI_hpRr3PvBB36n"

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.price= 0
        self.departure_airport_code = None
        self.departure_city = None
