import os
import cv2
from PIL import Image
import numpy as np
from keras.models import load_model


def makePrediction(model,img):
    IMG_WIDTH = 96
    IMG_HEIGHT = 103

    img = cv2.imread(os.path.join(subfolder_path, filename))
    img = img[:, :, :3]  # converting RGBA to RGB
    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    img = Image.fromarray(img)
    img = np.array(img)
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0) # Increases one more dimension in image for model
    prediction= model.predict(img)
    
    return prediction