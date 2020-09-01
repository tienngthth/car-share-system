from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from .forms import *
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
bp = Blueprint("blog", __name__)

def get_car(id, check_author=True):
    """Get a car and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    car = (
        get_db()
        .execute(
            "SELECT p.id, make, body, colour, seats, location, cost, status, author_id "
            " FROM cars p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if car is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return car

@bp.route("/", methods=("GET", "POST"))
def index():
    form = carSearch()
    db = get_db()
    if request.method == "POST":
        make = '%' + request.form['make'] + '%'
        colour = '%' + request.form['colour'] + '%'
        datestart = request.form['start']
        dateend = request.form['end']
        # search form
        cars = db.execute(
            "SELECT id, make, body, colour, seats, location, cost FROM cars WHERE make LIKE ? AND colour LIKE ? ORDER BY created DESC",(make,colour,)
        ).fetchall()
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
        
        
@bp.route("/adminusers", methods=("GET", "POST"))
def adminusers():
    form = userSearch()
    db = get_db()
    if request.method == "POST":
        username = '%' + request.form['username'] + '%'
        # search form
        users = db.execute(
            "SELECT id, username FROM user WHERE username LIKE ? ORDER BY username DESC",(username,)
        ).fetchall()
        # all in the search box will return all the tuples
        return render_template("blog/adminusers.html", users=users, form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        users = db.execute(
            "SELECT id, username"
            " FROM user "
            " ORDER BY username DESC"
        ).fetchall()
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/adminusers.html", users=users, form=form)
        
        
        
@bp.route("/admincars", methods=("GET", "POST"))
def admincars():
    form = adminCarSearch()
    db = get_db()
    if request.method == "POST":
        make = '%' + request.form['make'] + '%'
        colour = '%' + request.form['colour'] + '%'
        # search form
        cars = db.execute(
            "SELECT id, make, body, colour, seats, location, cost, status, author_id FROM cars WHERE make LIKE ? AND colour LIKE ? ORDER BY created DESC",(make,colour,)
        ).fetchall()
        # all in the search box will return all the tuples
        return render_template("blog/admincars.html", cars=cars, form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        cars = db.execute(
            "SELECT p.id, make, body, colour, seats, location, status, cost, created, author_id, username"
            " FROM cars p JOIN user u ON p.author_id = u.id"
            " ORDER BY created DESC"
        ).fetchall()
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/admincars.html", cars=cars, form=form)



@bp.route("/bookings", methods=("GET", "POST"))
@login_required
def bookings():
    form = bookingSearch()
    db = get_db()
    if request.method == "POST":
        start = '%' + request.form['start'] + '%'
        end = '%' + request.form['end'] + '%'
        # search date only
        bookings = db.execute(
            "SELECT id, make, body, colour, seats, location, cost FROM cars WHERE make LIKE ? AND colour LIKE ? ORDER BY created DESC",(start,end,)
        ).fetchall()
        # all in the search box will return all the tuples
        return render_template("blog/bookings.html", bookings=bookings, form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        bookings = db.execute(
            "SELECT p.id, make, body, colour, seats, location, cost, created, author_id, username"
            " FROM cars p JOIN user u ON p.author_id = u.id"
            " ORDER BY created DESC"
        ).fetchall()
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


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form=newCarForm()
    """Create a new car for the current user."""
    if request.method == "POST":
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
            db = get_db()
            db.execute(
                "INSERT INTO cars (make, body, colour, seats, location, cost, author_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (make, body, colour, seats, location, cost, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.admincars"))

    return render_template("blog/create.html", form=form)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a car if the current user is the author."""
    car = get_car(id)
    form=updateCarForm()
    if request.method == "POST":
        make = request.form["make"]
        body = request.form["body"]
        colour = request.form["colour"]
        seats = request.form["seats"]
        location = request.form["location"]
        cost = request.form["cost"]
        error = None

# placeholder for input validation
        if not make:
            error = "Make is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE cars SET make = ?, body = ?, colour = ?, seats = ?, location = ?, cost = ? WHERE id = ?", (make, body, colour, seats, location, cost, id)
            )
            db.commit()
            return redirect(url_for("blog.admincars"))

    return render_template("blog/update.html", car=car, form=form)


@bp.route("/<int:id>/confirm", methods=("GET", "POST"))
def confirm(id):
    """Update a car if the current user is the author."""
    car = get_car(id)
    datestart=request.args['datestart']
    dateend=request.args['dateend']
    form=updateCarForm()
    return render_template("blog/confirm.html", car=car,datestart=datestart,dateend=dateend)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a car.

    Ensures that the car exists and that the logged in user is the
    author of the car.
    """
    get_car(id)
    db = get_db()
    db.execute("DELETE FROM cars WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.admincars"))
    
    
@bp.route("/<int:id>/repair", methods=("POST",))
@login_required
def repair(id):
    """Delete a car.

    Ensures that the car exists and that the logged in user is the
    author of the car.
    """
    get_car(id)
    db = get_db()
    db.execute(
            "UPDATE cars SET status = 'repair' WHERE id = ?", (id,)
            )
    db.commit()
    return redirect(url_for("blog.admincars"))
