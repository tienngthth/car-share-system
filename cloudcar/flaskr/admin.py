from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from flaskr.script.emailscripts.sendmail import send_mail
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from .auth import login_required
from .forms import *
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
from datetime import *
import smtplib
import requests
import math
import re
import os
from flaskr.script.model.booking import Booking

admin = Blueprint("admin", __name__)

@admin.route("/cars", methods=("GET", "POST"))
@login_required
def car_view():
    """Admin view car"""
    if (g.type != "Admin"):
        return "Access Denied"
    form = AdminCarSearchForm()
    if request.method == "POST":
        return search_car(form)
    if request.method == "GET":
        return display_all_cars(form)

def search_car(form):
    """Search car by filter"""
    brand = request.form['brand']
    car_type = request.form['car_type']
    color = request.form['color']
    seat = request.form['seat']
    cost = request.form['cost']
    mac_address = request.form['mac_address']
    if not Booking.validate_cost(cost):
        return display_all_cars(form)
    cars = requests.get(
        "http://127.0.0.1:8080/cars/read?brand={}&car_type={}&color={}&seat={}&cost={}&mac_address={}"
        .format(brand, car_type, color, seat, cost, mac_address)
    ).json()
    return render_template("admin/car_view.html", cars=cars["car"], form=form)

def display_all_cars(form):
    """Show all the cars"""
    cars = requests.get(
        "http://127.0.0.1:8080/cars/read?mac_address=&brand=&car_type=&status&color=&seat=&cost=&start=&end="
    ).json()
    return render_template("admin/car_view.html", cars=cars["car"], form=form)

@admin.route("/users", methods=("GET", "POST"))
@login_required
def user_view():
    if (g.type != "Admin"):
        return "Access Denied"
    form = AdminUserSearchForm()
    if request.method == "POST":
        username = '%' + request.form['username'].strip() + '%'
        first = '%' + request.form['first'].strip() + '%'
        last = '%' + request.form['last'].strip() + '%'
        phone = '%' + request.form['phone'].strip() + '%'
        email = '%' + request.form['email'].strip() + '%'
        error = None
        users = []
        users = requests.get("http://127.0.0.1:8080/customers/read?username={}&first_name={}&last_name={}&email={}&phone={}"
        .format(str(username), str(first), str(last), str(email), str(phone))).json()
        # all in the search box will return all the tuples
        return render_template("admin/user_view.html", users=users["user"], form=form)
    if request.method == "GET":
        users = requests.get("http://127.0.0.1:8080/customers/get/all/users").json()
        return render_template("admin/user_view.html", users=users["user"], form=form)
        

@admin.route("/<int:id>/carbookings", methods=("GET", "POST"))
@login_required
def carbookings(id):
    if (g.type != "Admin"):
        return "Access Denied"
    bookings = []
    error = None
    bookings = requests.get("http://127.0.0.1:8080/cars/history?id={}".format(id)).json()

    return render_template("customer/carbookings.html", bookings=bookings["history"], id=id)


@admin.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if (g.type != "Admin"):
        return "Access Denied"
    form=NewCarForm()
    """Create a new car for the current user."""
    if request.method == "POST":
        mac_address = request.form["mac_address"].strip()
        brand = request.form["brand"].strip()
        car_type = request.form["car_type"].strip()
        color = request.form["color"].strip()
        seat = request.form["seat"].strip()
        location_id = request.form["location_id"].strip()
        cost = request.form["cost"].strip()
        error = None
        #input validation
        try:
            cost=float(cost)
        except: 
            error = "Cost must be a number"
            flash(error)
            return render_template("admin/create.html", form=form)
        if not mac_address:
            error = "Mac Address is required."
        elif not brand:
            error = "Brand is required."
        elif not car_type:
            error = "Car type is required."    
        elif not color:
            error = "Color is required."
        elif not seat:
            error = "Seat is required."
        elif not location_id:
            error = "Location is required."
        elif not cost:
            error = "Cost is required."
        elif cost < 1 or cost > 1000:
            error = "Cost must be a number between 1 and 1000."
        if error is not None:
            flash(error)
        else:
            requests.get("http://127.0.0.1:8080/cars/create?mac_address={}&brand={}&type={}&location_id={}&status=Available&color={}&seat={}&cost={}"
            .format(str(mac_address), str(brand), str(car_type), str(location_id), str(color), str(seat), str(cost)))
            return redirect(url_for("admin.cars"))
        return render_template("admin/create.html", form=form)

    return render_template("admin/create.html", form=form)

