from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
import requests
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.source.model.database import Database

from flaskr.auth import login_customer_required, login_admin_required, login_manager_required, login_engineer_required
from .forms import *
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
from datetime import *
import math
import re
import os

bp = Blueprint("blog", __name__)

#graph integration

def make_profit_line_chart():
    Database = get_db()
    labels = Database.select_record("DATE(RentTime) AS Date", "Bookings", " WHERE Status = 'Booked' GROUP BY DATE(RentTime)")
    values = Database.select_record("SUM(TotalCost) AS Daily_Profit", "Bookings", " WHERE Status = 'Booked' GROUP BY DATE(RentTime)")
    return Database.get_list_from_tuple_list(labels), Database.get_list_from_tuple_list(values)

def make_booked_car_bar_chart():
    Database = get_db()
    labels = Database.select_record("CarID", "Bookings", " WHERE Status = 'Booked' GROUP BY CarID")
    values = Database.select_record("SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)) as Booked_time", 
    "Bookings", " WHERE Status = 'Booked' GROUP BY CarID")
    return Database.get_list_from_tuple_list(labels), Database.get_list_from_tuple_list(values)

def make_backlog_pie_chart():
    Database = get_db()
    labels = Database.select_record("CarID", "Backlogs", " GROUP BY CarID")
    values = Database.select_record("COUNT(CarID) as Number_of_repairs", "Backlogs", " GROUP BY CarID")
    colors = ["#F7464A", "#46BFBD", "#FDB45C"]
    return Database.get_list_from_tuple_list(labels), Database.get_list_from_tuple_list(values), colors
    
@bp.route("/bar", methods=("GET", "POST"))
@login_required
def bar():
    if (g.user['UserType'] != "Manager"):
        return "Access Denied"
    bar_labels = make_booked_car_bar_chart()[0]
    bar_values = make_booked_car_bar_chart()[1]
    return render_template('bar_chart.html', title='Most booked cars in minutes', max=15000, labels=bar_labels, values=bar_values)

@bp.route("/line", methods=("GET", "POST"))
@login_required
def line():
    if (g.user['UserType'] != "Manager"):
        return "Access Denied"
    line_labels = make_profit_line_chart()[0]
    line_values = make_profit_line_chart()[1]
    return render_template('line_chart.html', title='Profit by date', max=1000, labels=line_labels, values=line_values)

@bp.route("/pie", methods=("GET", "POST"))
@login_required
def pie():
    if (g.user['UserType'] != "Manager"):
        return "Access Denied"
    pie_labels = make_backlog_pie_chart()[0]
    pie_values = make_backlog_pie_chart()[1]
    pie_colors = make_backlog_pie_chart()[2]
    return render_template('pie_chart.html', title='Most repaired cars', max=10, set=zip(pie_values, pie_labels, pie_colors))

# Some helper functions used by some API endpoints

def get_car(id, check_author=False):
    """Get a car by id.
    :raise 404: if a post with the given id doesn't exist
    """
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(id))).json()
    if car is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    return car
    
def get_booking(id, check_author=False):
    booking = (
        get_db()
        .execute(
            "SELECT id, Car, User, Created, Starttime, Endtime "
            " FROM Booking"
            " WHERE id = ?",
            (id,),
        )
        .fetchone()
    )

    if booking is None:
        abort(404, "Car id {0} doesn't exist.".format(id))

    return booking
 
def get_user(id, check_author=False):
    user = (
        get_db()
        .execute(
            "SELECT id, Created, UserName, Password, FirstName, LastName, Email, UserType "
            " FROM User"
            " WHERE id = ?",
            (id,),
        )
        .fetchone()
    )

    if user is None:
        abort(404, "User id {0} doesn't exist.".format(id))

    return user

#API endpoints begin here

@bp.route("/createadmin", methods=("GET", "POST"))
def createadmin():
    db = get_db()
    username = "admin"
    usertype = "Admin"
    password = "admin"
    firstname = "admin"
    lastname = "admin"
    email = "admin"
    db.execute(
    "INSERT INTO User (UserName, UserType, Password, FirstName, LastName, Email) VALUES (?, ?, ?, ?, ?, ?)",
    (username, usertype, generate_password_hash(password), firstname, lastname, email),
    )
    db.commit()
    return "done"


