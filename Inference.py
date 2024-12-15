# import os
# from RunPridiction import makePrediction
# import numpy as np
# from keras.models import load_model

# model = load_model("test1.h5")


# prediction = np.array(makePrediction(model,'Data\A-\cluster_1_67.BMP'))
# np.set_printoptions(suppress=True,linewidth=10)
# print (prediction)


import numpy as np
from keras.models import load_model
from RunPridiction import makePrediction


EPOCHS = 12
# Load the trained modelp
model = load_model(f"Models/test-{EPOCHS}-epochs.h5")

while(1):
# Provide the path to the image you want to predict
#image_path = r"uploads/download.bmp"
    #image_path = r"Data\A-\cluster_1_83.BMP"
    image_path = input("Enter relative Path: ")
    # Make a prediction
    try:
        prediction = makePrediction(model, image_path)
        np.set_printoptions(suppress=True, linewidth=100)
        print("Prediction:", prediction)
        labels = ["A-", "A+", "AB-", "AB+", "B-", "B+","O-", "O+"]
        max_index = np.argmax(prediction[0])  # Use prediction[0] to access the first row
        print(labels[max_index])
    except FileNotFoundError as e:
        print(e)
