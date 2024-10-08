from flask import current_app as app
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

mongo_uri = 'mongodb+srv://amarbanerjee:bRMR3l2ECcYGmJF1@cluster0.rx9fb.mongodb.net/newsletter?retryWrites=true&w=majority&appName=Cluster0'  # Make sure this is correct
client = MongoClient(mongo_uri)
db = client['crud']  # Replace with your actual database name
product_collection = db['products']

def add_product(product_data):
    # product = {
    #     "name": product_data['name'],
    #     "price": product_data['price'],
    #     "description": product_data['description'],
    #     "category": product_data['category'],
    #     "stock": product_data['stock']
    # }
    result = product_collection.insert_one(product_data)
    return result.inserted_id

def get_all_products():
    products = list(product_collection.find({}))  # Fetch all products
    serialized_products = [serialize_product(product) for product in products]  # Serialize each product
    return serialized_products  # Return the serialized list of products


def serialize_product(product):
    """
    Convert MongoDB ObjectId and datetime objects to JSON serializable format.
    """
    if '_id' in product:
        product['_id'] = str(product['_id'])  # Convert ObjectId to string
    if 'createdAt' in product and isinstance(product['createdAt'], datetime):
        product['createdAt'] = product['createdAt'].strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
    if 'updatedAt' in product and isinstance(product['updatedAt'], datetime):
        product['updatedAt'] = product['updatedAt'].strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
    return product


# Function to get a product by ID
def get_product_by_id(product_id):
    return product_collection.find_one({"_id": ObjectId(product_id)})

# Function to update a product by ID
def update_product_in_db(product_id, updated_data):
    # Use MongoDB's update_one method to update the product
    result = product_collection.update_one(
        {"_id": ObjectId(product_id)}, 
        {"$set": updated_data}
    )
    
    # Return the updated product
    if result.modified_count > 0:
        return get_product_by_id(product_id)  # Return the updated product
    else:
        return None
    

# Function to delete a product by ID
def delete_product_by_id(product_id):
    result = product_collection.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count  # Returns the number of documents deleted (1 if successful, 0 if not)