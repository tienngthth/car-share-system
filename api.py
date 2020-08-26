#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from model.database import Database
from model.context import Context
from model.preference import Preference
from model.util import Util

app = Flask(__name__)
preference = Preference()

# Function to catch GET API
@app.route('/get/newest/context', methods=['GET'])
def get_context():
    try:
        return get_latest_context()
    except:
        # Return error message if not be able to connect to database and table
        return "Fail to get latest context record from database, please check your database and table"

# Get latest context record from the database
def get_latest_context():
    record = Database.select_a_record("*",  " ORDER BY timestamp DESC LIMIT 1")
    json_content = {
        "timestamp" : record[0],
        "temp" : record[1],
        "humidity" : record[2]
    }
    # Return result in json format
    return jsonify(json_content)

# Function to catch POST API
@app.route('/upload/context', methods=['POST'])
def upload_context():
    try:
        # Try to get temperature and humidity values from request's json
        try:
            temp = request.json['temp']
            humidity = request.json['humidity']
        except:
            # Return error message if missing temperature or humidity
            return "Missing temperature or humidity"
        # Check if input is valid float for temperature and humidity
        if Util.check_float(str(temp)) and Util.check_float(str(humidity)):
            Context().update_context(temp, humidity, None, True)
            return "Successfully upload new context"
        else:
            # Return error message if input has invalid format
            return "Wrong temperture or humidity format, invalid number"
    except:
        # Return error message if something goes wrong, i.e. with database
        return "Fail to create new context"

# Function to catch PUT API
@app.route('/update/newest/context', methods=['PUT'])
def update_context():
    return update_temp() + "\n" + update_humidity()

def update_temp():
    # Try to get temperature value from request's json
    try:
        temp = request.json['temp']
        if Util.check_float(str(temp)):
            Database.update_last_record("temp", (temp,))
            return "Successfully update temperature"
        else:
            # Return error message if input has invalid format
            return "Wrong temperture format, invalid number"
    except:
        # Return message if no temperature found
        return "Temperature is not updated"

def update_humidity():
    # Try to get humidity value from request's json
    try:
        humidity = request.json['humidity']
        if Util.check_float(str(humidity)):
            Database.update_last_record("humidity", (humidity,))
            return "Successfully update humidity"
        else:
            # Return error message if input has invalid format
            return "Wrong humidity format, invalid number"
    except:
        # Return message if no humidity found
        return "Humidity is not updated"

if __name__ == "__main__":
    app.run(debug=True, port=8080)