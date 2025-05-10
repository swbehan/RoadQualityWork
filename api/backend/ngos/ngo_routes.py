from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error

ngos = Blueprint("ngos", __name__)


@ngos.route("/ngos", methods=["GET"])
def get_all_ngos():
    try:
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        country = request.args.get("country")
        focus_area = request.args.get("focus_area")
        founding_year = request.args.get("founding_year")

        # Base query
        query = "SELECT * FROM WorldNGOs WHERE 1=1"
        params = []

        # Add filters if provided
        if country:
            query += " AND Country = %s"
            params.append(country)
        if focus_area:
            query += " AND Focus_Area = %s"
            params.append(focus_area)
        if founding_year:
            query += " AND Founding_Year = %s"
            params.append(founding_year)

        cursor.execute(query, params)
        ngos = cursor.fetchall()
        cursor.close()

        return jsonify(ngos), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@ngos.route("/ngos/<int:ngo_id>", methods=["GET"])
def get_ngo(ngo_id):
    try:
        cursor = db.get_db().cursor()

        # Get NGO details
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        ngo = cursor.fetchone()

        if not ngo:
            return jsonify({"error": "NGO not found"}), 404

        # Get associated projects
        cursor.execute("SELECT * FROM Projects WHERE NGO_ID = %s", (ngo_id,))
        projects = cursor.fetchall()

        # Get associated donors
        cursor.execute("SELECT * FROM Donors WHERE NGO_ID = %s", (ngo_id,))
        donors = cursor.fetchall()

        # Combine all data
        ngo["projects"] = projects
        ngo["donors"] = donors

        cursor.close()
        return jsonify(ngo), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@ngos.route("/ngos", methods=["POST"])
def create_ngo():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["Name", "Country", "Founding_Year", "Focus_Area", "Website"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Insert new NGO
        query = """
        INSERT INTO WorldNGOs (Name, Country, Founding_Year, Focus_Area, Website)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["Name"],
                data["Country"],
                data["Founding_Year"],
                data["Focus_Area"],
                data["Website"],
            ),
        )

        db.get_db().commit()
        new_ngo_id = cursor.lastrowid
        cursor.close()

        return (
            jsonify({"message": "NGO created successfully", "ngo_id": new_ngo_id}),
            201,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500


@ngos.route("/ngos/<int:ngo_id>", methods=["PUT"])
def update_ngo(ngo_id):
    try:
        data = request.get_json()

        # Check if NGO exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["Name", "Country", "Founding_Year", "Focus_Area", "Website"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(ngo_id)
        query = f"UPDATE WorldNGOs SET {', '.join(update_fields)} WHERE NGO_ID = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "NGO updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@ngos.route("/ngos/<int:ngo_id>/projects", methods=["GET"])
def get_ngo_projects(ngo_id):
    try:
        cursor = db.get_db().cursor()

        # Check if NGO exists
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Get all projects for the NGO
        cursor.execute("SELECT * FROM Projects WHERE NGO_ID = %s", (ngo_id,))
        projects = cursor.fetchall()
        cursor.close()

        return jsonify(projects), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@ngos.route("/ngos/<int:ngo_id>/donors", methods=["GET"])
def get_ngo_donors(ngo_id):
    try:
        cursor = db.get_db().cursor()

        # Check if NGO exists
        cursor.execute("SELECT * FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Get all donors for the NGO
        cursor.execute("SELECT * FROM Donors WHERE NGO_ID = %s", (ngo_id,))
        donors = cursor.fetchall()
        cursor.close()

        return jsonify(donors), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
