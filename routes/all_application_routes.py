from flask import request, jsonify,Blueprint
from services.db_service import get_all_applications
get_application_bp = Blueprint('get_all_applications', __name__)

@get_application_bp.route('/get_all_applications', methods=['GET'])
def get_all_application():
    try:
        # Fetch all applications from the database
        applications = get_all_applications()

        # Format the result as a list of dictionaries (MongoDB's ObjectId needs conversion)
        formatted_applications = [
            {
                "_id": str(app["_id"]),
                "name": app.get("name", ""),
                "email": app.get("email", ""),
                "resume": app.get("resume", "")
            } for app in applications
        ]

        return jsonify({
            "success": True,
            "data": formatted_applications
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
 

 