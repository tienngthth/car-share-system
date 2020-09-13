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
from flaskr.source.model.database import Database

from flaskr.auth import login_customer_required, login_admin_required, login_manager_required, login_engineer_required
from .forms import *
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
bp = Blueprint("blog", __name__)

#This function gets the car by ID
def get_car(id):
    """Get a car and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(id))).json()
    if car is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    return car

#This is the main page
@bp.route("/", methods=("GET", "POST"))
def index():
    form = carSearch()
    if request.method == "POST":
        make = request.form['make']
        body = request.form['body']
        colour = request.form['colour']
        seats = request.form['seats']
        cost = request.form['cost']
        datestart = request.form['start']
        dateend = request.form['end']
        start_date = datetime.strptime(datestart, '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(dateend, '%Y-%m-%dT%H:%M')
        # This code will fill the API with the data collected from the form and then execute that API
        cars = requests.get("http://127.0.0.1:8080/cars/read?mac_address=&brand={}&car_type={}&status=Available&color={}&seat={}&cost={}&start={}&end={}"
        .format(str(make), str(body), str(colour), str(seats), str(cost), str(start_date), str(end_date))).json()
        # Results are displayed in this page
        return render_template("blog/index.html", cars=cars["car"], form=form, datestart=datestart, dateend=dateend)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        datestart = ""
        dateend = ""
        # Results are displayed in this page
        return render_template("blog/index.html", form=form, datestart=datestart, dateend=dateend)
        
#Users page (view only by admin)        
@bp.route("/adminusers", methods=("GET", "POST"))
@login_admin_required
def adminusers():
    if g.type != "Admin":
        return redirect(url_for("blog.index"))
    form = userSearch()
    if request.method == "POST":
        username = request.form['username']
        first = request.form['first']
        last = request.form['last']
        email = request.form['email']
        phone = request.form['phone']
        # This code will fill the API with the data collected from the form and then execute that API
        users = requests.get("http://127.0.0.1:8080/customers/read?username={}&first_name={}&last_name={}&email={}&phone={}"
        .format(str(username), str(first), str(last), str(email), str(phone))).json()
        # Results are displayed in this page
        return render_template("blog/adminusers.html", users=users["results"], form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        users = requests.get("http://127.0.0.1:8080/customers/get/all/users").json()
        # Results are displayed in this page
        return render_template("blog/adminusers.html", users=users["user"], form=form)
        
        
#Cars page (View only by admin)       
@bp.route("/admincars", methods=("GET", "POST"))
@login_admin_required
def admincars():
    if g.type != "Admin":
        return redirect(url_for("blog.index"))
    form = adminCarSearch()
    if request.method == "POST":
        make = request.form['make']
        body = request.form['body']
        colour = request.form['colour']
        seat = request.form['seats']
        cost = request.form['cost']
        status = request.form['status']
        # This code will fill the API with the data collected from the form and then execute that API
        cars = requests.get("http://127.0.0.1:8080/cars/read?mac_address=&brand={}&car_type={}&status={}&color={}&seat={}&cost={}&start=&end="
        .format(str(make), str(body), str(status), str(colour), str(seat), str(cost))).json()
        # Results are displayed in this page
        return render_template("blog/admincars.html", cars=cars["car"], form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        cars = requests.get("http://127.0.0.1:8080/cars/read?mac_address=&brand=&car_type=&status&color=&seat=&cost=&start=&end=").json()
        # Results are displayed in this page
        return render_template("blog/admincars.html", cars=cars["car"], form=form)

#Backlogs page (view only by engineers)       
@bp.route("/engineercars", methods=("GET", "POST"))
@login_engineer_required
def engineercars():
    if g.type != "Engineer":
        return redirect(url_for("blog.index"))
    if request.method == "GET":
        cars = requests.get("http://127.0.0.1:8080/backlogs/engineer/get/cars").json()
        # Results are displayed in this page
        return render_template("blog/engineercars.html", cars=cars["car"])

#Customer's booking history
@bp.route("/customer/bookings", methods=("GET", "POST"))
@login_customer_required
def customer_bookings():
    if g.type != "Customer":
        return redirect(url_for("blog.index"))
    form = bookingSearch()
    if request.method == "POST":
        start = request.form['start']
        start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        # This code will fill the API with the data collected from the form and then execute that API
        bookings = requests.get("http://127.0.0.1:8080/bookings/get/customer/booking?start={}&id={}".format(str(start_date), g.user["ID"])).json()
        # Results are displayed in this page
        return render_template("blog/bookings.html", bookings=bookings["booking"], form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        bookings = requests.get("http://127.0.0.1:8080/bookings/get/all/customer/bookings?id={}".format(g.user["ID"])).json()
        # Results are displayed in this page
        return render_template("blog/bookings.html", bookings=bookings["booking"], form=form)

#Admin's booking history
@bp.route("/admin/bookings", methods=("GET", "POST"))
@login_admin_required
def admin_bookings():
    if g.type != "Admin":
        return redirect(url_for("blog.index"))
    form = bookingSearch()
    if request.method == "POST":
        start = request.form['start']
        start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        # This code will fill the API with the data collected from the form and then execute that API
        bookings = requests.get("http://127.0.0.1:8080/bookings/get/admin/booking?start={}".format(str(start_date))).json()
        # Results are displayed in this page
        return render_template("blog/bookings.html", bookings=bookings["booking"], form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        bookings = requests.get("http://127.0.0.1:8080/bookings/get/all/admin/bookings").json()
        # Results are displayed in this page
        return render_template("blog/bookings.html", bookings=bookings["booking"], form=form)

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

#Add a new car (can only be done by admin)
@bp.route("/admincars/create", methods=("GET", "POST"))
@login_admin_required
def create():
    if g.type != "Admin":
        return redirect(url_for("blog.index"))
    form=newCarForm()
    """Create a new car for the current user."""
    if request.method == "POST":
        mac_address = request.form["mac_address"]
        make = request.form["make"]
        body = request.form["body"]
        colour = request.form["colour"]
        seats = request.form["seats"]
        location = request.form["location"]
        cost = request.form["cost"]
        error = None
#placeholder for input validation
        if not make:
            error = "Make is required."
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