@admin.route("/createuser", methods=("GET", "POST"))
@login_required
def createuser():
    if (g.type != "Admin"):
        return "Access Denied"
    form = CreateUserForm()
    if request.method == "GET":
        render_template("admin/createuser.html", form=form)
    """Create a new car for the current user."""
    if request.method == "POST":
        username = request.form["username"].strip()
        firstname = request.form["firstname"].strip()
        lastname = request.form["lastname"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        password = request.form["password"]
        valid_email = re.findall(r"[^@]+@[^@]+\.[^@]+",email)
        error = None
        if not username:
            error = "Username is required."
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
            requests.get("http://127.0.0.1:8080/customers/get/id?username={}".format(str(username))) != "invalid"
        ):
            error = "User {0} is already registered.".format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            requests.get("http://127.0.0.1:8080/customers/create?username={}&first_name={}&last_name={}&email={}&phone={}&password={}"
            .format(str(username), str(firstname), str(lastname), str(email), str(phone), str(password)))
            return redirect(url_for("admin.users"))

        flash(error)

    return render_template("admin/createuser.html", form=form)

@admin.route("/<int:id>/updateuser", methods=("GET", "POST"))
@login_required
def updateuser(id):
    if (g.type != "Admin"):
        return "Access Denied"
    """Update a user."""
    user = requests.get("http://127.0.0.1:8080/customers/get/user/by/id?id={}".format(str(id))).json()["user"][0]
    form = UpdateUserForm()
    if request.method == "GET":
        return render_template("admin/updateuser.html", user=user, form=form)
    if request.method == "POST":
        username = request.form["username"].strip()
        phone = request.form["phone"].strip()
        firstname = request.form["first"].strip()
        lastname = request.form["last"].strip()
        email = request.form["email"].strip()
        error = None
        if not username:
            username = user["Username"]
        if not phone:
            phone = user["Phone"]
        if not firstname:
            firstname = user["FirstName"]
        if not lastname:
            lastname = user["LastName"]
        if not email:
            email = user["Email"]
        valid_email = re.findall(r"[^@]+@[^@]+\.[^@]+",email)
        if len(valid_email) < 1:
            error = "Incorrectly formatted email address"

        if error is None:
            requests.get("http://127.0.0.1:8080/customers/update?username={}&first_name={}&last_name={}&email={}&phone={}&id={}"
            .format(str(username), str(firstname), str(lastname), str(email), str(phone),str(id)))
            return redirect(url_for("admin.users"))
        return render_template("admin/updateuser.html", user=user, form=form)
        
@admin.route("/<int:id>/deleteuser", methods=("GET", "POST"))
@login_required
def deleteuser(id):
    if (g.type != "Admin"):
        return "Access Denied"    
    user = requests.get("http://127.0.0.1:8080/customers/delete?id={}".format(str(id)))
    return redirect(url_for("admin.users"))

@admin.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    if (g.type != "Admin"):
        return "Access Denied"
    """Update a car."""
    car = requests.get("http://127.0.0.1:8080/cars/get?id={}".format(str(id))).json()["car"][0]
    form=UpdateCarForm()
    if request.method == "POST":
        mac_address = request.form["mac_address"].strip()
        brand = request.form["brand"].strip()
        car_type = request.form["car_type"].strip()
        color = request.form["color"].strip()
        seat = request.form["seat"].strip()
        location_id = request.form["location_id"].strip()
        cost = request.form["cost"].strip()
        error = None
        if not mac_address:
            mac_address = car["MacAddress"]
        if not brand:
            brand = car["Brand"]
        if not car_type:
            car_type = car["Type"]
        if not color:
            color = car["Color"]
        if not seat:
            seat = car["Seat"]
        if not location_id:
            location_id = car["LocationID"]
        if not cost:
            cost = car["Cost"]
        elif cost < 1 or cost > 1000:
            error = "Cost must be a number between 1 and 1000."
        #input validation
        try:
            cost=float(cost)
        except: 
            error = "Cost must be a number"
            flash(error)
            return render_template("admin/update.html", form=form, car=car)
        
        if error is not None:
            flash(error)
        else:
            requests.get("http://127.0.0.1:8080/cars/update?id={}&mac_address={}&brand={}&type={}&location_id={}&status=Available&color={}&seat={}&cost={}"
            .format(str(id), str(mac_address), str(brand), str(car_type), str(location_id), str(color), str(seat), str(cost)))
            return redirect(url_for("admin.cars"))
        return render_template("admin/update.html", car=car, form=form)
    return render_template("admin/update.html", car=car, form=form)


@admin.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    if (g.type != "Admin"):
        return "Access Denied"
    car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id={}".format(str(id))).json()
    return redirect(url_for("blog.admincars"))


