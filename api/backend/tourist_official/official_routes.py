from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
import pandas as pd
import numpy as np

# Create a Blueprint for routes
official_bp = Blueprint("official", __name__)
    
# Get the data from the RoadQuality table
@official_bp.route("/roadquality", methods=["GET"])
def get_road_qualities():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM RoadQuality;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the TourismPrioritization table
@official_bp.route("/tourismprioritization", methods=["GET"])
def get_tourism_prior():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM TourismPrioritization;")
        data = cursor.fetchall()
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the RoadDensity table
@official_bp.route("/roaddensity", methods=["GET"])
def get_road_density():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM RoadDensity;")
        data = cursor.fetchall()
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the AvgFuelPrice table
@official_bp.route("/avgfuelprice", methods=["GET"])
def get_fuel_price():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM AvgFuelPrice;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the RoadSpending table
@official_bp.route("/roadspending", methods=["GET"])
def get_road_spending():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM RoadSpending;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the PassengerCars table
@official_bp.route("/passengercars", methods=["GET"])
def get_pass_cars():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM PassengerCars;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the Trips table
@official_bp.route("/trips", methods=["GET"])
def get_trips():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Trips;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get users of specific type
@official_bp.route("/usersoftype/<string:type>", methods=["GET"])
def get_users_of_type(type):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(f"""SELECT Username, Nationality, UserID, UserType FROM Users 
                       WHERE UserType = '{type}';""")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

@official_bp.route("/timeseries/<string:country>", methods=["GET"])
def get_ts_prediction(country):
   cursor = None
   try:
       cursor = db.get_db().cursor()


       cursor.execute("""SELECT Country, TripYear, PredictedTrips
                        FROM TourismPredictions
                        WHERE Country = %s
                        ORDER BY TripYear;""", (country,))
      
       prediction_rows = cursor.fetchall()
      
       if not prediction_rows:
           return jsonify({"error": "Data not found"}), 404
      
       cursor.close()
       return jsonify(prediction_rows), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500
  
@official_bp.route("/trips/<string:country>", methods=["GET"])
def get_trip_for_country(country):
   cursor = None
   try:
       cursor = db.get_db().cursor()


       cursor.execute("""SELECT Country, TripYear, NumTrips
                        FROM Trips
                        WHERE Country = %s
                        ORDER BY TripYear;""", (country,))
      
       prediction_rows = cursor.fetchall()
      
       if not prediction_rows:
           return jsonify({"error": "Data not found"}), 404
      
       cursor.close()
       return jsonify(prediction_rows), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

@official_bp.route("/graph", methods=["GET","POST"])
def graph():
    if request.method == "POST":
        try:
                data = request.get_json()
                cursor = db.get_db().cursor()
                query = """
                INSERT INTO GraphFindings (OfficialID, NationalityValues, SelectedCountryValues, NationalityName, SelectedCountryName, ComparisonName)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        data["OfficialID"],
                        data["NationalityValues"],
                        data["SelectedCountryValues"],
                        data["NationalityName"],
                        data["SelectedCountryName"],
                        data["ComparisonName"]
                    ),
                )
                db.get_db().commit()
                cursor.close()
                return jsonify({"message": "Graph data saved successfully"}), 201
        except Error as e:
                return jsonify({"error": str(e)}), 500
    elif request.method == "GET":
        try:
            cursor = db.get_db().cursor()
            query = """
                SELECT 
                    g.GraphID,
                    g.NationalityValues,
                    g.SelectedCountryValues,
                    g.NationalityName,
                    g.SelectedCountryName,
                    g.ComparisonName,
                    g.OfficialID,
                    g.GraphDate,
                    u.UserName as OfficialName
                FROM GraphFindings g
                LEFT JOIN Users u ON g.OfficialID = u.UserID
            """
            cursor.execute(query)
            graphs = cursor.fetchall()
            cursor.close()
            return jsonify({
                "message": f"Found {len(graphs)} posts",
                "posts": graphs
            }), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
            