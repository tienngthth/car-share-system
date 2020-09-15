import requests
from geopy.geocoders import Nominatim

class GoogleMap:
    @staticmethod
    def get_coordinates(backlog_ID):
        latitude = requests.get("http://127.0.0.1:8080/cars/get/car/latitude/from/backlog?id={}"
        .format(str(backlog_ID))).json()["car"][0]["Latitude"]
        longitude = requests.get("http://127.0.0.1:8080/cars/get/car/longitude/from/backlog?id={}"
        .format(str(backlog_ID))).json()["car"][0]["Longitude"]
        return latitude, longitude

    @staticmethod
    def get_address(latitude, longitude):
        geolocator = Nominatim(user_agent="nguyenthanhtamahs@gmail.com")
        coordinates = str(latitude) + ", " + str(longitude)
        location = geolocator.reverse(coordinates)
        return location.address
