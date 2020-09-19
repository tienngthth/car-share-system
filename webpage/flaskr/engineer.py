#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, flash, g, redirect
from flask import render_template, request, url_for
from .auth import login_required
import requests
import json

engineer = Blueprint("engineer", __name__)

@engineer.route("/cars", methods=("GET", "POST"))
@login_required
def car_view():
    if g.type != "Engineer":
        return "Access Denied"
    if request.method == "GET":
        backlogs = requests.get("http://127.0.0.1:8080/backlogs/get/all").json()["backlogs"]
        return render_template("engineer/backlog_view.html", backlogs=backlogs)

@engineer.route("/location", methods=("GET", "POST"))
@login_required
def location_map():
    if g.type != "Engineer":
        return "Access Denied"
    car = requests.get("http://127.0.0.1:8080/cars/read?id=" + request.args['car_id']).json()["cars"][0]
    location = requests.get("http://127.0.0.1:8080/locations/get?id=" + request.args['location_id']).json()["location"][0]
    return render_template("engineer/location_map.html", car=car, location=location)

@engineer.route("/close/backlog", methods=("POST",))
@login_required
def close_backlog():
    if g.type != "Engineer":
        return "Access Denied"
    requests.put(
        "http://127.0.0.1:8080/backlogs/close?car_id={}&signed_engineer_id={}"
        .format(request.args['car_id'], g.user['ID'])
    )
    requests.put(
        "http://127.0.0.1:8080/cars/update?id={}&status=Available"
        .format(request.args['car_id'])
    )
    return redirect(url_for("engineer.car_view"))