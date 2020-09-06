import requests

def get_coordinates(backlog_ID):
    link1 = "http://127.0.0.1:8080/cars/get/car/latitude/from/backlog?id={}".format(str(backlog_ID))
    link2 = "http://127.0.0.1:8080/cars/get/car/longtitude/from/backlog?id={}".format(str(backlog_ID))
    latitude = requests.get(link1).text.strip("][")
    longtitude = requests.get(link2).text.strip("][")
    return float(latitude), float(longtitude)