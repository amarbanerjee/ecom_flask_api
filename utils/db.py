from pymongo import MongoClient

# Centralized MongoDB connection setup
mongo_uri = 'mongodb+srv://amarbanerjee:bRMR3l2ECcYGmJF1@cluster0.rx9fb.mongodb.net/newsletter?retryWrites=true&w=majority&appName=Cluster0'  # Replace with your URI
client = MongoClient(mongo_uri)

# Use a specific database (e.g., 'crud')
db = client['crud']  # Replace with your actual database name