#This is the main page
@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
#redirect user types to their homepages
    if (g.user['UserType'] == "Admin"):
        return redirect(url_for("blog.admincars"))
    if (g.user['UserType'] == "Engineer"):
        return redirect(url_for("blog.engineercars"))
    if (g.user['UserType'] == "Manager"):
        return redirect(url_for("blog.manager"))
    form = carSearch()
    if request.method == "POST":
        cars = []
        make = '%' + request.form['make'] + '%'
        body = '%' + request.form['body'] + '%'
        colour = '%' + request.form['colour'] + '%'
        seats = '%' + request.form['seats'].strip() + '%'
        cost = request.form['cost'].strip()
        error = None
        if not cost:
            cost = 1000
        if cost:
            try:
                cost=float(cost)
            except: 
                error = "Cost must be a number"
                flash(error)
                datestart = ""
                dateend = ""
                cars = []
                return render_template("blog/index.html", form=form, cars=cars,datestart=datestart, dateend=dateend)
        try:
            datestart = request.form['start'].strip()
            datestart = datetime.strptime(datestart, '%Y-%m-%dT%H:%M')
        except: return "Start date required"
        try:
           dateend = request.form['end'].strip()
           dateend = datetime.strptime(dateend, '%Y-%m-%dT%H:%M')
        except: return "End date required"
        if (dateend - datestart).days < 0:
            error = "End date must be later than start date"
            flash(error)
            return render_template("blog/index.html", cars=cars, form=form)
        if error is not None:
            flash(error)
        else:   
            cars = requests.get("http://127.0.0.1:8080/cars/read?mac_address=&brand={}&car_type={}&status=Available&color={}&seat={}&cost={}&start={}&end={}"
            .format(str(make), str(body), str(colour), str(seats), str(cost), str(start_date), str(end_date))).json()
            # Results are displayed in this page
            return render_template("blog/index.html", cars=cars["car"], form=form, datestart=datestart, dateend=dateend)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        datestart = ""
        dateend = ""
        cars = []
        return render_template("blog/index.html", cars=cars, form=form, datestart=datestart, dateend=dateend)
        
        
#Users page (view only by admin)        
@bp.route("/adminusers", methods=("GET", "POST"))
@login_required
def adminusers():
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    form = userSearch()
    if request.method == "POST":
        username = '%' + request.form['username'].strip() + '%'
        usertype = '%' + request.form['usertype'].strip() + '%'
        first = '%' + request.form['first'].strip() + '%'
        last = '%' + request.form['last'].strip() + '%'
        email = '%' + request.form['email'].strip() + '%'
        error = None
        users = []
        users = requests.get("http://127.0.0.1:8080/customers/read?username={}&first_name={}&last_name={}&email={}&phone={}"
        .format(str(username), str(first), str(last), str(email), str(phone))).json()
        # all in the search box will return all the tuples
        return render_template("blog/adminusers.html", users=users, form=form)
    if request.method == "GET":
        users = requests.get("http://127.0.0.1:8080/customers/get/all/users").json()
       
        return render_template("blog/adminusers.html", users=users, form=form)
        
