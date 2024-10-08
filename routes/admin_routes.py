from flask import Blueprint, request, jsonify
from models.admin_model import create_admin, get_admin_by_email, verify_password
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
import re




# Define Blueprint
admin_blueprint = Blueprint('admin_blueprint', __name__)

# Helper function for email validation
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Admin Signup Route
@admin_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Validate data
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({"error": "Invalid input."}), 400
    
    if not is_valid_email(data.get('email')):
        return jsonify({"error": "Invalid email format."}), 400
    
    if len(data.get('password')) < 6:
        return jsonify({"error": "Password must be at least 6 characters long."}), 400
    
    # Check if the admin already exists
    if get_admin_by_email(data.get('email')):
        return jsonify({"error": "Admin with this email already exists."}), 400

    # Create the admin
    new_admin = create_admin(data)
    return jsonify({"message": "Admin registered successfully.", "admin": new_admin}), 201

# Admin Login Route
@admin_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    
    # Validate data
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required."}), 400

    # Fetch admin from the database
    admin = get_admin_by_email(data.get('email'))
    if not admin:
        return jsonify({"error": "Admin not found."}), 404

    # Verify password
    if not verify_password(admin['password'], data.get('password')):
        return jsonify({"error": "Invalid password."}), 401

    # Create JWT token with admin info and expiration
    access_token = create_access_token(
        identity={"username": admin['username'], "email": admin['email'], "role": admin['role']},
        expires_delta=timedelta(hours=24)
    )
    
    return jsonify({"message": "Login successful", "token": access_token, "admin": admin}), 200

# Protected Route (Example)
@admin_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "This is a protected route!"}), 200