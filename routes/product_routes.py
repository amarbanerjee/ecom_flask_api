import os
from flask import Blueprint, request, jsonify
from models.product_model import add_product, get_all_products,update_product_in_db, get_product_by_id,delete_product_by_id,get_product_by_id
from utils.auth import admin_required
from werkzeug.utils import secure_filename
from datetime import datetime
from bson import ObjectId



product_blueprint = Blueprint('product_blueprint', __name__)

# Define the directory to save uploaded images
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Add a new product
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Helper function to make MongoDB data JSON serializable
def serialize_product(product):
    product['_id'] = str(product['_id'])
    return product

# Add a new product endpoint (with image upload)
@product_blueprint.route('/add', methods=['POST'])
@admin_required
def add_new_product():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided."}), 400
    
    image = request.files['image']

    # Check if the file is allowed
    if image and allowed_file(image.filename):
        # Secure the file name
        filename = secure_filename(image.filename)
        
        # Save the image to the UPLOAD_FOLDER
        image.save(os.path.join(UPLOAD_FOLDER, filename))
        
        # Retrieve other product details from the form (assuming form-data)
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        
        # Validate required fields
        if not title or not description or not price:
            return jsonify({"error": "Missing required product fields."}), 400
        
        # Create product data for saving in MongoDB
        product_data = {
            'title': title,
            'description': description,
            'price': float(price),  # Assuming price is numeric
            'image': filename,  # Save the image file name
            'createdAt': datetime.now(),
            'updatedAt': datetime.now()
        }
        
        # Save product in MongoDB
        product_id = add_product(product_data)
        
        return jsonify({"message": "Product added successfully", "product_id": str(product_id)}), 201
    else:
        return jsonify({"error": "Invalid file type."}), 400
    

# Get all products
@product_blueprint.route('/', methods=['GET'])
def get_products():
    auth_header = request.headers.get('Authorization')
    print(f"Authorization header: {auth_header}")
    products = get_all_products()
    print(products)
    return jsonify(products), 200

@product_blueprint.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    products = serialize_product(get_product_by_id(product_id))
    print(products)
    return jsonify(products), 200


# Update product by ID
@product_blueprint.route('/update/<product_id>', methods=['PUT'])
# @admin_required
def update_product(product_id):
    # Fetch the existing product from the database
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found."}), 404

    # Get the form data
    title = request.form.get('title', product['title'])
    description = request.form.get('description', product['description'])
    price = request.form.get('price', product['price'])

    # Handle the image file upload (optional)
    if 'image' in request.files and request.files['image']:
        image = request.files['image']
        if image and allowed_file(image.filename):
            # Secure the file name
            filename = secure_filename(image.filename)

            # Save the new image to the UPLOAD_FOLDER
            image.save(os.path.join(UPLOAD_FOLDER, filename))

            # Optionally, delete the old image file if needed:
            # os.remove(os.path.join(UPLOAD_FOLDER, product['image']))

        else:
            return jsonify({"error": "Invalid file type."}), 400
    else:
        filename = product['image']  # Keep the old image if no new image is uploaded

    # Prepare the updated product data
    updated_product_data = {
        'title': title,
        'description': description,
        'price': float(price),
        'image': filename,
        'updatedAt': datetime.now()  # Update the timestamp
    }

    # Update the product in MongoDB
    updated_product = update_product_in_db(product_id, updated_product_data)

    # Convert ObjectId to string for JSON serialization
    if updated_product:
        serialized_product = serialize_product(updated_product)
        return jsonify({"message": "Product updated successfully", "product": serialized_product}), 200
    else:
        return jsonify({"error": "Failed to update product."}), 500
    

# Delete product by ID
@product_blueprint.route('/delete/<product_id>', methods=['DELETE'])
# @admin_required
def delete_product(product_id):
    # Fetch the existing product from the database
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found."}), 404

    # Remove the product's image file from the local directory if it exists
    if product.get('image'):
        image_path = os.path.join(UPLOAD_FOLDER, product['image'])
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete the product from the database
    deleted_count = delete_product_by_id(product_id)

    if deleted_count > 0:
        return jsonify({"message": "Product deleted successfully."}), 200
    else:
        return jsonify({"error": "Failed to delete product."}), 500


