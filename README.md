# Document Verification System

## Overview
The Document Verification System is a deep-learning-based solution that automates the classification, extraction, and validation of key information from various document types, including Aadhaar, PAN, driving license, voter ID, passport, and utility bills. Designed for applications in banking, KYC, and identity validation, this system offers enhanced speed, accuracy, and reliability in document verification processes.

Using a Convolutional Neural Network (CNN), the system identifies the type of document uploaded via a custom form interface. After classification, Optical Character Recognition (OCR) powered by Pytesseract extracts essential text details, such as document numbers and names, which are then validated using predefined patterns. To improve model robustness, data augmentation techniques like rotation, zooming, shifting, and flipping are employed, simulating real-world variations in document presentation.

## Key Features
- **Automated Document Classification**: Classifies documents by type (e.g., Aadhaar, PAN) using a CNN model.
- **OCR and Data Validation**: Extracts and validates key text information to ensure document authenticity.
- **Data Augmentation**: Enhances model performance across diverse document formats and conditions.
- **Custom Form Integration**: Predicts document type and validates data directly through an intuitive upload interface.
- **Scalable Design**: Easily extendable to accommodate additional document types or verification criteria.

This project is ideal for large-scale applications in industries requiring reliable, fast, and accurate document verification.

## Installation and Usage

### Step 1: Install Requirements
Install the necessary packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 2: Data Collection and Preprocessing
Navigate to the preprocessing folder and run the data preprocessing script:
```bash
cd preprocessing
python data_preprocessing.py
```

### Step 3: Train the Model
Go to the `model` folder and run the model training script:
```bash
cd model
python document_verification_model.py
```

### Step 4: Run the API
After training the model, navigate to the `api` folder and run the API:
```bash
cd api
python app.py
```

### Step 5: Run the Frontend
Navigate to the frontend directory and install the necessary dependencies. Then, start the frontend server:
```bash
npm install
npm start
```

### MongoDB Connection
Ensure that you have connected to MongoDB for storing and managing verification data.

## Project Structure
- **preprocessing**: Scripts for data collection and preprocessing.
- **model**: Scripts for training the document verification CNN model.
- **api**: Contains `app.py`, which hosts the backend API.
- **frontend**: Frontend code to provide an upload interface for users.

## Technologies Used
- **Deep Learning**: Convolutional Neural Network (CNN) with TensorFlow/Keras.
- **OCR**: Pytesseract for extracting text from documents.
- **Data Augmentation**: Techniques like rotation, zooming, shifting, and flipping to enhance model performance.
- **MongoDB**: Database for storing verification data.
- **Flask**: Backend framework to host the API.
- **React**: Frontend framework for the document upload interface.

"# python_project" 
