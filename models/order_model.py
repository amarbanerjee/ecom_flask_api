from flask import current_app as app
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from utils.db import db  # Import the centralized MongoDB connection

order_collection = db['orders']

def create_order(order_data):
    order_data['created_at'] = datetime.utcnow()  # Add created timestamp
    order_data['status'] = order_data.get('status', 'Pending')  # Default to 'Pending' if not provided

    # order = {
    #     "user_id": order_data['user_id'],
    #     "products": order_data['products'],
    #     "status": "pending",
    #     "total_price": order_data['total_price'],
    #     "created_at": order_data['created_at']
    # }
    order_collection.insert_one(order_data)
    return order_data

def get_orders_by_status(status):
    return list(order_collection.find({"status": status}))

def update_order_status(order_id, status):
    order_collection.update_one({"order_id": order_id}, {"$set": {"status": status}})
    return {"msg": "Order updated"}

def get_all_orders():
    return list(order_collection.find())

def get_order_by_id(order_id):
    return order_collection.find_one({"order_id": order_id})

def add_order(order_data):
    return order_collection.insert_one(order_data)
