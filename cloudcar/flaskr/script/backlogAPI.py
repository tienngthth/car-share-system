from flask import Blueprint, request, Flask, Markup, render_template
from model.database import Database

backlog_api = Blueprint("backlog_api", __name__)

@backlog_api.route("/create", methods=['GET', 'POST'])
def create_backlog():
    # try:
        Database.insert_record_parameterized(
            "Backlogs(AssignedEngineerID, CarID, CreatedDate, Status, Description) ",
            "(%s, %s, CURDATE(), %s, %s)",
            (
                request.args.get("assigned_engineer_id"),
                request.args.get("car_id"),
                request.args.get("status"),
                request.args.get("description")
            )
        )
        return "Success"
    # except:
        return "Fail"

@backlog_api.route("/close", methods=['GET', 'PUT'])
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

#New API starts here
@backlog_api.route("/get/all")
def get_all_backlogs():
    results = Database.select_record(
        "Cars.ID AS CarID, Cars.Type AS CarType, Cars.Brand AS CarBrand, Cars.LocationID as LocationID," +
        "Backlogs.CreatedDate AS CreatedDate, Backlogs.Status AS Status" , 
        "Cars INNER JOIN Backlogs ON Cars.ID = Backlogs.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID",
        ""
    )
    return {"backlogs": results}

@backlog_api.route("/get/engineer/id")
def get_engineer_id():
    results = Database.select_record_parameterized(
        " AssignedEngineerID ", 
        " Backlogs ", 
        " WHERE CarID LIKE %s AND Status LIKE 'Not done' ",
        (request.args.get("car_id"),)
    ) 
    if len(results) == 0:
        return "No engineer found"
    else:
        return results[0]