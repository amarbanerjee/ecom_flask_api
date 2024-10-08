from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from pymongo import MongoClient

# Assume mongo is initialized in your app
mongo_uri = 'mongodb+srv://amarbanerjee:bRMR3l2ECcYGmJF1@cluster0.rx9fb.mongodb.net/newsletter?retryWrites=true&w=majority&appName=Cluster0'  # Make sure this is correct
client = MongoClient(mongo_uri)
db = client['crud']  # Replace with your actual database name
admin_collection = db['admins']

# Create an admin account (Sign up)
def create_admin(data):
    # print(data)
    hashed_password = generate_password_hash(data.get('password'))
    # hashed_password = data.get('password')
    new_admin = {
        "username": data.get('username'),
        "email": data.get('email'),
        "password": hashed_password,
        "role": data.get('role', 'admin')  # Default role is 'admin'
    }
    admin_id = admin_collection.insert_one(new_admin).inserted_id
    new_admin['_id'] = str(admin_id)  # Convert ObjectId to string
    return new_admin

# Get admin by email (Login)
def get_admin_by_email(email):
    admin = admin_collection.find_one({"email": email})
    if admin:
        admin['_id'] = str(admin['_id'])  # Convert ObjectId to string
    return admin

# Verify password
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)
    