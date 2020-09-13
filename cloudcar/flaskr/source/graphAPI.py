from flask import Blueprint, Flask, Markup, render_template
from model.database import Database
import requests

graph_api = Blueprint("graph_api", __name__)

@graph_api.route('/most/booked/cars')
def bar():
    data = requests.get("http://127.0.0.1:8080/bookings/get/bookings/data").json()
    return render_template('bar_chart.html', title='Most booked cars in minutes', max=15000, data=data["results"])

@graph_api.route('/profit/by/date')
def line():
    data = requests.get("http://127.0.0.1:8080/bookings/get/profit/data").json()
    return render_template('line_chart.html', title='Profit by date', max=1000, data=data["results"])

@graph_api.route('/most/repaired/cars')
def pie():
    pie_colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    data = requests.get("http://127.0.0.1:8080/backlogs/get/backlogs/data").json()
    return render_template('pie_chart.html', title='Most repaired cars', max=20, set=zip(data["results"], pie_colors))