from flask_pymongo import ObjectId

class Offer:
    @staticmethod
    def create_offer(product_id, discount_percentage, start_date, end_date):
        offer_data = {
            'product_id': product_id,
            'discount_percentage': discount_percentage,
            'start_date': start_date,
            'end_date': end_date
        }
        return mongo.db.offers.insert_one(offer_data)

    @staticmethod
    def get_offers():
        offers = mongo.db.offers.find()
        offer_list = []
        for offer in offers:
            offer_list.append({
                'id': str(offer['_id']),
                'product_id': offer['product_id'],
                'discount_percentage': offer['discount_percentage'],
                'start_date': offer['start_date'],
                'end_date': offer['end_date']
            })
        return offer_list

    @staticmethod
    def get_offer_by_product(product_id):
        return mongo.db.offers.find_one({'product_id': product_id})

    @staticmethod
    def delete_offer(offer_id):
        return mongo.db.offers.delete_one({'_id': ObjectId(offer_id)})
