#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backlogAPI.py defines the backlog API, whcih handles requests for engineers to repair cars.
"""
from flask import Blueprint, request, Flask, Markup, render_template
from database import Database
from flask.json import jsonify

backlog_api = Blueprint("backlog_api", __name__)

@backlog_api.route("/create", methods=['GET', 'POST'])
def create_backlog():
    """
    This function creates a new engineering backlog entry. Parameters:
    
    assigned_engineer_id: The ID of the engineer responsible for this task
    car_id: The car the engineer is assigned to repair
    status: The status of the car. Needs to be set to Repair
    description: Description of repairs required
    
    If all parameters are present and valid, the function returns Success, otherwise it returns Fail 
    """
    try:
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
    except:
        return "Fail"

@backlog_api.route("/close", methods=['GET', 'PUT'])
def close_backlog():
    """
    This closes an engineering backlog task as complete. Parameters:
    
    signed_engineer_id: The ID of the engineer responsible for this repair
    car_id: The car that was just repaired
    
    The function will return Success if all parameters are valid, and Fail if not.
    """
    Database.update_record_parameterized(
        " Backlogs ", 
        " Status = 'Done', SignedEngineerID = (%s)",
        " WHERE CarID = (%s) OR ID = (%s) AND Status = 'Not done' ",
        (request.args.get("signed_engineer_id"), request.args.get("car_id"), request.args.get("backlog_id"))
    ) 
    return "Success"

@backlog_api.route("/get/data")
def get_backlogs_data():
    """
    Returns a JSON object of all car id and its occurances. No parameters required.
    """
    results = Database.select_record(
        " CarID, CONVERT(COUNT(CarID), SIGNED) as Total", 
        " Backlogs ", 
        " WHERE CarID != 'None' GROUP BY CarID "
    ) 
    return jsonify(results)

#New API starts here
@backlog_api.route("/get/all")
def get_all_backlogs():
    """
    Returns a JSON object of all engineering backlog tasks. No parameters required.
    """
    results = Database.select_record(
        " Cars.ID AS CarID, Cars.Type AS CarType, Cars.Brand AS CarBrand, Cars.LocationID as LocationID, " +
        " Backlogs.CreatedDate AS CreatedDate, Backlogs.Status AS Status, Backlogs.Description AS Description, Backlogs.ID AS BacklogID " , 
        " Cars INNER JOIN Backlogs ON Cars.ID = Backlogs.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID ",
        " ORDER BY Backlogs.CreatedDate DESC "
    )
    return jsonify(results)

@backlog_api.route("/get/engineer/id")
def get_engineer_id():
    """
    Returns the ID of the engineer assigned to repair a particular car. Parameters:
    
    car_id: The car in question.
    
    Returns the engineer ID if there is an open task for that car, otherwise will return No engineer found.
    """
    results = Database.select_record_parameterized(
        " AssignedEngineerID ", 
        " Backlogs ", 
        " WHERE CarID LIKE %s AND Status LIKE 'Not done' ",
        (request.args.get("car_id"),)
    ) 
    if len(results) == 0:
        return "No engineer found"
    else:
        return str(results[0]["AssignedEngineerID"])

@backlog_api.route("remove/assigned/engineer")
def remove_assigned_engineer_from_backlogs():
    """
    Unassigns a particular assigned engineer from their tasks. Parameters:
    
    id: The ID of the assigned engineer.
    
    Returns Success if there were tasks to remove the given engineer from, and Fail otherwise. 
    """
    try:
        Database.update_record_parameterized(
            " Backlogs ", 
            " AssignedEngineerID = NULL",
            " WHERE AssignedEngineerID = (%s)",
            (request.args.get("id"),)
        ) 
        return "Success"
    except:
        return "Fail"

@backlog_api.route("remove/signed/engineer", methods=['GET', 'PUT'])
def remove_signed_engineer_from_backlogs():
    """
    Unassigns a particular assigned engineer from their tasks. Parameters:
    
    id: The ID of the signed engineer.
    
    Returns Success if there were tasks to remove the given engineer from, and Fail otherwise. 
    """
    try:
        Database.update_record_parameterized(
            " Backlogs ", 
            " SignedEngineerID = NULL",
            " WHERE SignedEngineerID = (%s)",
            (request.args.get("id"),)
        ) 
        return "Success"
    except:
        return "Fail"

@backlog_api.route("remove/car", methods=['GET', 'PUT'])
def remove_car_from_backlogs():
    """
    Remove a particular car from all engineering backlogs. Parameters:
    
    car_id: The car in question.
    
    Returns Success if any records were found and updated, Fail otherwise.
    """
    try:
        Database.update_record_parameterized(
            " Backlogs ", 
            " CarID = NULL",
            " WHERE CarID = (%s)",
            (request.args.get("car_id"),)
        ) 
        return "Success"
    except:
        return "Fail"
