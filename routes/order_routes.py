from flask import Blueprint, request, jsonify
from utils.auth import admin_required
from models.order_model import create_order, get_orders_by_status, update_order_status,get_all_orders,get_order_by_id

admin_order_blueprint = Blueprint('admin_order_blueprint', __name__)

# # Create a new order
@admin_order_blueprint.route('/create-order', methods=['POST'])
def create_new_order():
    data = request.get_json()
    order = create_order(data)
    order['_id'] = str(order['_id'])
    return jsonify(order), 201

# # # Get orders by status (admin only)
@admin_order_blueprint.route('/status/<status>', methods=['GET'])
@admin_required
def get_orders_by_status_endpoint(status):
    orders = get_orders_by_status(status)
    return jsonify(orders), 200


@admin_order_blueprint.route('/change-status/<order_id>', methods=['PUT', 'OPTIONS'],endpoint='change_status')
# @admin_required
def change_order_status_endpoint(order_id):
    if request.method == 'OPTIONS':
        # Handle the preflight request and return a 200 OK with appropriate CORS headers
        response = jsonify({"message": "Preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "PUT, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200
    elif request.method == 'PUT':
        # Logic to update the order status
        data = request.get_json()
        data = request.get_json()
        updated_order = update_order_status(order_id, data.get('status'))
        return jsonify(updated_order), 200
        

    

# # # Update order status (admin only)
# @admin_order_blueprint.route('/change-order-status/<order_id>', methods=['PUT'])
# @admin_required
# def update_order_status_endpoint(order_id):
#     data = request.get_json()
#     updated_order = update_order_status(order_id, data['status'])
#     return jsonify(updated_order), 200


# Order Listing
@admin_order_blueprint.route('/', methods=['GET'])
def list_orders():
    orders = get_all_orders()
    # Convert ObjectId to string before returning JSON
    for order in orders:
        order['_id'] = str(order['_id'])
    return jsonify(orders), 200

# Order Details
@admin_order_blueprint.route('/details/<order_id>', methods=['GET'])
def order_details(order_id):
    order = get_order_by_id(order_id)
    if order:
        order['_id'] = str(order['_id'])  # Convert ObjectId to string
        return jsonify(order), 200
    else:
        return jsonify({"error": "Order not found"}), 404
