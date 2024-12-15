# ******************NEW BACKEND*******************
from flask import Flask, send_from_directory
from io import BytesIO
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import base64
import os
import datetime

import numpy as np
from keras.models import load_model
from RunPridiction import makePrediction

app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='')
input_data = {}
scan_data = {}
EPOCHS = 10
# Serve the main index.html file
@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

# Serve static files like CSS, JS, and assets
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('frontend', filename)
    

@app.route('/SimpleScan', methods=['GET', 'POST'])
def SimpleScan():
    input_data['SecuGen_Lic'] = '' #LIC_STR
    input_data['Timeout'] = 10000
    input_data['Quality'] = 50
    input_data['Fake_Detect'] = 0
    input_data['TemplateFormat'] = 'ISO'
    input_data['ImageWSQRate'] = '0.75'
    # 5/15/24 -> At this time, only ImageWSQRate only has 2 options:  0.75 or 2.25
    # input_data['ImageWSQRate'] = '2.25'
    input_data['FakeDetect'] = '0'
    return render_template('SimpleScan.html', user_input=input_data)

@app.route('/Display_Image', methods=['GET', 'POST'])
def DisplayImage():
    # ErrorNumber = int(request.form.get('ErrorCode'))
    # if ErrorNumber > 0:
    #     return render_template('error.html', error=ErrorNumber, errordescription=TranslateErrorNumber(ErrorNumber))
    
    
    bmp_base64_data = request.form.get('BMPBase64')
    if bmp_base64_data:
        # Remove the 'data:image/bmp;base64,' prefix if it exists
        if bmp_base64_data.startswith("data:image/bmp;base64,"):
            bmp_base64_data = bmp_base64_data[len("data:image/bmp;base64,"):]

        # Decode the base64 string to binary data
        bmp_data = base64.b64decode(bmp_base64_data)

        # Specify the file path for saving the BMP image
        uploads_folder = 'uploads'  # Set this to your desired folder
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)  # Create uploads folder if it doesn't exist
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"file_{timestamp}.bmp"
        file_path = os.path.join(uploads_folder, filename)

        # Save the BMP image to the file system
        with open(file_path, 'wb') as bmp_file:
            bmp_file.write(bmp_data)

        print(f"BMP image saved as {file_path}")
        model = load_model(f"Models/test-{EPOCHS}-epochs.h5")

        # Make a prediction
        try:
            prediction = makePrediction(model, file_path)
            np.set_printoptions(suppress=True, linewidth=100)
            print("Prediction:", prediction)
        except FileNotFoundError as e:
            print(e)
        labels = ["A-", "A+", "AB-", "AB+", "B-", "B+","O-", "O+"]
        max_index = np.argmax(prediction[0])  # Use prediction[0] to access the first row
        print(labels[max_index])
        
    scan_data['BloodGroup'] = labels[max_index]
    scan_data['Probability'] =  prediction[0][max_index]
    scan_data['Quality'] = "Working"
    scan_data['Accuracy'] = 0.74
    scan_data['Epochs'] =  EPOCHS
    scan_data['BMPBase64'] = bmp_base64_data
    
    return render_template('display_image.html', metadata=scan_data, user_input=input_data) 

@app.route('/test',methods=['GET'])
def test():
    print(request.form.get('BMPBase64'))
    return "hello"
if __name__ == '__main__':
    app.run(debug=True)
