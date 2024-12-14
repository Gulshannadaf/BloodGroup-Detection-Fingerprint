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

# Load the trained model
model = load_model("test1.h5")

# Provide the path to the image you want to predict
image_path = r"Data\A-\cluster_1_67.BMP"

# Make a prediction
try:
    prediction = makePrediction(model, image_path)
    np.set_printoptions(suppress=True, linewidth=100)
    print("Prediction:", prediction)
except FileNotFoundError as e:
    print(e)
