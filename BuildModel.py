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
    for label, subfolder in enumerate(["A-", "A+", "AB-", "AB+", "B-", "B+","O-", "O+"]):
        subfolder_path = os.path.join(folder, subfolder)
        for filename in os.listdir(subfolder_path):
            img = cv2.imread(os.path.join(subfolder_path, filename))
            img = Image.fromarray(img)
            img = img.resize((RESO,RESO))
            img = np.array(img)
            images.append(img)
            labels.append(label)
    return np.array(images), np.array(labels)

images, labels = load_images_from_folder(dataset_path)

images = images.astype('float32') / 255.0

labels = to_categorical(labels)

train_images, val_images, train_labels, val_labels = train_test_split(
    images, labels, test_size=0.2, random_state=42)






# Define the model architecture
model = models.Sequential(
    [
        # Convolutional and pooling layers
        layers.Conv2D(32, input_shape=(RESO, RESO, 3), padding="same", kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(32, kernel_size=(3, 3), padding="same", activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), padding="same", activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), padding="same", activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), padding="same", activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(128, kernel_size=(3, 3), padding="same", activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten and dense layers
        layers.Flatten(),
        layers.Dropout(0.5),  # Dropout to reduce overfitting
        layers.Dense(128, activation="relu"),  # Fully connected layer with 128 neurons
        layers.Dropout(0.5),
        layers.Dense(8, activation="softmax"),  # 8 output classes (A+, A-, B+, B-, AB+, AB-, O+, O-)
    ]
)

# Compile the model
model.compile(
    optimizer="adam",  # You can use Adam optimizer for faster convergence
    loss="categorical_crossentropy",  # Categorical crossentropy for multi-class classification
    metrics=["accuracy"],  # Track accuracy during training
)

history = model.fit(train_images, train_labels, epochs=5, batch_size=32,
                    validation_data=(val_images, val_labels))

model.save("test1.h5")

# Print the model summary
model.summary()

print("Model saved successfully as 'test1.h5'")