@admin.route("/<int:id>/repair", methods=("GET",))
@login_required
def report(id):
    if (g.type != "Admin"):
        return "Access Denied"
    car = requests.get("http://127.0.0.1:8080/cars/get?id={}".format(str(id))).json()
    engineer = requests.get("http://127.0.0.1:8080/staffs/get/engineer").json()
    message = MIMEMultipart("alternative")
    message["Subject"] = "Car Maintenance Request"
    message["From"] = "ahjhj24012000@gmail.com"
    message["To"] = "quoccuong242000@gmail.com"

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <!doctype html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width" />
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Simple Transactional Email</title>
        <style>
        /* -------------------------------------
            GLOBAL RESETS
        ------------------------------------- */
        
        /*All the styling goes here*/
        
        img {
            border: none;
            -ms-interpolation-mode: bicubic;
            max-width: 100%; 
        }

        body {
            background-color: #f6f6f6;
            font-family: sans-serif;
            -webkit-font-smoothing: antialiased;
            font-size: 14px;
            line-height: 1.4;
            margin: 0;
            padding: 0;
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%; 
        }

        table {
            border-collapse: separate;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
            width: 100%; }
            table td {
            font-family: sans-serif;
            font-size: 14px;
            vertical-align: top; 
        }

        /* -------------------------------------
            BODY & CONTAINER
        ------------------------------------- */

        .body {
            background-color: #f6f6f6;
            width: 100%; 
        }

        /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
        .container {
            display: block;
            margin: 0 auto !important;
            /* makes it centered */
            max-width: 580px;
            padding: 10px;
            width: 580px; 
        }

        /* This should also be a block element, so that it will fill 100% of the .container */
        .content {
            box-sizing: border-box;
            display: block;
            margin: 0 auto;
            max-width: 580px;
            padding: 10px; 
        }

        /* -------------------------------------
            HEADER, FOOTER, MAIN
        ------------------------------------- */
        .main {
            background: #ffffff;
            border-radius: 3px;
            width: 100%; 
        }

        .wrapper {
            box-sizing: border-box;
            padding: 20px; 
        }

        .content-block {
            padding-bottom: 10px;
            padding-top: 10px;
        }

        .footer {
            clear: both;
            margin-top: 10px;
            text-align: center;
            width: 100%; 
        }
            .footer td,
            .footer p,
            .footer span,
            .footer a {
            color: #999999;
            font-size: 12px;
            text-align: center; 
        }

        /* -------------------------------------
            TYPOGRAPHY
        ------------------------------------- */
        h1,
        h2,
        h3,
        h4 {
            color: #000000;
            font-family: sans-serif;
            font-weight: 400;
            line-height: 1.4;
            margin: 0;
            margin-bottom: 30px; 
        }

        h1 {
            font-size: 35px;
            font-weight: 300;
            text-align: center;
            text-transform: capitalize; 
        }

        p,
        ul,
        ol {
            font-family: sans-serif;
            font-size: 14px;
            font-weight: normal;
            margin: 0;
            margin-bottom: 15px; 
        }
            p li,
            ul li,
            ol li {
            list-style-position: inside;
            margin-left: 5px; 
        }

        a {
            color: #3498db;
            text-decoration: underline; 
        }

        /* -------------------------------------
            BUTTONS
        ------------------------------------- */
        .btn {
            box-sizing: border-box;
            width: 100%; }
            .btn > tbody > tr > td {
            padding-bottom: 15px; }
            .btn table {
            width: auto; 
        }
            .btn table td {
            background-color: #ffffff;
            border-radius: 5px;
            text-align: center; 
        }
            .btn a {
            background-color: #ffffff;
            border: solid 1px #3498db;
            border-radius: 5px;
            box-sizing: border-box;
            color: #3498db;
            cursor: pointer;
            display: inline-block;
            font-size: 14px;
            font-weight: bold;
            margin: 0;
            padding: 12px 25px;
            text-decoration: none;
            text-transform: capitalize; 
        }

        .btn-primary table td {
            background-color: #3498db; 
        }

        .btn-primary a {
            background-color: #3498db;
            border-color: #3498db;
            color: #ffffff; 
        }

        /* -------------------------------------
            OTHER STYLES THAT MIGHT BE USEFUL
        ------------------------------------- */
        .last {
            margin-bottom: 0; 
        }

        .first {
            margin-top: 0; 
        }

        .align-center {
            text-align: center; 
        }

        .align-right {
            text-align: right; 
        }

        .align-left {
            text-align: left; 
        }

        .clear {
            clear: both; 
        }

        .mt0 {
            margin-top: 0; 
        }

        .mb0 {
            margin-bottom: 0; 
        }

        .preheader {
            color: transparent;
            display: none;
            height: 0;
            max-height: 0;
            max-width: 0;
            opacity: 0;
            overflow: hidden;
            mso-hide: all;
            visibility: hidden;
            width: 0; 
        }

        .powered-by a {
            text-decoration: none; 
        }

        hr {
            border: 0;
            border-bottom: 1px solid #f6f6f6;
            margin: 20px 0; 
        }

        /* -------------------------------------
            RESPONSIVE AND MOBILE FRIENDLY STYLES
        ------------------------------------- */
        @media only screen and (max-width: 620px) {
            table[class=body] h1 {
            font-size: 28px !important;
            margin-bottom: 10px !important; 
            }
            table[class=body] p,
            table[class=body] ul,
            table[class=body] ol,
            table[class=body] td,
            table[class=body] span,
            table[class=body] a {
            font-size: 16px !important; 
            }
            table[class=body] .wrapper,
            table[class=body] .article {
            padding: 10px !important; 
            }
            table[class=body] .content {
            padding: 0 !important; 
            }
            table[class=body] .container {
            padding: 0 !important;
            width: 100% !important; 
            }
            table[class=body] .main {
            border-left-width: 0 !important;
            border-radius: 0 !important;
            border-right-width: 0 !important; 
            }
            table[class=body] .btn table {
            width: 100% !important; 
            }
            table[class=body] .btn a {
            width: 100% !important; 
            }
            table[class=body] .img-responsive {
            height: auto !important;
            max-width: 100% !important;
            width: auto !important; 
            }
        }

        /* -------------------------------------
            PRESERVE THESE STYLES IN THE HEAD
        ------------------------------------- */
        @media all {
            .ExternalClass {
            width: 100%; 
            }
            .ExternalClass,
            .ExternalClass p,
            .ExternalClass span,
            .ExternalClass font,
            .ExternalClass td,
            .ExternalClass div {
            line-height: 100%; 
            }
            .apple-link a {
            color: inherit !important;
            font-family: inherit !important;
            font-size: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
            text-decoration: none !important; 
            }
            #MessageViewBody a {
            color: inherit;
            text-decoration: none;
            font-size: inherit;
            font-family: inherit;
            font-weight: inherit;
            line-height: inherit;
            }
            .btn-primary table td:hover {
            background-color: #34495e !important; 
            }
            .btn-primary a:hover {
            background-color: #34495e !important;
            border-color: #34495e !important; 
            } 
        }

        </style>
    </head>
    <body class="">
        <span class="preheader">This is preheader text. Some clients will show this text as a preview.</span>
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
        <tr>
            <td>&nbsp;</td>
            <td class="container">
            <div class="content">

                <!-- START CENTERED WHITE CONTAINER -->
                <table role="presentation" class="main">

                <!-- START MAIN CONTENT AREA -->
                <tr>
                    <td class="wrapper">
                    <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                        <tr>
                        <td>
                            <p>Hello engineer,</p>
                            <p>Repairs have been requested for car #""" + str(id) +"""</p>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
                            <tbody>
                                <tr>
                                <td align="left">
                                    <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                    <tbody>
                                        <tr>
                                        <td> <a href=\"""" + "http://127.0.0.1:5000/auth/login" + """\" target="_blank">Click here to login</a> </td>
                                        </tr>
                                    </tbody>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                            <p>Once logged in, you can see the car's location. Remember to mark the car as repaired when finished!</p>
                            <p>Have a great day.</p>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>

                <!-- END MAIN CONTENT AREA -->
                </table>
                <!-- END CENTERED WHITE CONTAINER -->

                <!-- START FOOTER -->
                <div class="footer">
                <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                    <td class="content-block">
                        <span class="apple-link">CloudCar, 123 Fake Street, HCMC Vietnam 700000</span>
                        
                    </td>
                    </tr>
                    <tr>
                    <td class="content-block powered-by">
                        Powered by <a href="https://github.com/leemunroe/responsive-html-email-template">HTMLemail</a>.
                    </td>
                    </tr>
                </table>
                </div>
                <!-- END FOOTER -->

                </div>
                </td>
                <td>&nbsp;</td>
            </tr>
            </table>
        </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("ahjhj24012000@gmail.com", "quoc2401@")
    server.sendmail("ahjhj24012000@gmail.com", "quoccuong242000@gmail.com", message.as_string())
    requests.get("http://127.0.0.1:8080/backlogs/create?assigned_engineer_id={}&car_id={}&status=Not%20done&description="
            .format(str(engineer["engineer"][0]["ID"]), str(car["car"][0]["ID"])))
    return redirect(url_for("admin.cars"))


@admin.route("/edituser", methods=("GET", "POST"))
@login_required
def edituser():
    return redirect(url_for("blog.adminusers"))





    
    
