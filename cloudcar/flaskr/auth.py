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

@auth.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template("auth/login.html", form=form)
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        validated_user = Account.verify_password(username, password)
        if validated_user == "invalid":
            flash("Incorrect username or password.")
        else:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = validated_user["ID"]
            try:
                session["user_type"] = validated_user["UserType"]
            except:
                session["user_type"] = None
            return redirect(url_for("home.index"))
    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("home.index"))

@auth.route("/register", methods=("GET", "POST"))
def register():
    """
    Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    form = RegisterForm()
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        firstname = request.form["firstname"].strip()
        lastname = request.form["lastname"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        account = Account(username, password, email, firstname, lastname, phone)
        validate_account = account.validate_new_account()
        if validate_account != "Valid":
            flash(validate_account)
        else:
            print(validate_account)
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@auth.before_app_request
def load_logged_in_user():
    """
    If a user id is stored in the session, load the user object from
    the database into ``g.user``.
    """
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
