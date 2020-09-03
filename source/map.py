from geopy.geocoders import Nominatim
from flask import Flask, Markup, render_template
from model.database import Database

app = Flask(__name__)

#In reality we don't get the coordinates from a certain address. The coordinates are retrieved first and the location is figured out based on the coordinates
#How this program works:
#1) Get backlog number 3 (Backlogs.ID = 3)
#2) Get the car listed in the backlog (CarID = 7)
#3) Get the location of the car (address)
#4) Get the real-life coordinates of that address
#5) Display those coordinates on the Google Map, with a marker pointing to it

def get_address_from_car_in_backlog(ID):        #Temporary fucntion
    address = Database.select_record("Cars.Location", "Cars INNER JOIN Backlogs ON Cars.ID = Backlogs.CarID", " WHERE Backlogs.ID = " + str(ID))
    return address[0][0]

def get_coordinates():
    geolocator = Nominatim(user_agent="nguyenthanhtamahs@gmail.com")
    address = get_address_from_car_in_backlog(3)
    location = geolocator.geocode(address)
    lattitude = location.latitude
    longtitude = location.longitude
    return lattitude, longtitude

@app.route('/map')
def map():
    lattitude = get_coordinates()[0]
    longtitude = get_coordinates()[1]
    return render_template('map.html', title='Map', lattitude=lattitude, longtitude=longtitude)

#@app.route('/map')
#def map():
#    lattitude = lattitude_from_Pi
#    longtitude = longtitude_from_Pi
#    return render_template('map.html', title='Map', lattitude=lattitude, longtitude=longtitude)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)