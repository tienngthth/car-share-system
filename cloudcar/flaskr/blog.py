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
from .forms import carSearch
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
bp = Blueprint("blog", __name__)



@bp.route("/", methods=("GET", "POST"))
def index():
    """Show all the cars, most recent first."""
    db = get_db()
    cars = db.execute(
        "SELECT p.id, make, body, colour, seats, location, cost, created, author_id, username"
        " FROM cars p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    
    form = carSearch()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template("blog/index.html", cars=cars, form=form)

@bp.route("/test")
def test():
    """Show all the cars, most recent first."""
    db = get_db()
    cars = db.execute(
        "SELECT p.id, make, body, colour, seats, location, cost, created, author_id, username"
        " FROM cars p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/test.html", cars=cars)


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
            "SELECT p.id, make, body, colour, seats, location, cost, created, author_id, username"
            " FROM cars p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if car is None:
        abort(404, "Car id {0} doesn't exist.".format(id))

    if check_author and car["author_id"] != g.user["id"]:
        abort(403)

    return car


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
            error = "Title is required."

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
