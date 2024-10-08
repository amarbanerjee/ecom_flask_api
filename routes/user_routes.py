from flask import Blueprint, request, jsonify
from models.user_model import User
from flask_jwt_extended import create_access_token

user_blueprint = Blueprint('user_blueprint', __name__)

# User signup
@user_blueprint.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        # Extract individual fields from data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Call create_user with individual arguments
        user, status_code = User.create_user(username, email, password)
        
        # Return the response
        return jsonify(user), status_code
    
    except Exception as e:
        # If something goes wrong, return an error message
        return jsonify({"error": str(e)}), 500
    

@user_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user, status_code = User.login(email, password)
        return jsonify(user), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
