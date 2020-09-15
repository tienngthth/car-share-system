from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from .auth import login_required
from .forms import *
from datetime import *
import requests

home = Blueprint("home", __name__)

@home.errorhandler(404)
def page_not_found(e):
    return "Page not found"

@home.route("/", methods=("GET", "POST"))
@login_required
def index():
    if (g.type == "Admin"):
        return redirect(url_for("admin.cars"))
    if (g.type == "Engineer"):
        return redirect(url_for("engineer.cars"))
    if (g.type == "Manager"):
        return redirect(url_for("manager.manager"))
    return redirect(url_for("customer.cars"))



    