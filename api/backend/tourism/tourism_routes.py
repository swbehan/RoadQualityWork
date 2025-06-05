from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for routes
tourism_bp = Blueprint("tourism", __name__)

# Get the data from the RoadQuality table
@tourism_bp.route("/roadquality", methods=["GET"])
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
@tourism_bp.route("/tourismprioritization", methods=["GET"])
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
@tourism_bp.route("/roaddensity", methods=["GET"])
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
@tourism_bp.route("/avgfuelprice", methods=["GET"])
def get_fuel_price():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM AvgFuelPrice;")
        data = cursor.fetchall()
        print("Data:", data)
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the RoadSpending table
@tourism_bp.route("/roadspending", methods=["GET"])
def get_road_spending():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM RoadSpending;")
        data = cursor.fetchall()
        print("Data:", data)
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the PassengerCars table
@tourism_bp.route("/passengercars", methods=["GET"])
def get_pass_cars():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM PassengerCars;")
        data = cursor.fetchall()
        print("Data:", data)
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the Trips table
@tourism_bp.route("/trips", methods=["GET"])
def get_trips():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Trips;")
        data = cursor.fetchall()
        print("Data:", data)
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500