from flask import Blueprint, Flask, Markup, render_template
from model.database import Database

graph_api = Blueprint("graph_api", __name__)

def make_profit_line_chart():
    labels = Database.select_record("DATE(RentTime) AS Date", "Bookings", " WHERE Status = 'Booked' GROUP BY DATE(RentTime)")
    values = Database.select_record("SUM(TotalCost) AS Daily_Profit", "Bookings", " WHERE Status = 'Booked' GROUP BY DATE(RentTime)")
    return Database.get_list_from_tuple_list(labels), Database.get_list_from_tuple_list(values)

def make_booked_car_bar_chart():
    labels = Database.select_record("CarID", "Bookings", " WHERE Status = 'Booked' GROUP BY CarID")
    values = Database.select_record("SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)) as Booked_time", 
    "Bookings", " WHERE Status = 'Booked' GROUP BY CarID")
    return Database.get_list_from_tuple_list(labels), Database.get_list_from_tuple_list(values)

def make_backlog_pie_chart():
    labels = Database.select_record("CarID", "Backlogs", " GROUP BY CarID")
    values = Database.select_record("COUNT(CarID) as Number_of_repairs", "Backlogs", " GROUP BY CarID")
    colors = ["#F7464A", "#46BFBD", "#FDB45C"]
    return Database.get_list_from_tuple_list(labels), Database.get_list_from_tuple_list(values), colors

@graph_api.route('/most/booked/cars')
def bar():
    bar_labels = make_booked_car_bar_chart()[0]
    bar_values = make_booked_car_bar_chart()[1]
    return render_template('bar_chart.html', title='Most booked cars in minutes', max=15000, labels=bar_labels, values=bar_values)

@graph_api.route('/profit/by/date')
def line():
    line_labels = make_profit_line_chart()[0]
    line_values = make_profit_line_chart()[1]
    return render_template('line_chart.html', title='Profit by date', max=1000, labels=line_labels, values=line_values)

@graph_api.route('/most/repaired/cars')
def pie():
    pie_labels = make_backlog_pie_chart()[0]
    pie_values = make_backlog_pie_chart()[1]
    pie_colors = make_backlog_pie_chart()[2]
    return render_template('pie_chart.html', title='Most repaired cars', max=10, set=zip(pie_values, pie_labels, pie_colors))