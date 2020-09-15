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
#redirect user types to their homepages
    if (g.type == "Admin"):
        return redirect(url_for("admin.admincars"))
    if (g.type == "Engineer"):
        return redirect(url_for("engineer.engineercars"))
    if (g.type == "Manager"):
        return redirect(url_for("manager.manager"))
    form = UserCarSearch()
    if request.method == "POST":
        cars = []
        make = '%' + request.form['make'] + '%'
        body = '%' + request.form['body'] + '%'
        colour = '%' + request.form['colour'] + '%'
        seats = '%' + request.form['seats'].strip() + '%'
        cost = request.form['cost'].strip()
        error = None
        if not cost:
            cost = 1000
        if cost:
            try:
                cost=float(cost)
            except: 
                error = "Cost must be a number"
                flash(error)
                datestart = ""
                dateend = ""
                cars = []
                return render_template("html/blog/index.html", form=form, cars=cars,datestart=datestart, dateend=dateend)
        try:
            datestart = request.form['start'].strip()
            datestart = datetime.strptime(datestart, '%Y-%m-%dT%H:%M')
        except: return "Start date required"
        try:
           dateend = request.form['end'].strip()
           dateend = datetime.strptime(dateend, '%Y-%m-%dT%H:%M')
        except: return "End date required"
        if (dateend - datestart).days < 0:
            error = "End date must be later than start date"
            flash(error)
            return render_template("blog/index.html", cars=cars, form=form)
        if error is not None:
            flash(error)
        else:   
            # search form
            cars = requests.get("http://127.0.0.1:8080/cars/read?mac_address=&brand={}&car_type={}&status=Available&color={}&seat={}&cost={}&start={}&end={}"
                .format(str(make), str(body), str(colour), str(seats), str(cost), str(datestart), str(dateend))).json()
            return render_template("/index.html", cars=cars["car"], form=form, datestart=datestart, dateend=dateend)
    
    """Show all the cars, most recent first."""
    if request.method == "GET":
        datestart = ""
        dateend = ""
        cars = []
        return render_template("/index.html", cars=cars, form=form, datestart=datestart, dateend=dateend)



        


        

    