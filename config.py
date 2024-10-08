import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')