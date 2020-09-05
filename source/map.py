from geopy.geocoders import Nominatim
from flask import Flask, Markup, render_template, request
from model.database import Database
import requests

app = Flask(__name__)

def get_coordinates(backlog_ID):
    link1 = "http://127.0.0.1:8080/cars/get/car/latitude/from/backlog?id={}".format(str(backlog_ID))
    link2 = "http://127.0.0.1:8080/cars/get/car/longtitude/from/backlog?id={}".format(str(backlog_ID))
    latitude = requests.get(link1).text.strip("][")
    longtitude = requests.get(link2).text.strip("][")
    return float(latitude), float(longtitude)

@app.route('/map/backlog')
def map():
    lattitude = get_coordinates(request.args.get("id"))[0]
    longtitude = get_coordinates(request.args.get("id"))[1]
    return render_template('map.html', title='Map', lattitude=lattitude, longtitude=longtitude)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)