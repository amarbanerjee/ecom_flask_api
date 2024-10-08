from bson import ObjectId
from datetime import datetime

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
