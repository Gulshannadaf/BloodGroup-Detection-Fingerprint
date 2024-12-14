# from flask import Flask, render_template, jsonify
# import os
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# from PIL import Image
# import numpy as np

# # If using a hardware scanner library like PyFingerprint:
# # from pyfingerprint.pyfingerprint import PyFingerprint

# app = Flask(__name__)

# # Load your trained ML model
# MODEL_PATH = 'models/trained_model.h5'
# model = load_model(MODEL_PATH)

# # Route for the homepage
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Route to capture fingerprint and detect blood group
# @app.route('/capture_and_detect', methods=['POST'])
# def capture_and_detect():
#     try:
#         # Step 1: Capture fingerprint image using the hardware scanner
#         # Uncomment the following lines if using a library like PyFingerprint
#         # scanner = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
#         # if scanner.readImage():
#         #     imagePath = 'uploads/fingerprint.bmp'
#         #     scanner.downloadImage(imagePath)
#         #     fingerprint_image = Image.open(imagePath)
        
#         # For now, simulate image capture (Replace with actual hardware code)
#         fingerprint_image = Image.open('sample_fingerprint.jpg')  # Replace this with scanner output
#         fingerprint_image = fingerprint_image.convert('RGB')
#         fingerprint_image = fingerprint_image.resize((224, 224))  # Match model's input shape
        
#         # Step 2: Preprocess the fingerprint image
#         img_array = np.array(fingerprint_image) / 255.0  # Normalize pixel values
#         img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

#         # Step 3: Use the trained model for prediction
#         predictions = model.predict(img_array)
#         blood_group = decode_predictions(predictions)  # Decode the model's predictions

#         return jsonify({'blood_group': blood_group})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Custom function to decode model predictions
# def decode_predictions(predictions):
#     blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']  # Adjust based on your model
#     predicted_index = np.argmax(predictions)
#     return blood_groups[predicted_index]

# if __name__ == '__main__':
#     app.run(debug=True)
 
from flask import Flask, request, jsonify, render_template
import random  # For blood group simulation

app = Flask(__name__)
@app.route('/')
def home():
    return "Welcome to the Blood Group Detection API! Use the /capture_and_detect endpoint."


# Simulated blood group detection logic
def detect_blood_group(fingerprint_data):
    # In reality, process the fingerprint_data with SecuGen SDK here
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    return random.choice(blood_groups)

# API Endpoint to capture and detect blood group
@app.route('/capture_and_detect', methods=['POST'])
def capture_and_detect():
    try:
        # Simulate receiving fingerprint data
        fingerprint_data = request.get_json().get('fingerprint_data', None)
        if not fingerprint_data:
            return jsonify({"error": "Fingerprint data not provided"}), 400

        # Process fingerprint data to detect blood group
        blood_group = detect_blood_group(fingerprint_data)

        return jsonify({"blood_group": blood_group}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
