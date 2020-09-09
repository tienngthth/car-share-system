import requests
from geopy.geocoders import Nominatim

def get_coordinates(backlog_ID):
    link1 = "http://127.0.0.1:8080/cars/get/car/latitude/from/backlog?id={}".format(str(backlog_ID))
    link2 = "http://127.0.0.1:8080/cars/get/car/longitude/from/backlog?id={}".format(str(backlog_ID))
    latitude = requests.get(link1).text.strip("][")
    longitude = requests.get(link2).text.strip("][")
    return float(latitude), float(longitude)

def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="nguyenthanhtamahs@gmail.com")
    coordinates = str(latitude) + ", " + str(longitude)
    location = geolocator.reverse(coordinates)
    return location.address
