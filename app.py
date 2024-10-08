from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

# MongoDB connection URL
app.config.from_object(Config)
#mongo = PyMongo(app)

# Secret key for JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'  
jwt = JWTManager(app)

# Registering blueprints (routes)
from routes.product_routes import product_blueprint
from routes.admin_routes import admin_blueprint
from routes.user_routes import user_blueprint
from routes.offer_routes import offer_blueprint
from routes.order_routes import admin_order_blueprint


app.register_blueprint(product_blueprint, url_prefix="/api/products")
app.register_blueprint(admin_blueprint, url_prefix="/api/admin")
app.register_blueprint(user_blueprint, url_prefix="/api/users")
app.register_blueprint(offer_blueprint, url_prefix="/api/offers")
app.register_blueprint(admin_order_blueprint, url_prefix='/api/orders')

if __name__ == "__main__":
    app.run(debug=True)
