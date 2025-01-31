# api/config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_jwt_secret_key')
    MONGO_URI = 'mongodb://localhost:27017/document_verification' 
