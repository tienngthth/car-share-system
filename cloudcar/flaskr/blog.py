from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
import requests
from flask import url_for
from werkzeug.exceptions import abort
from flaskr.source.model.database import Database

from flaskr.auth import login_required
from .forms import *
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
bp = Blueprint("blog", __name__)

#DONE
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

#DONE
@bp.route("/", methods=("GET", "POST"))
def index():
    form = carSearch()
    if request.method == "POST":
        make = request.form['make']
        colour = request.form['colour']
        datestart = request.form['start']
        dateend = request.form['end']
        # search form
        cars = requests.get("http://127.0.0.1:8080/cars/index/get/car?brand={}&color={}".format(str(make), str(colour))).json()
        return render_template("blog/index.html", cars=cars["car"], form=form, datestart=datestart, dateend=dateend)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        datestart = ""
        dateend = ""
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/index.html", form=form, datestart=datestart, dateend=dateend)
        
#DONE        
@bp.route("/adminusers", methods=("GET", "POST"))
def adminusers():
    form = userSearch()
    if request.method == "POST":
        username = request.form['username']
        # search form
        users = requests.get("http://127.0.0.1:8080/customers/read?username={}&first_name=&last_name=&email=&phone=".format(str(username))).json()
        return render_template("blog/adminusers.html", users=users["results"], form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        users = requests.get("http://127.0.0.1:8080/customers/get/all/users").json()
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/adminusers.html", users=users["user"], form=form)
        
        
#DONE        
@bp.route("/admincars", methods=("GET", "POST"))
def admincars():
    form = adminCarSearch()
    if request.method == "POST":
        make = request.form['make']
        colour = request.form['colour']
        # search form
        cars = requests.get("http://127.0.0.1:8080/cars/admin/search/car?brand={}&color={}".format(str(make), str(colour))).json()
        return render_template("blog/admincars.html", cars=cars["car"], form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        cars = requests.get("http://127.0.0.1:8080/cars/admin/get/all/cars").json()
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/admincars.html", cars=cars["car"], form=form)

#DONE        
@bp.route("/engineercars", methods=("GET", "POST"))
def engineercars():
    if request.method == "GET":
        cars = requests.get("http://127.0.0.1:8080/backlogs/engineer/get/cars").json()
        #do I need these next 2 lines?
        return render_template("blog/engineercars.html", cars=cars["car"])


#DONE
@bp.route("/bookings", methods=("GET", "POST"))
def bookings():
    form = bookingSearch()
    if request.method == "POST":
        start = request.form['start']
        end =  request.form['end']
        start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(end, '%Y-%m-%dT%H:%M')
        # search date only
        bookings = requests.get("http://127.0.0.1:8080/bookings/get/booking?start={}&end={}".format(str(start_date), str(end_date))).json()
        return render_template("blog/bookings.html", bookings=bookings["booking"], form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        bookings = requests.get("http://127.0.0.1:8080/bookings/get/all/bookings").json()
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/bookings.html", bookings=bookings["booking"], form=form)



@bp.route("/updateBooking", methods=("GET", "POST"))
@login_required
def updateBooking():
   

    return redirect(url_for("blog.index"))
    
@bp.route("/edituser", methods=("GET", "POST"))
@login_required
def edituser():
   

    return redirect(url_for("blog.adminusers"))

#DONE
@bp.route("/create", methods=("GET", "POST"))
def create():
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
            requests.get("http://127.0.0.1:8080/cars/create?mac_address={}&brand={}&type={}&location_id={}&status=Available&color={}&seat={}&cost={}"
            .format(str(mac_address), str(make), str(body), str(location), str(colour), str(seats), str(cost)))
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html", form=form)

#DONE
@bp.route("/<int:ID>/update", methods=("GET", "POST"))
def update(ID):
    """Update a car if the current user is the author."""
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
            requests.get("http://127.0.0.1:8080/cars/update?id={}&mac_address={}&brand={}&type={}&locationID=1&status={}&color={}&seat={}&cost={}"
            .format(str(car_id), str(mac_address), str(make), str(body), str(status), str(colour), str(seats), str(cost)))
            return redirect(url_for("blog.admincars"))
    return render_template("blog/update.html", car=car["car"], form=form)

#DONE
@bp.route("/<int:ID>/confirm", methods=("GET", "POST"))
def confirm(ID):
    """Update a car if the current user is the author."""
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    datestart=request.args['datestart']
    dateend=request.args['dateend']
    start_date = datetime.strptime(datestart, '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(dateend, '%Y-%m-%dT%H:%M')
    total = int((end_date - start_date).total_seconds() / 3600) * car["car"][0]["Cost"]
    return render_template("blog/confirm.html", car=car["car"],datestart=datestart,dateend=dateend,total=total)

#DONE
@bp.route("/<int:ID>/delete", methods=("POST",))
def delete(ID):
    """Delete a car.
    Ensures that the car exists and that the logged in user is the
    author of the car.
    """
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    requests.get("http://127.0.0.1:8080/cars/delete?id={}".format(str(car["car"][0]["ID"])))
    return redirect(url_for("blog.index"))
    
#DONE    
@bp.route("/<int:ID>/repair", methods=("POST",))
def repair(ID):
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(ID))).json()
    requests.get("http://127.0.0.1:8080/backlogs/fix/car?car_id={}".format(str(car["car"][0]["ID"])))
    return redirect(url_for("blog.engineercars"))
    
#DONE    
@bp.route("/<int:ID>/report", methods=("GET", "POST"))
def report(ID):
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
            requests.get("http://127.0.0.1:8080/backlogs/create?assigned_engineer_id={}&car_id={}&created_date={}&status=Not%20done&description="
            .format(str(engineer_ID), str(car_id), str(new_date)))
            return redirect(url_for("blog.admincars"))
    return render_template("blog/backlog.html", form=form)