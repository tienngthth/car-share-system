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
from .forms import carSearch, bookingSearch
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
bp = Blueprint("blog", __name__)



@bp.route("/", methods=("GET", "POST"))
def index():
    form = carSearch()
    db = get_db()
    if request.method == "POST":
        make = '%' + request.form['make'] + '%'
        colour = '%' + request.form['colour'] + '%'
        # search form
        cars = db.execute(
            "SELECT id, make, body, colour, seats, location, cost FROM cars WHERE make LIKE ? AND colour LIKE ? ORDER BY created DESC",(make,colour,)
        ).fetchall()
        # all in the search box will return all the tuples
        return render_template("blog/index.html", cars=cars, form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        cars = db.execute(
            "SELECT p.id, make, body, colour, seats, location, cost, created, author_id, username"
            " FROM cars p JOIN user u ON p.author_id = u.id"
            " ORDER BY created DESC"
        ).fetchall()
        #do I need these next 2 lines?
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template("blog/index.html", cars=cars, form=form)

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





@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
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
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    car = get_car(id)

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
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", car=car)


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
    return redirect(url_for("blog.index"))
