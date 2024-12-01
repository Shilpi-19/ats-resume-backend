from flask import request, jsonify,Blueprint
from services.db_service import get_status
email_bp=Blueprint('email_bp', __name__)

# Define the route for checking email with a GET request
@email_bp.route('/check_email', methods=['GET'])
def check_email():
    try:
        # Get email from the query parameters
        email = request.args.get('email')
        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Fetch the user document using the helper function
        user = get_status(email)

        if not user:
            return jsonify({"error": "Email not found"}), 404

        # Extract relevant details from the resume field
        resume = user.get("resume", {})
        response = {
            "name": user.get("name"),
            "email": user.get("email"),
            "is_ats_friendly": resume.get("is_ats_friendly", False),
            "missing_keywords": resume.get("missing_keywords", []),
            "format_issues": resume.get("format_issues", []),
            "recommendations": resume.get("recommendations", []),
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


