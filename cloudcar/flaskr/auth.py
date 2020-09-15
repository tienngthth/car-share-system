import functools
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flaskr.database.model.account import Account
from .forms import *
import re
import requests

auth = Blueprint("auth", __name__)


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("html.auth.login"))

        return view(**kwargs)

    return wrapped_view


@auth.before_app_request
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

@auth.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    form = Register()
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        firstname = request.form["firstname"].strip()
        lastname = request.form["lastname"].strip()
        email = request.form["email"].strip()
        valid_email = re.findall(r"[^@]+@[^@]+\.[^@]+",email)
        usertype = "Customer"
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
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        validate = Account.verify_password(username, password, "customers")
        if not validate:
            flash("Incorrect username or password.")
        else:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = int(requests.get("http://127.0.0.1:8080/customers/get/id?username=" + username).text)
            return redirect(url_for("index"))
    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))