@bp.route("/admincars", methods=("GET", "POST"))
@login_required
def admincars():
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    form = adminCarSearch()
    if request.method == "POST":
        error = None
        cars=[]
        make = '%' + request.form['make'] + '%'
        body = '%' + request.form['body'] + '%'
        colour = '%' + request.form['colour'] + '%'
        seats = '%' + request.form['seats'].strip() + '%'
        cost =request.form['cost'].strip()
        location = '%' + request.form['location'].strip() + '%'
        status = '%' + request.form['status'].strip() + '%'
        if not cost:
            cost = 1000
        if cost:
            try:
                cost=float(cost)
            except: 
                error = "Cost must be a number"
                flash(error)
                cars = []
                return render_template("blog/admincars.html", form=form, cars=cars)
        cars = requests.get("http://127.0.0.1:8080/cars/read?mac_address=&brand={}&car_type={}&status={}&color={}&seat={}&cost={}&start=&end="
        .format(str(make), str(body), str(status), str(colour), str(seat), str(cost))).json()
        return render_template("blog/admincars.html", cars=cars, form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        cars = requests.get("http://127.0.0.1:8080/cars/read?mac_address=&brand=&car_type=&status&color=&seat=&cost=&start=&end=").json()
        # Results are displayed in this page
        #do I need these next 2 lines?
        #if form.validate_on_submit():
        #    return redirect(url_for('success'))
        return render_template("blog/admincars.html", cars=cars["car"], form=form)
        
@bp.route("/engineercars", methods=("GET", "POST"))
@login_required
def engineercars():
    if (g.user['UserType'] != "Engineer"):
        return "Access Denied"

    if request.method == "GET":
        cars = requests.get("http://127.0.0.1:8080/cars/read?mac_address=&brand=&car_type=&status&color=&seat=&cost=&start=&end=").json()
        # Results are displayed in this page
        return render_template("blog/engineercars.html", cars=cars["car"])


@bp.route("/<int:id>/location", methods=("GET", "POST"))
@login_required
def location(id):
    if (g.user['UserType'] != "Engineer"):
        return "Access Denied"
    car = get_car(id)
    return render_template("blog/location.html", car=car)

@bp.route("/<int:id>/carbookings", methods=("GET", "POST"))
@login_required
def carbookings(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    db = get_db()
    bookings = []
    error = None
    bookings = db.execute(
        "SELECT id, Car, User, Created, Starttime, Endtime FROM Booking WHERE Car = ? ORDER BY Created DESC",(id,)
    ).fetchall()
    return render_template("blog/carbookings.html", bookings=bookings, id=id)

@bp.route("/bookings", methods=("GET", "POST"))
@login_required
def bookings():
    user = g.user['id']
    form = bookingSearch()
    if request.method == "POST":
        bookings = []
        error = None
        try:
            start = request.form['start']
            start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        except: return "Start date required"
        if error is not None:
            flash(error)
        else:   
            bookings = requests.get("http://127.0.0.1:8080/bookings/get/customer/booking?start={}&id={}".format(str(start_date), g.user["ID"])).json()
        # Results are displayed in this page
        return render_template("blog/bookings.html", bookings=bookings["booking"], form=form)

    if request.method == "GET":
        bookings = requests.get("http://127.0.0.1:8080/bookings/get/customer/booking?start={}&id={}".format(str(start_date), g.user["ID"])).json()
        # Results are displayed in this page
        return render_template("blog/bookings.html", bookings=bookings["booking"], form=form)


# Cần bàn thêm
@bp.route("/<int:id>/deletebooking", methods=("GET", "POST"))
@login_required
def deletebooking(id):
    booking = get_booking(id)
    if (g.user['UserType'] != "Admin") and (int(g.user['id']) != int(booking['User'])):
        return "You cannot delete another user's booking unless you are logged in as an Admin"
    elif (int(g.user['id']) == int(booking['User'])) or (g.user['UserType'] == "Admin"):
        db = get_db()
        db.execute("DELETE FROM Booking WHERE id = ?", (id,))
        db.commit()
        return redirect(url_for("blog.bookings"))
    return "Unknown Error"
    
@bp.route("/edituser", methods=("GET", "POST"))
@login_required
def edituser():
    return redirect(url_for("blog.adminusers"))


#Create a new booking (Can only be done by customer)
@bp.route("/<int:ID>/<string:Start>/<string:End>/<int:UserID>/<int:Cost>/bookings/confirm/createBooking", methods=("GET", "POST"))
@login_customer_required
def createBooking(ID, Start, End, UserID, Cost):
    if g.type != "Customer":
        return redirect(url_for("blog.index"))
    requests.get("http://127.0.0.1:8080/bookings/create?customer_id={}&car_id={}&rent_time={}&return_time={}&total_cost={}"
    .format(str(UserID), str(ID), str(Start), str(End), str(Cost)))
    # Results are displayed in this page
    return redirect(url_for("blog.index"))


@bp.route("/<int:id>/createbooking", methods=("GET", "POST"))
@login_required
def createbooking(id):
    car = get_car(id)
    user = g.user['id']
    error = None
    try:
        datestart=request.args['datestart']
        datestart = datetime.strptime(datestart, '%Y-%m-%d %H:%M:%S')
    except: return "Start date required"
    try:
        dateend = request.args['dateend']
        dateend = datetime.strptime(dateend, '%Y-%m-%d %H:%M:%S')
    except: return "End date required"
    if (dateend - datestart).days < 0:
        error = "End date must be later than start date"
        form = carSearch()
        datestart = ""
        dateend = ""
        cars = []
        return render_template("blog/index.html", cars=cars, form=form, datestart=datestart, dateend=dateend)
    if error is not None:
        flash(error)
    else:
        datestart = datestart.strftime("%Y-%m-%d %H:%M")
        dateend = dateend.strftime("%Y-%m-%d %H:%M")
        #get cost from car id * total rent hours -> total cost
        requests.get("http://127.0.0.1:8080/bookings/create?customer_id={}&car_id={}&rent_time={}&return_time={}&total_cost=?"
        .format(str(user), str(car['id']), str(datestart), str(dateend))
        return redirect(url_for("blog.bookings"))

#Update a user (can only be done by customer)    
@bp.route("/<int:ID>/customer/update", methods=("GET", "POST"))
@login_customer_required
def editUser(ID):
    if g.type != "Customer":
        return redirect(url_for("blog.index"))
    user = requests.get("http://127.0.0.1:8080/customers/get/user/by/id?id={}".format(str(ID))).json()
    form = updateUserForm()
    if request.method == "POST":
        user_id = user["user"][0]["ID"]
        username = request.form["username"]
        password = request.form["password"]
        first = request.form["first"]
        last = request.form["last"]
        phone = request.form["phone"]
        email = request.form["email"]
        error = None
        if not username:
            error = "Username is required."
        if error is not None:
            flash(error)
        else:
            # This code will fill the API with the data collected from the form and then execute that API
            requests.get("http://127.0.0.1:8080/customers/update?id={}&username={}&password={}&first_name={}&last_name={}&email={}&phone={}"
            .format(str(user_id), str(username), str(password), str(first), str(last), str(email), str(phone)))
            return redirect(url_for("blog.adminusers"))
    # Results are displayed in this page
    return render_template("blog/update_user.html", user=user["user"], form=form)

@bp.route("/manager", methods=("GET", "POST"))
def manager():
    if request.method == "GET":
        try:
            graph = request.args["graph"]
        except: graph = "barchart"
        
        if graph == "barchart":
            return render_template("blog/bar_chart.html")
        elif graph == "linechart":
            return render_template("blog/line_chart.html")
        elif graph == "piechart":
            return render_template("blog/pie_chart.html")
        
        else:
            return "No graph of that type."

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    form=newCarForm()
    """Create a new car for the current user."""
    if request.method == "POST":
        mac_address = request.form["MAC"]
        make = request.form["make"].strip()
        body = request.form["body"].strip()
        colour = request.form["colour"].strip()
        seats = request.form["seats"].strip()
        location = request.form["location"].strip()
        cost = request.form["cost"].strip()
        error = None
        #input validation
        try:
            cost=float(cost)
        except: 
            error = "Cost must be a number"
            flash(error)
            return render_template("blog/create.html", form=form)
        if not make:
            error = "Make is required."
        elif not body:
            error = "Body is required."
        elif not colour:
            error = "Colour is required."
        elif not seats:
            error = "Seats is required."
        elif not location:
            error = "Location is required."
        elif not cost:
            error = "Cost is required."
        elif cost < 1 or cost > 1000:
            error = "Cost must be a number between 1 and 1000."
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO Car (make, body, colour, seats, location, cost) VALUES (?, ?, ?, ?, ?, ?)",
                (make, body, colour, seats, location, cost),
            )
            db.commit()
             # This code will fill the API with the data collected from the form and then execute that API
            requests.get("http://127.0.0.1:8080/cars/create?mac_address=?&brand={}&type={}&location_id={}&status=Available&color={}&seat={}&cost={}"
            .format(str(mac_address), str(make), str(body), str(location), str(colour), str(seats), str(cost)))
            return redirect(url_for("blog.admincars"))
        return render_template("blog/create.html", form=form)

    return render_template("blog/create.html", form=form)


@bp.route("/createuser", methods=("GET", "POST"))
@login_required
def createuser():
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    db = get_db()
    form=AdminUserForm()
    if request.method == "GET":
        render_template("blog/createuser.html", form=form)
    """Create a new car for the current user."""
    if request.method == "POST":
        username = request.form["username"].strip()
        usertype = request.form["usertype"].strip()
        firstname = request.form["firstname"].strip()
        lastname = request.form["lastname"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        valid_email = re.findall(r"[^@]+@[^@]+\.[^@]+",email)
        error = None
        if not username:
            error = "Username is required."
        if not usertype:
            error = "User type is required."
        elif not password:
            error = "Password is required."
        elif not firstname:
            error = "First name is required."
        elif not lastname:
            error = "Last name is required."
        elif not email:
            error = "Email is required."
        elif len(valid_email) < 1:
            error = "Incorrectly formatted email address"
        
        elif (
            db.execute("SELECT id FROM User WHERE UserName = ?", (username,)).fetchone()
            is not None
        ):
            error = "User {0} is already registered.".format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                "INSERT INTO User (UserName, UserType, Password, FirstName, LastName, Email) VALUES (?, ?, ?, ?, ?, ?)",
                (username, usertype, generate_password_hash(password), firstname, lastname, email),
            )
            db.commit()
            return redirect(url_for("blog.adminusers"))

        flash(error)

    return render_template("blog/createuser.html", form=form)


@bp.route("/<int:id>/updateuser", methods=("GET", "POST"))
@login_required
def updateuser(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    """Update a user."""
    user = get_user(id)
    form=AdminUserForm()
    if request.method == "GET":
        return render_template("blog/updateuser.html", user=user, form=form)
    if request.method == "POST":
        username = request.form["username"].strip()
        usertype = request.form["usertype"].strip()
        firstname = request.form["firstname"].strip()
        lastname = request.form["lastname"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        valid_email = re.findall(r"[^@]+@[^@]+\.[^@]+",email)
        error = None
        if not username:
            error = "Username is required."
        if not usertype:
            error = "User type is required."
        elif not password:
            error = "Password is required."
        elif not firstname:
            error = "First name is required."
        elif not lastname:
            error = "Last name is required."
        elif not email:
            error = "Email is required."
        elif len(valid_email) < 1:
            error = "Incorrectly formatted email address"

        if error is None:
            db = get_db()
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                "UPDATE User SET UserName = ?, UserType = ?, Password = ?, FirstName = ?, LastName = ?, Email = ? WHERE id = ?",
                (username, usertype, generate_password_hash(password), firstname, lastname, email, id),
            )
            db.commit()
            return redirect(url_for("blog.adminusers"))
        return render_template("blog/updateuser.html", user=user, form=form)
        
@bp.route("/<int:id>/deleteuser", methods=("GET", "POST"))
@login_required
def deleteuser(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"    
    user = get_user(id)
    db = get_db()
    db.execute("DELETE FROM User WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.adminusers"))

@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    """Update a car."""
    car = get_car(id)
    form=updateCarForm()
    if request.method == "POST":
        make = request.form["make"].strip()
        body = request.form["body"].strip()
        colour = request.form["colour"].strip()
        seats = request.form["seats"].strip()
        location = request.form["location"].strip()
        cost = request.form["cost"].strip()
        error = None
        
        #input validation
        try:
            cost=float(cost)
        except: 
            error = "Cost must be a number"
            flash(error)
            return render_template("blog/update.html", form=form, car=car)
        if not make:
            error = "Make is required."
        elif not body:
            error = "Body is required."
        elif not colour:
            error = "Colour is required."
        elif not seats:
            error = "Seats is required."
        elif not location:
            error = "Location is required."
        elif cost < 1 or cost > 1000:
            error = "Cost must be a number between 1 and 1000."
        elif not cost:
            error = "Cost is required."
        if error is not None:
            flash(error)
        else:
            # This code will fill the API with the data collected from the form and then execute that API
            requests.get("http://127.0.0.1:8080/cars/update?id={}&mac_address={}&brand={}&type={}&locationID=1&status={}&color={}&seat={}&cost={}"
            .format(str(car_id), str(mac_address), str(make), str(body), str(status), str(colour), str(seats), str(cost)))
            return redirect(url_for("blog.admincars"))
        return render_template("blog/update.html", car=car["car"], form=form)
    return render_template("blog/update.html", car=car["car"], form=form)

@bp.route("/<int:id>/confirm", methods=("GET", "POST"))
@login_required
def confirm(id):
    """Update a car if the current user is the author."""
    car = get_car(id)
    error = None
    try:
        datestart=request.args['datestart']
        datestart = datetime.strptime(datestart, '%Y-%m-%d %H:%M:%S')
    except: return "Start time required"
    try:
        dateend = request.args['dateend']
        dateend = datetime.strptime(dateend, '%Y-%m-%d %H:%M:%S')
    except: return "End date required"
    if (dateend - datestart).days < 0:
        error = "End date must be later than start date"
        form = carSearch()
        datestart = ""
        dateend = ""
        cars = []
        return render_template("blog/index.html", cars=cars, form=form, datestart=datestart, dateend=dateend)
    if error is not None:
            flash(error)
    else:
        cost = math.ceil((dateend - datestart).total_seconds()/3600) * car['cost']
        return render_template("blog/confirm.html", car=car,datestart=datestart,dateend=dateend, total_cost=cost)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    """Delete a car.

    Ensures that the car exists and that the logged in user is the
    author of the car.
    """
    get_car(id)
    db = get_db()
    db.execute("DELETE FROM Car WHERE id = ?", (id,))
    db.commit()
        if error is not None:
            flash(error)
        else:
            # This code will fill the API with the data collected from the form and then execute that API
            requests.get("http://127.0.0.1:8080/cars/create?mac_address={}&brand={}&type={}&location_id={}&status=Available&color={}&seat={}&cost={}"
            .format(str(mac_address), str(make), str(body), str(location), str(colour), str(seats), str(cost)))
            return redirect(url_for("blog.admincars"))
    # Results are displayed in this page
    return render_template("blog/create.html", form=form)

#Update cars (can only be done by admin)
@bp.route("/<int:ID>/admincars/update", methods=("GET", "POST"))
@login_admin_required
def editCar(ID):
    if g.type != "Admin":
        return redirect(url_for("blog.index"))
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    form=updateCarForm()
    if request.method == "POST":
        car_id = car["car"][0]["ID"]
        mac_address = request.form["mac_address"]
        make = request.form["make"]
        body = request.form["body"]
        colour = request.form["colour"]
        seats = request.form["seats"]
        cost = request.form["cost"]
        status = request.form["status"]
        error = None
        # placeholder for input validation
        if not make:
            error = "Make is required."
        if error is not None:
            flash(error)
        else:
            # This code will fill the API with the data collected from the form and then execute that API
            requests.get("http://127.0.0.1:8080/cars/update?id={}&mac_address={}&brand={}&type={}&locationID=1&status={}&color={}&seat={}&cost={}"
            .format(str(car_id), str(mac_address), str(make), str(body), str(status), str(colour), str(seats), str(cost)))
            return redirect(url_for("blog.admincars"))
    # Results are displayed in this page
    return render_template("blog/update.html", car=car["car"], form=form)

#Confirm booking (can only be done by customer)
@bp.route("/<int:ID>/bookings/confirm", methods=("GET", "POST"))
@login_customer_required
def confirm(ID):
    if g.type != "Customer":
        return redirect(url_for("blog.index"))
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    datestart=request.args['datestart']
    dateend=request.args['dateend']
    start_date = datetime.strptime(datestart, '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(dateend, '%Y-%m-%dT%H:%M')
    total = int((end_date - start_date).total_seconds() / 3600) * car["car"][0]["Cost"]
    # Results are displayed in this page
    return render_template("blog/confirm.html", car=car["car"],datestart=datestart,dateend=dateend,total=total)

#Delete a car (can only be done by admin)
@bp.route("/<int:ID>/admincars/update/delete", methods=("POST",))
@login_admin_required
def delete(ID):
    if g.type != "Admin":
        return redirect(url_for("blog.index"))
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    requests.get("http://127.0.0.1:8080/cars/delete?id={}".format(str(car["car"][0]["ID"])))
    return redirect(url_for("blog.admincars"))
    
#Repair a car (can only be done by admin)   
@bp.route("/<int:ID>/engineercars/repair", methods=("POST",))
@login_engineer_required
def repair(ID):
    if g.type != "Engineer":
        return redirect(url_for("blog.index"))
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    requests.get("http://127.0.0.1:8080/backlogs/fix/car?car_id={}".format(str(car["car"][0]["ID"])))
    return redirect(url_for("blog.engineercars"))
    
@bp.route("/<int:id>/repair", methods=("POST",))
@login_required
def repair(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    get_car(id)
   # mail = send_mail(str(id))
    #mail.send()
    db = get_db()
    db.execute(
            "UPDATE Car SET Status = 'Repair' WHERE id = ?", (id,)
            )
    db.commit()
    return redirect(url_for("blog.admincars"))
    
@bp.route("/<int:id>/fix", methods=("POST",))
@login_required
def fix(id):
    if (g.user['UserType'] != "Engineer"):
        return "Access Denied"
    get_car(id)
    db = get_db()
    db.execute(
            "UPDATE Car SET status = 'Available' WHERE id = ?", (id,)
            )
    db.commit()
    return redirect(url_for("blog.engineercars"))
    
@bp.route("/<int:id>/sendmail", methods=("GET",))
@login_required
def sendmail(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"   
    car = get_car(id) 
    # Mail Sending integration goes here
    #
    #
    return redirect(url_for("blog.admincars"))
    
@bp.route("/<int:id>/calendar", methods=("GET",))
@login_required
def calendar(id):
    user = get_user(g.user['id'])
    booking = get_booking(id)
    # Calendar Sending integration goes here
    #
    #
    return redirect(url_for("blog.index"))
    
#Report a car (can only be done by admin)  
@bp.route("/<int:ID>/admincars/update/report", methods=("GET", "POST"))
@login_admin_required
def report(ID):
    if g.type != "Admin":
        return redirect(url_for("blog.index"))
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    form=newBacklogForm()
    if request.method == "POST":
        car_id = car["car"][0]["ID"]
        engineer_ID = request.form["engineer_ID"]
        date = request.form["date"]
        new_date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        error = None
        if not engineer_ID:
            error = "Engineer is required."
        if error is not None:
            flash(error)
        else:
            # This code will fill the API with the data collected from the form and then execute that API
            requests.get("http://127.0.0.1:8080/backlogs/create?assigned_engineer_id={}&car_id={}&created_date={}&status=Not%20done&description="
            .format(str(engineer_ID), str(car_id), str(new_date)))
            return redirect(url_for("blog.admincars"))
    # Results are displayed in this page
    return render_template("blog/backlog.html", form=form)

#Cancel booking (Can only be done by customer)    
@bp.route("/<int:ID>/bookings/cancel", methods=("POST",))
@login_customer_required
def cancel_booking(ID):
    if g.type != "Customer":
        return redirect(url_for("blog.index"))
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    requests.get("http://127.0.0.1:8080/bookings/update?status=Cancelled&id={}".format(str(car["car"][0]["ID"])))
    return redirect(url_for("blog.customer_bookings"))

#View car's rental history (can only be done by admin)
@bp.route("/<int:ID>/admincars/history", methods=("GET",))
@login_admin_required
def get_history(ID):
    if g.type != "Admin":
        return redirect(url_for("blog.index"))
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    history = requests.get("http://127.0.0.1:8080/cars/history?id={}".format(str(car["car"][0]["ID"]))).json()
    return render_template("blog/history.html", history=history["history"])

@bp.route("/manager", methods=("GET",))
@login_manager_required
def get_graphs():
    if g.type != "Manager":
        return redirect(url_for("blog.index"))
    if request.method == "GET":
        return render_template("blog/manager.html")


