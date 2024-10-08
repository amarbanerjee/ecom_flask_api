from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

# MongoDB setup
mongo_uri = 'mongodb+srv://amarbanerjee:bRMR3l2ECcYGmJF1@cluster0.rx9fb.mongodb.net/newsletter?retryWrites=true&w=majority&appName=Cluster0'  # Make sure this is correct
client = MongoClient(mongo_uri)
db = client['crud']  # Replace with your actual database name
users_collection = db['users']

class User:
    @staticmethod
    def create_user(username, email, password):
        # Simple validation
        if not username or not email or not password:
            return {"error": "Missing username, email, or password."}, 400

        # Hashing the password before storing it
        hashed_password = generate_password_hash(password)

        # Checking if the user already exists
        if users_collection.find_one({"email": email}):
            return {"error": "User with this email already exists."}, 400

        # Creating a new user object
        new_user = {
            'username': username,
            'email': email,
            'password': hashed_password  # Storing the hashed password
        }

        # Inserting into the database
        result = users_collection.insert_one(new_user)

        # Return the created user info (without the password)
        return {
            "id": str(result.inserted_id),
            "username": username,
            "email": email
        }, 201  # Return the status code along with the user info

    
    @staticmethod
    def get_user_by_username(username):
        return users_collection.find_one({'username': username})

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user['password'], password)
    

    @staticmethod
    def login(email, password):
        user = users_collection.find_one({"email": email})
        if not user:
            return {"error": "User not found."}, 404

        # Check the password against the hashed password
        if not check_password_hash(user['password'], password):
            return {"error": "Invalid password."}, 401

        # Create JWT token
        access_token = create_access_token(identity={"id": str(user['_id']), "username": user['username'], "email": user['email']})

        return {
            "access_token": access_token,
            "user": {
                "id": str(user['_id']),
                "username": user['username'],
                "email": user['email']
            }
        }, 200
