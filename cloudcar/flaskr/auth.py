import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from .forms import *
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import re
from flaskr.db import get_db
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
import requests

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_customer_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login_as_customer"))
        return view(**kwargs)
    return wrapped_view

def login_admin_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login_as_admin"))
        return view(**kwargs)
    return wrapped_view

def login_manager_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login_as_manager"))
        return view(**kwargs)
    return wrapped_view

def login_engineer_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login_as_engineer"))
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    user_type = session.get("user_type")

    if user_id is None:
        g.user = None
    else:
        if user_type is None:
            g.user = requests.get("http://127.0.0.1:8080/customers/get/user/by/id?id={}".format(str(user_id))).json()["user"][0]
            g.type = "Customer"
        elif user_type == "Admin":
            g.user = requests.get("http://127.0.0.1:8080/staffs/get/admin?username=&id={}".format(str(user_id))).json()["admin"][0]
            g.type = user_type
        elif user_type == "Manager":
            g.user = requests.get("http://127.0.0.1:8080/staffs/get/manager?username=&id={}".format(str(user_id))).json()["manager"][0]
            g.type = user_type
        elif user_type == "Engineer":
            g.user = requests.get("http://127.0.0.1:8080/staffs/get/engineer?username=&id={}".format(str(user_id))).json()["engineer"][0]
            g.type = user_type

#DONE
@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    form = Register()
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        first = request.form["first"]
        last = request.form["last"]
        email = request.form["email"]
        phone = request.form["phone"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif len(requests.get("http://127.0.0.1:8080/customers/get/user/by/username?username={}".format(str(username))).json()["user"]) > 0:
            error = "User {0} is already registered.".format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            requests.get("http://127.0.0.1:8080/customers/create?username={}&password={}&first_name={}&last_name={}&email={}&phone={}"
            .format(str(username), generate_password_hash(password), str(first), str(last), str(email), str(phone)))
            return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login_as_customer():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = requests.get("http://127.0.0.1:8080/customers/get/user/by/username?username={}".format(str(username))).json()["user"]
        if len(user) == 0:
            error = "Incorrect username."
        elif user[0]["Password"] != password:
            error = "Incorrect password."
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user[0]["ID"]
            session["user_type"] = None
            return redirect(url_for("index"))
        flash(error)
    return render_template("auth/login.html")

@bp.route("/login/admin", methods=("GET", "POST"))
def login_as_admin():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = requests.get("http://127.0.0.1:8080/staffs/get/admin?username={}&id=".format(str(username))).json()["admin"]
        if len(user) == 0:
            error = "Incorrect username."
        elif user[0]["Password"] != password:
            error = "Incorrect password."
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user[0]["ID"]
            session["user_type"] = user[0]["UserType"]
            return redirect(url_for("index"))
        flash(error)
    return render_template("auth/login.html")

@bp.route("/login/manager", methods=("GET", "POST"))
def login_as_manager():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = requests.get("http://127.0.0.1:8080/staffs/get/manager?username={}&id=".format(str(username))).json()["manager"]
        if len(user) == 0:
            error = "Incorrect username."
        elif user[0]["Password"] != password:
            error = "Incorrect password."
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user[0]["ID"]
            session["user_type"] = user[0]["UserType"]
            return redirect(url_for("index"))
        flash(error)
    return render_template("auth/login.html")

@bp.route("/login/engineer", methods=("GET", "POST"))
def login_as_engineer():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = requests.get("http://127.0.0.1:8080/staffs/get/engineer?username={}&id=".format(str(username))).json()["engineer"]
        if len(user) == 0:
            error = "Incorrect username."
        elif user[0]["Password"] != password:
            error = "Incorrect password."
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user[0]["ID"]
            session["user_type"] = user[0]["UserType"]
            return redirect(url_for("index"))
        flash(error)
    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
