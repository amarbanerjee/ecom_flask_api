from flask import Blueprint, request, jsonify
from utils.auth import admin_required
from models.offer_model import Offer

offer_blueprint = Blueprint('offer_blueprint', __name__)

# Create an offer (admin only)
@offer_blueprint.route('/create', methods=['POST'])
@admin_required
def create_new_offer():
    data = request.get_json()
    offer = Offer.create_offer(data)
    return jsonify(offer), 201

# Get all offers
@offer_blueprint.route('/offers', methods=['GET'])
def get_offers():
    offers = Offer.get_offers()
    return jsonify(offers), 200

