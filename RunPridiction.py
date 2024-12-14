import os
import cv2
from PIL import Image
import numpy as np
from keras.models import load_model


def makePrediction(model, img_path):
    IMG_WIDTH = 96
    IMG_HEIGHT = 103

    # Load the image
    img = cv2.imread(img_path)  # Use img_path directly
    if img is None:
        raise FileNotFoundError(f"Image not found at path: {img_path}")

    # Convert RGBA to RGB if needed
    if img.shape[-1] == 4:  # If image has 4 channels (RGBA)
        img = img[:, :, :3]

    # Resize the image
    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

    # Normalize the image
    img = img.astype('float32') / 255.0

    # Expand dimensions to match the model's input shape
    img = np.expand_dims(img, axis=0)

    # Predict using the model
    prediction = model.predict(img)

    return prediction





#def makePrediction(model,img):
    # IMG_WIDTH = 96
    # IMG_HEIGHT = 103
    # img = cv2.imread(file)

    # #img = cv2.imread(os.path.join(subfolder_path, filename))
    # img = img[:, :, :3]  # converting RGBA to RGB
    # img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    # img = Image.fromarray(img)
    # img = np.array(img)
    # img = img.astype('float32') / 255.0
    # img = np.expand_dims(img, axis=0) # Increases one more dimension in image for model
    # prediction= model.predict(img)
    
    # return prediction