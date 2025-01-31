from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from datetime import datetime, timedelta
import logging
import jwt
from functools import wraps
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import send_from_directory, request
import numpy as np
import io
from pymongo import MongoClient
from details_extractor import extract_details
import pytesseract
from PIL import Image
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Secret key for JWT encoding and decoding
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Load the model
model = load_model(r'C:\Users\X1\pycharmprojects\document_verification_project11\models\document_verification_model.h5')
categories = ['adhar', 'pan', 'driving_license', 'voter_id', 'passport', 'utility']

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.document_verification

# Path to the uploads directory
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the uploads folder if it doesn't exist

# sep9

def preprocess_image(file_path):
    img = Image.open(file_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def extract_text(img):
    return pytesseract.image_to_string(img)
# today i removed


def find_value(text, keyword):
    keyword = keyword.lower()
    regex = re.compile(rf'{keyword}\s*([^\n]+)', re.IGNORECASE)
    match = regex.search(text.lower())
    if match:
        return match.group(1).strip()
    return 'Not Found'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header[len('Bearer '):]
        if not token:
            return jsonify({'error': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if db.users.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    db.users.insert_one({'username': username, 'password': password})
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = db.users.find_one({'username': username, 'password': password})

    if user:
        token = jwt.encode({
            'username': username,
            'exp': datetime.utcnow() + timedelta(minutes=60)

        }, app.config['SECRET_KEY'], algorithm='HS256')

        # Print the token to the terminal
        logger.info(f"Generated JWT Token: {token}")

        return jsonify({'message': 'Login successful', 'token': token})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/verify-token', methods=['GET'])
@token_required
def verify_token():
    return jsonify({'valid': True})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/predict', methods=['POST'])
@token_required
def predict():
    if 'file' not in request.files:
        logger.error('No file part in the request')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        logger.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the file locally to the UPLOAD_FOLDER
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)  # Save the file to disk

        # Determine the full URL path for the uploaded file
        base_url = request.host_url  # This gets the base URL of the current request
        file_url = f'{base_url}uploads/{file.filename}'

        # Log file path and timestamp with full URL
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file_path = os.path.join(UPLOAD_FOLDER, 'upload_log.txt')
        with open(log_file_path, 'a') as f:
            f.write(f"{timestamp} - <a href='{file_url}'>{file.filename}</a>\n")

        # Preprocess the saved image file
        img_array = preprocess_image(file_path)
        predictions = model.predict(img_array)
        class_idx = np.argmax(predictions)
        class_name = categories[class_idx]
        confidence = np.max(predictions)

        # Open the saved image file for extracting text
        with Image.open(file_path) as img:
            text = extract_text(img)

        # Extract details from the text based on the document type
        details = extract_details(text, class_name)

        # Save details into the database
        db.documents.insert_one({
            'document_type': class_name,
            'confidence': float(confidence),
            'text': text,
            'details': details,
            'file_path': file_path,
            'timestamp': timestamp
        })

        # Return the result as JSON response
        return jsonify({
            'document_type': class_name,
            'confidence': float(confidence),
            'extracted_text': text,
            'details': details,
            'file_path': file_path,
            'timestamp': timestamp
        })

    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
