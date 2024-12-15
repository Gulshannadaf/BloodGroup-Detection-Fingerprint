import os
import cv2
from PIL import Image
import numpy as np
from keras.models import load_model

IMG_WIDTH = 96
IMG_HEIGHT = 103
CLACHE_CLIP_LIMIT = 2.0
CLACHE_TILE_GRID_SIZE = 4
ALPHA = 2.5
BETA = 0

def makePrediction(model, img_path):
    IMG_WIDTH = 96
    IMG_HEIGHT = 103

    # Load the image
    img = cv2.imread(img_path)  # Use img_path directly
    if img is None:
        raise FileNotFoundError(f"Image not found at path: {img_path}")

    # Convert RGBA to RGB if needed
    img = img[:, :, :3]  # converting RGBA to RGB
    x_start, y_start = 54, 0     # Top-left corner of the crop
    x_end, y_end = 246, 206      # Bottom-right corner of the crop
    img = img[y_start:y_end, x_start:x_end]
    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    img = np.expand_dims(img, axis=-1) # Add the channel dimension (shape becomes (height, width, 1))
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=CLACHE_CLIP_LIMIT, tileGridSize=(CLACHE_TILE_GRID_SIZE, CLACHE_TILE_GRID_SIZE))
    img = clahe.apply(img)

    # Apply contrast adjustment
    img = cv2.convertScaleAbs(img, alpha=ALPHA, beta=BETA)  # Making image more contrast

    # Ensure the image is in the correct shape for grayscale (height, width, 1)
    

    # Ensure the data type is uint8 for proper conversion to Image
    #img = img.astype(np.uint8)  

    # Convert the image to a PIL Image for further processing (optional)
    #img = Image.fromarray(img)

    # Normalize the image
    img = np.array(img).astype('float32') / 255.0

    # Expand dimensions to match the model's input shape (batch size, height, width, channels)
    img = np.expand_dims(img, axis=0)  # Now the shape is (1, IMG_HEIGHT, IMG_WIDTH, 1)

    # print(img.shape)  # Check the shape of the input image before passing to the model

    # Predict using the model
    prediction = model.predict(img)
    
    return prediction
