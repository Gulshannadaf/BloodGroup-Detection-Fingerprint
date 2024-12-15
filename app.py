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

app = Flask(__name__, static_folder='frontend', static_url_path='')
input_data = {}
response_data = {}
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
    ErrorNumber = int(request.form.get('ErrorCode'))
    if ErrorNumber > 0:
        return render_template('error.html', error=ErrorNumber, errordescription=TranslateErrorNumber(ErrorNumber))
    blood_group = ''
    input_data['Timeout'] = request.form.get('timeout')
    input_data['Quality'] = request.form.get('quality')
    input_data['Fake_Detect'] = request.form.get('fake_detect')
    input_data['TemplateFormat'] = request.form.get('template_format')
    input_data['ImageWSQRate'] = request.form.get('imagewsqrate')

    # Extract data coming from the external API
    response_data['Manufacturer'] = request.form.get('Manufacturer')
    response_data['Model'] = request.form.get('Model')
    response_data['SerialNumber'] =  blood_group#request.form.get('SerialNumber')
    response_data['ImageWidth'] = request.form.get('ImageWidth')
    response_data['ImageHeight'] = request.form.get('ImageHeight')
    response_data['ImageDPI'] = request.form.get('ImageDPI')
    response_data['ImageQuality'] = request.form.get('ImageQuality')
    response_data['NFIQ'] = request.form.get('NFIQ')
    response_data['TemplateBase64'] = request.form.get('TemplateBase64')
    response_data['WSQImageSize'] = request.form.get('WSQImageSize')
    response_data['WSQImage'] = request.form.get('WSQImage')
    response_data['BMPBase64'] = request.form.get('BMPBase64')
    
    
    bmp_base64_data = response_data.get('BMPBase64')
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
        model = load_model("test-4-epochs.h5")

        # Make a prediction
        try:
            prediction = makePrediction(model, file_path)
            np.set_printoptions(suppress=True, linewidth=100)
            print("Prediction:", prediction)
        except FileNotFoundError as e:
            print(e)
        response_data['SerialNumber'] =  prediction[0][1]#request.form.get('SerialNumber')
    
    
    return render_template('display_image.html', metadata=response_data, user_input=input_data) 

@app.route('/test',methods=['GET'])
def test():
    print(request.form.get('BMPBase64'))
    return "hello"
if __name__ == '__main__':
    app.run(debug=True)
