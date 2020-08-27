from flask import Flask, Markup, render_template
import connect

app = Flask(__name__)
connection = connect.connect_to_database()
cursor = connection.cursor()

def make_profit_line_chart(cursor):
    labels = []
    values = []
    cursor.execute("SELECT DATE(RentTime) AS Date FROM Bookings GROUP BY DATE(RentTime)")
    for Date in cursor:
        labels.append(Date[0])

    cursor.execute("SELECT SUM(TotalCost) AS Daily_Profit FROM Bookings GROUP BY DATE(RentTime)")
    for Daily_profit in cursor:
        values.append(Daily_profit[0])

    return labels, values

def make_booked_car_bar_chart(cursor):
    labels = []
    values = []
    cursor.execute("SELECT CarID FROM Bookings GROUP BY CarID")
    for CarID in cursor:
        labels.append(CarID[0])

    cursor.execute("SELECT SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)) as Booked_time FROM Bookings GROUP BY CarID")
    for Booked_time in cursor:
        values.append(Booked_time[0])

    return labels, values

def make_backlog_pie_chart(cursor):
    labels = []
    values = []
    cursor.execute("SELECT CarID FROM Backlogs GROUP BY CarID")
    for CarID in cursor:
        labels.append(CarID[0])

    cursor.execute("SELECT COUNT(CarID) as Number_of_repairs FROM Backlogs GROUP BY CarID")
    for Number_of_repairs in cursor:
        values.append(Number_of_repairs[0])

    colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    return labels, values, colors

@app.route('/bar')
def bar():
    bar_labels = make_booked_car_bar_chart(cursor)[0]
    bar_values = make_booked_car_bar_chart(cursor)[1]
    return render_template('bar_chart.html', title='Most booked cars in minutes', max=15000, labels=bar_labels, values=bar_values)

@app.route('/line')
def line():
    line_labels = make_profit_line_chart(cursor)[0]
    line_values = make_profit_line_chart(cursor)[1]
    return render_template('line_chart.html', title='Profit by date', max=1000, labels=line_labels, values=line_values)

@app.route('/pie')
def pie():
    pie_labels = make_backlog_pie_chart(cursor)[0]
    pie_values = make_backlog_pie_chart(cursor)[1]
    pie_colors = make_backlog_pie_chart(cursor)[2]
    return render_template('pie_chart.html', title='Most repaired cars', max=10, set=zip(pie_values, pie_labels, pie_colors))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)