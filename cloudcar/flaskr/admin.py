from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from .auth import login_required
from .forms import *
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
from datetime import *
import requests
import math
import re
import os

admin = Blueprint("admin", __name__)

@admin.route("/adminusers", methods=("GET", "POST"))
@login_required
def adminusers():
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    form = AdminUserSearch()
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
        return render_template("admin/adminusers.html", users=users, form=form)
    if request.method == "GET":
        users = requests.get("http://127.0.0.1:8080/customers/get/all/users").json()
       
        #if form.validate_on_submit():
        #    return redirect(url_for('success'))
        return render_template("admin/adminusers.html", users=users["user"], form=form)
        
@admin.route("/admincars", methods=("GET", "POST"))
@login_required
def admincars():
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    form = AdminCarSearch()
    if request.method == "POST":
        error = None
        cars=[]
        brand = '%' + request.form['brand'] + '%'
        car_type = '%' + request.form['car_type'] + '%'
        color = '%' + request.form['color'] + '%'
        seat = '%' + request.form['seat'].strip() + '%'
        cost =request.form['cost'].strip()
        if not cost:
            cost = 1000
        if cost:
            try:
                cost=float(cost)
            except: 
                error = "Cost must be a number"
                flash(error)
                cars = []
                return render_template("admin/admincars.html", form=form, cars=cars)
        cars = requests.get("http://127.0.0.1:8080/cars/read?brand={}&car_type={}&color={}&seat={}&cost={}"
        .format(str(brand), str(car_type), str(color), str(seat), str(cost))).json()
        return render_template("admin/admincars.html", cars=cars["car"], form=form)
    """Show all the cars, most recent first."""
    if request.method == "GET":
        cars = requests.get("http://127.0.0.1:8080/cars/read?mac_address=&brand=&car_type=&status&color=&seat=&cost=&start=&end=").json()
        #do I need these next 2 lines?
        #if form.validate_on_submit():
        #    return redirect(url_for('success'))
        return render_template("admin/admincars.html", cars=cars["car"], form=form)


@admin.route("/<int:id>/carbookings", methods=("GET", "POST"))
@login_required
def carbookings(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    bookings = []
    error = None
    bookings = requests.get("http://127.0.0.1:8080/cars/history?id={}".format(id)).json()

    return render_template("customer/carbookings.html", bookings=bookings["history"], id=id)

@admin.route("/<int:id>/deletebooking", methods=("GET", "POST"))
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


@admin.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    form=NewCarForm()
    """Create a new car for the current user."""
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
            return redirect(url_for("admin.admincars"))
        return render_template("blog/create.html", form=form)

    return render_template("blog/create.html", form=form)


@admin.route("/createuser", methods=("GET", "POST"))
@login_required
def createuser():
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    db = get_db()
    form = AdminUserForm()
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



@admin.route("/<int:id>/updateuser", methods=("GET", "POST"))
@login_required
def updateuser(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"
    """Update a user."""
    user = get_user(id)
    form = AdminUserForm()
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
        
@admin.route("/<int:id>/deleteuser", methods=("GET", "POST"))
@login_required
def deleteuser(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"    
    user = get_user(id)
    db = get_db()
    db.execute("DELETE FROM User WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.adminusers"))

@admin.route("/<int:id>/update", methods=("GET", "POST"))
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
            return render_template("admin/update.html", form=form, car=car)
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
            db = get_db()
            db.execute(
                "UPDATE Car SET make = ?, body = ?, colour = ?, seats = ?, location = ?, cost = ? WHERE id = ?", (make, body, colour, seats, location, cost, id)
            )
            db.commit()
            return redirect(url_for("blog.admincars"))
        return render_template("blog/update.html", car=car, form=form)
    return render_template("blog/update.html", car=car, form=form)


@admin.route("/<int:id>/delete", methods=("POST",))
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
    return redirect(url_for("blog.admincars"))


@admin.route("/<int:id>/repair", methods=("POST",))
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

    
@admin.route("/<int:id>/sendmail", methods=("GET",))
@login_required
def sendmail(id):
    if (g.user['UserType'] != "Admin"):
        return "Access Denied"   
    car = get_car(id) 
    # Mail Sending integration goes here
    #
    #
    return redirect(url_for("blog.admincars"))


@admin.route("/edituser", methods=("GET", "POST"))
@login_required
def edituser():
    return redirect(url_for("blog.adminusers"))





    
    
