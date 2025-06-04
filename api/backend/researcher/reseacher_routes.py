from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

researcher_api = Blueprint("researcher_api", __name__)

# --- Table Setup Route (for testing/initialization) ---
@researcher_api.route("/setup_tables", methods=["GET"])
def setup_tables():
    conn = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        
        # Just verify tables exist
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        current_app.logger.info(f"Connected to EuroTour database. Found {len(tables)} tables.")
        
        cursor.close()
        return jsonify({
            "message": "Successfully connected to EuroTour database!",
            "tables_found": len(tables)
        }), 200
        
    except Error as e:
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@researcher_api.route("/new_post", methods=["POST"])
def new_post():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["Title", "Research", "AuthorID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Insert new Post
        query = """
        INSERT INTO ResearchFindings (Title, Research, AuthorID)
        VALUES (%s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["Title"],
                data["Research"],
                data["AuthorID"]
            ),
        )

        db.get_db().commit()
        new_research_post_id = cursor.lastrowid
        cursor.close()

        return (
            jsonify({"message": "Post created successfully", "ResearchPostID": new_research_post_id}),
            201,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500


@researcher_api.route("/debug_researchers", methods=["GET"])
def debug_researchers():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Researcher;")
        researchers = cursor.fetchall()
        cursor.close()
        return jsonify({"researchers": researchers})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@researcher_api.route("/get_all_posts", methods=["GET"])
def get_all_posts():
    try:
        cursor = db.get_db().cursor()
        
        # Get all records from ResearchFindings
        query = """
            SELECT 
                rf.ResearchPostID,
                rf.Title,
                rf.PostDate,
                rf.Research,
                rf.AuthorID,
                r.ResearcherName,
                r.FieldOfStudy
            FROM ResearchFindings rf
            LEFT JOIN Researcher r ON rf.AuthorID = r.ResearcherID
            ORDER BY rf.PostDate DESC
        """
        cursor.execute(query)
        posts = cursor.fetchall()
        
        cursor.close()
        
        return jsonify({
            "message": f"Found {len(posts)} posts",
            "posts": posts
        }), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

@researcher_api.route("/delete_post/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        
        # First check if post exists
        check_query = "SELECT ResearchPostID FROM ResearchFindings WHERE ResearchPostID = %s"
        cursor.execute(check_query, (post_id,))
        post = cursor.fetchone()
        
        if not post:
            cursor.close()
            return jsonify({"error": "Post not found"}), 404
        
        # Delete associated files first (to maintain referential integrity)
        delete_files_query = "DELETE FROM Files WHERE ResearchPostID = %s"
        cursor.execute(delete_files_query, (post_id,))
        
        # Then delete the post
        delete_post_query = "DELETE FROM ResearchFindings WHERE ResearchPostID = %s"
        cursor.execute(delete_post_query, (post_id,))
        
        conn.commit()
        cursor.close()
        
        return jsonify({"message": f"Post {post_id} deleted successfully"}), 200
        
    except Error as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500