from flask import Blueprint, request, Flask, Markup, render_template
from model.database import Database
import googleMap

backlog_api = Blueprint("backlog_api", __name__)

@backlog_api.route("/get/all/repaired/car/ids")
def get_all_repaired_car_ids():
    results = Database.select_record(
        "CarID", 
        "Backlogs", 
        " GROUP BY CarID"
    ) 
    if len(results) == 0:
        return "No car found"
    else: 
        return str(results)

@backlog_api.route("/get/repaired/times/wrt/car/id")
def get_repaired_times_wrt_car_id():
    results = Database.select_record(
        "COUNT(CarID) as Number_of_repairs", 
        "Backlogs", 
        " GROUP BY CarID"
    ) 
    if len(results) == 0:
        return "No car found"
    else: 
        return str(results)

@backlog_api.route("/update/signed/engineer/id/and/status/by/car/id", methods=['GET', 'PUT'])
def update_signed_eng_id_and_status_by_car_id():
    Database.update_record_parameterized(
        "Backlogs", 
        " Status = 'Done', SignedEngineerID = (%s)",
        " WHERE CarID = (%s) AND Status = 'Not done' ",
        (request.args.get("signed_engineer_id"), request.args.get("car_id"))
    ) 
    return "Done"

@backlog_api.route("/create", methods=['GET', 'POST'])
def create_backlog():
    Database.insert_record_parameterized(
        "Backlogs(AssignedEngineerID, SignedEngineerID, CarID, Date, Status, Description) ",
        "(%s, %s, %s, %s, %s, %s)",
        (
            request.args.get("assigned_engineer_id"),
            request.args.get("signed_engineer_id"),
            request.args.get("car_id"),
            request.args.get("date"),
            request.args.get("status"),
            request.args.get("description")
        )
    )
    return "Done"

@backlog_api.route("/map/backlog")
def get_map():
    lattitude = googleMap.get_coordinates(request.args.get("id"))[0]
    longitude = googleMap.get_coordinates(request.args.get("id"))[1]
    return render_template('map.html', title='Map', lattitude=lattitude, longitude=longitude)