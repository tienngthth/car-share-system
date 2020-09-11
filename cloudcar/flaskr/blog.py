from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
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
    car = Database.select_record("*", 
                                 "Cars",
                                 " WHERE Cars.ID = " + str(id))
    if car is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return car

#DONE
@bp.route("/", methods=("GET", "POST"))
def index():
    form = carSearch()
    if request.method == "POST":
        make = '%' + request.form['make'] + '%'
        colour = '%' + request.form['colour'] + '%'
        datestart = request.form['start']
        dateend = request.form['end']
        # search form
        cars = Database.select_record("Cars.ID, Cars.Brand, Cars.Type, Cars.Color, Cars.Seat, Locations.Address, Cars.Cost", 
                                      "Cars INNER JOIN Locations ON Cars.LocationID = Locations.ID", 
                                      " WHERE Brand LIKE '" + make + "' AND Color LIKE '" + colour + "'")
        # all in the search box will return all the tuples
        return render_template("blog/index.html", cars=cars, form=form, datestart=datestart, dateend=dateend)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        datestart = ""
        dateend = ""
        cars = []
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/index.html", cars=cars, form=form, datestart=datestart, dateend=dateend)
        
#DONE        
@bp.route("/adminusers", methods=("GET", "POST"))
def adminusers():
    form = userSearch()
    if request.method == "POST":
        username = '%' + request.form['username'] + '%'
        # search form
        users = Database.select_record("*", "Customers", " WHERE Username LIKE '" + username + "' ORDER BY Username DESC")
        # all in the search box will return all the tuples
        return render_template("blog/adminusers.html", users=users, form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        users = Database.select_record("*", "Customers", " ORDER BY Username DESC")
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/adminusers.html", users=users, form=form)
        
        
#DONE        
@bp.route("/admincars", methods=("GET", "POST"))
def admincars():
    form = adminCarSearch()
    if request.method == "POST":
        make = '%' + request.form['make'] + '%'
        colour = '%' + request.form['colour'] + '%'
        # search form
        cars = Database.select_record("Cars.ID, Cars.Brand, Cars.Color, Locations.Address, Bookings.Status",
                                      "Cars LEFT JOIN Bookings ON Cars.ID = Bookings.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID",
                                      " WHERE Cars.Brand LIKE '" + make + "' AND Cars.Color LIKE '" + colour + "' ORDER BY Bookings.RentTime DESC")
        # all in the search box will return all the tuples
        return render_template("blog/admincars.html", cars=cars, form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        cars = Database.select_record("Cars.ID, Cars.Brand, Cars.Color, Locations.Address, Bookings.Status",
                                      "Cars LEFT JOIN Bookings ON Cars.ID = Bookings.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID",
                                      " ORDER BY Bookings.RentTime DESC")
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/admincars.html", cars=cars, form=form)

#DONE        
@bp.route("/engineercars", methods=("GET", "POST"))
def engineercars():
    if request.method == "GET":
        cars = Database.select_record("Cars.ID, Locations.Address, Backlogs.Date, Backlogs.Status", 
                                 "Cars INNER JOIN Backlogs ON Cars.ID = Backlogs.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID",
                                 "")
        #do I need these next 2 lines?
        return render_template("blog/engineercars.html", cars=cars)


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
        bookings = Database.select_record("Bookings.RentTime, Bookings.CarID, Cars.Brand, Cars.Color, TIMESTAMPDIFF(HOUR,Bookings.RentTime,Bookings.ReturnTime) AS Duration, Bookings.Status, Bookings.ID", 
                                                   "Cars INNER JOIN Bookings ON Cars.ID = Bookings.ID", 
                                                   " WHERE Bookings.RentTime > '" + str(start_date) + "' AND Bookings.RentTime < '" + str(end_date) + "'")
        # all in the search box will return all the tuples
        return render_template("blog/bookings.html", bookings=bookings, form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        bookings = Database.select_record("Bookings.RentTime, Bookings.CarID, Cars.Brand, Cars.Color, TIMESTAMPDIFF(HOUR,Bookings.RentTime,Bookings.ReturnTime) AS Duration, Bookings.Status, Bookings.ID", 
                                                   "Cars INNER JOIN Bookings ON Cars.ID = Bookings.ID", 
                                                   "")
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/bookings.html", bookings=bookings, form=form)



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
            Database.insert_record_parameterized(
                "Cars(MacAddress, Brand, Type, LocationID, Status, Color, Seat, Cost) ",
                "(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    mac_address,
                    make,
                    body,
                    location,
                    "Available",
                    colour,
                    seats,
                    cost,
                )
            )
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html", form=form)

#DONE
@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    """Update a car if the current user is the author."""
    car = get_car(id)[0]
    form=updateCarForm()
    if request.method == "POST":
        car_id = car[0]
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
            Database.update_record_parameterized(
                "Cars",
                " MacAddress = CASE WHEN %(mac_address)s = '' OR %(mac_address)s IS NULL " +
                " THEN MacAddress ELSE %(mac_address)s END, " +
                " Brand = CASE WHEN %(brand)s = '' OR %(brand)s IS NULL " +
                " THEN Brand ELSE %(brand)s END, " +
                " Type = CASE WHEN %(type)s = '' OR %(type)s IS NULL " + 
                " THEN Type ELSE %(type)s END, " +
                " Status = CASE WHEN %(status)s = '' OR %(status)s IS NULL " + 
                " THEN Status ELSE %(status)s END, " +
                " Color = CASE WHEN %(color)s = '' OR %(color)s IS NULL " + 
                " THEN Color ELSE %(color)s END, " +
                " Seat = CASE WHEN %(seat)s = '' OR %(seat)s IS NULL " + 
                " THEN Seat ELSE %(seat)s END, " +
                " Cost = CASE WHEN %(cost)s = '' OR %(cost)s IS NULL " + 
                " THEN Cost ELSE %(cost)s END ",
                " WHERE ID = %(car_id)s", 
                {
                    "car_id": car_id,
                    "mac_address": mac_address, 
                    "brand": make, 
                    "type": body,
                    "status": status,
                    "color": colour,
                    "seat": seats,
                    "cost": cost
                }
            )
            return redirect(url_for("blog.index"))
    return render_template("blog/update.html", car=car, form=form)

#DONE
@bp.route("/<int:id>/confirm", methods=("GET", "POST"))
def confirm(id):
    """Update a car if the current user is the author."""
    car = get_car(id)[0]
    datestart=request.args['datestart']
    dateend=request.args['dateend']
    start_date = datetime.strptime(datestart, '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(dateend, '%Y-%m-%dT%H:%M')
    total = int((end_date - start_date).total_seconds() / 3600) * car[8]
    return render_template("blog/confirm.html", car=car,datestart=datestart,dateend=dateend,total=total)

#DONE
@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    """Delete a car.
    Ensures that the car exists and that the logged in user is the
    author of the car.
    """
    car = get_car(id)[0]
    Database.delete_record_parameterized(
        "Cars",
        " WHERE ID = %s",
         car[0],
    )
    return redirect(url_for("blog.index"))
    
#DONE    
@bp.route("/<int:id>/repair", methods=("POST",))
def repair(id):
    car = get_car(id)[0]
    Database.update_record_parameterized(
        "Backlogs", 
        " Status = 'Done'",
        " WHERE CarID = (%s) AND Status = 'Not done' ",
        car[0]
    ) 
    return redirect(url_for("blog.engineercars"))
    
#DONE    
@bp.route("/<int:id>/report", methods=("GET", "POST"))
def report(id):
    car = get_car(id)[0]
    form=newBacklogForm()
    if request.method == "POST":
        car_id = car[0]
        engineer_ID = request.form["engineer_ID"]
        date = request.form["date"]
        new_date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        error = None
        if not engineer_ID:
            error = "Engineer is required."
        if error is not None:
            flash(error)
        else:
            Database.insert_record_parameterized(
                "Backlogs(AssignedEngineerID, SignedEngineerID, CarID, Date, Status, Description) ",
                "(%s, %s, %s, %s, %s, %s)",
                (
                    engineer_ID,
                    None,
                    car_id,
                    new_date,
                    "Not done",
                    ""
                )
            )
            return redirect(url_for("blog.admincars"))
    return render_template("blog/backlog.html", form=form)