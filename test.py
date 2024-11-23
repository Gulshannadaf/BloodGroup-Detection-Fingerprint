import os
#import random

import cv2
import numpy as np
from PIL import Image

#import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from tensorflow import keras
from keras import layers, models
from keras.preprocessing.image import img_to_array, load_img
from keras.utils import to_categorical

# from tensorflow import keras
# from tensorflow.keras import layers 
# from tensorflow.keras import layers, models
# from tensorflow.keras.utils import to_categorical

RESO = 320

dataset_path = "Data/"

def load_images_from_folder(folder):
    images = []
    labels = []
    for label, subfolder in enumerate(["A-", "A+", "AB-", "AB+", "B-", "B+", "O-", "O+"]):
        subfolder_path = os.path.join(folder, subfolder)
        for filename in os.listdir(subfolder_path):
            img = cv2.imread(os.path.join(subfolder_path, filename), cv2.IMREAD_UNCHANGED)  # Load image
            if img is not None:
                print(f"Loaded {filename} with shape: {img.shape}")  # Print the shape of the image
                img = Image.fromarray(img)
                img = img.resize((RESO, RESO))
                img = np.array(img)

                # If the image is grayscale (1 channel), convert it to 3 channels
                if img.ndim == 2:  # Grayscale image (2D)
                    img = np.stack((img,) * 3, axis=-1)  # Convert to 3 channels by stacking

                images.append(img)
                labels.append(label)
            else:
                print(f"Failed to load {filename}.")
    return np.array(images), np.array(labels)

# Load images and check shapes
images, labels = load_images_from_folder(dataset_path)
