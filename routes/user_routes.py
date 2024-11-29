# from flask import Blueprint, jsonify

# # Define blueprint
# user_bp = Blueprint('user', __name__)

# @user_bp.route('', methods=['GET'])
# def get_users():
#     return jsonify({'message': 'Users fetched successfully'})

from flask import Blueprint, request, jsonify
from services.db_service import insert_application, get_all_applications

# Create a Blueprint
user_bp = Blueprint('user', __name__)

# Example route
@user_bp.route('/users', methods=['GET'])
def get_users():
    # Your logic to get users
    return jsonify({'message': 'Users fetched successfully'})

# Add more routes as needed

