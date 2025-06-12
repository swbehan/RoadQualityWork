from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
import pandas as pd
import numpy as np

# Create a Blueprint for routes
official_bp = Blueprint("official", __name__)

@official_bp.route("/get_merged_data", methods=["GET"])
def get_merged_data():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""SELECT DISTINCT RoadYear AS Year,
                t.Country,
                RoadSpending,
                GDP,
                SpendingByGDPPercent,
                SUM(t.NumTrips) AS TotalTrips,
                COUNT(t.Duration) AS NumDurationTypes
FROM RoadSpending rs
         JOIN RoadQuality rq
              ON ((rs.Country = rq.Country) AND (rs.SpendingYear = rq.RoadYear))
         JOIN Trips t
              ON ((rq.Country = t.Country) AND (rq.RoadYear = t.TripYear))
         JOIN TourismPrioritization tp
              ON ((t.Country = tp.Country) AND (t.TripYear = tp.TourismYear))
GROUP BY rs.SpendingYear, rs.Country, rs.RoadSpending, rs.GDP, rs.SpendingByGDPPercent;""")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
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
    

@official_bp.route("/timeseries/<string:country>")
def get_ts_prediction(country):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(f"""SELECT *
            FROM TimeSeriesPredictions
            WHERE Country = '{country}';""")
        
        pred_data = cursor.fetchall()
        if not pred_data:
            return jsonify({"error": "Prediction data not found"}), 404

        pred_df = pd.DataFrame(pred_data)
        pred_df = pred_df.rename(columns={'PredictedTrips': 'NumTrips'})

        cursor.execute(f"""SELECT *
            FROM Trips
            WHERE Country = '{country}' AND Duration = '1 night or over';""")
        
        past_data = cursor.fetchall()
        if not past_data:
            return jsonify({"error": "Past data not found"}), 404

        past_df = pd.DataFrame(past_data)
        past_df = past_df.drop('Duration', axis=1)

        all_df = pd.concat([past_df, pred_df], ignore_index=True)

        past_and_pred_dict = all_df.to_dict(orient="records")

        cursor.close()
        return jsonify(past_and_pred_dict), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500