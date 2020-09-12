from flask import Blueprint, request
from model.database import Database

backlog_api = Blueprint("backlog_api", __name__)

@backlog_api.route("/create", methods=['GET', 'POST'])
def create_backlog():
    try:
        Database.insert_record_parameterized(
            "Backlogs(AssignedEngineerID, CarID, CreatedDate, Status, Description) ",
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

@backlog_api.route("/get/all/repaired/car/ids")
def get_all_repaired_car_ids():
    results = Database.select_record(
        " CarID ", 
        " Backlogs ", 
        " GROUP BY CarID "
    ) 
    return {"car_ids": results}

@backlog_api.route("/get/repaired/times/wrt/car/id")
def get_repaired_times_wrt_car_id():
    results = Database.select_record(
        " COUNT(CarID) as SUM ", 
        " Backlogs ", 
        " GROUP BY CarID"
    ) 
    return results[0]
