from flask import Blueprint, request, Flask, Markup, render_template
from model.database import Database
import googleMap

backlog_api = Blueprint("backlog_api", __name__)

@backlog_api.route("/create", methods=['GET', 'POST'])
def create_backlog():
    try:
        Database.insert_record_parameterized(
            "Backlogs(AssignedEngineerID, CarID, Date, Status, Description) ",
            "(%s, %s, %s, %s, %s)",
            (
                request.args.get("assigned_engineer_id"),
                request.args.get("car_id"),
                request.args.get("created_date"),
                request.args.get("status"),
                request.args.get("description")
            )
        )
        return "Success"
    except:
        return "Fail"

@backlog_api.route("/update", methods=['GET', 'PUT'])
def update():
    try:
        Database.update_record_parameterized(
            " Backlogs ", 
            " Status = 'Done', SignedEngineerID = (%s)",
            " WHERE CarID = (%s) AND Status = 'Not done' ",
            (request.args.get("signed_engineer_id"), request.args.get("car_id"))
        ) 
        return "Success"
    except:
        return "Fail"

@backlog_api.route("/get/backlogs/data")
def get_all_repaired_car_ids():
    results = Database.select_record(
        " CarID, CONVERT(COUNT(CarID), SIGNED) as Total", 
        " Backlogs ", 
        " GROUP BY CarID "
    ) 
    return {"results": results}

@backlog_api.route("/map/backlog")
def get_map():
    lattitude = googleMap.get_coordinates(request.args.get("id"))[0]
    longitude = googleMap.get_coordinates(request.args.get("id"))[1]
    return render_template('map.html', title='Map', lattitude=lattitude, longitude=longitude)

#New API starts here
@backlog_api.route("/engineer/get/cars")
def get_cars_for_engineer_page():
    results = Database.select_record(
        "Cars.ID, Locations.Address, Backlogs.Date, Backlogs.Status, Backlogs.ID AS Backlog_number", 
        "Cars INNER JOIN Backlogs ON Cars.ID = Backlogs.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID",
        ""
    )
    return {"car": results}

#This one does not require signed engineer's ID (Temporary API)
@backlog_api.route("/fix/car", methods=['GET', 'PUT'])
def fix_car():
    try:
        Database.update_record_parameterized(
            " Backlogs ", 
            " Status = 'Done'",
            " WHERE CarID = (%s) AND Status = 'Not done' ",
            request.args.get("car_id")
        ) 
        return "Success"
    except:
        return "Fail"