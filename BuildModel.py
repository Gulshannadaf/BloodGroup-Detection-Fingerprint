import os
import cv2
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split

from tensorflow import keras
from keras import layers, models
#from keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.utils import img_to_array, load_img
from keras.utils import to_categorical

IMG_WIDTH = 96
IMG_HEIGHT = 103
CLACHE_CLIP_LIMIT = 2.0
CLACHE_TILE_GRID_SIZE = 4
ALPHA = 2.5
BETA = 0
NUM_CLASSES = 8
EPOCHS = 5

dataset_path = "Data/"

def load_images_from_folder(folder):
    images = []
    labels = []
    for label, subfolder in enumerate(["A-", "A+", "AB-", "AB+", "B-", "B+","O-", "O+"]):
        subfolder_path = os.path.join(folder, subfolder)
        for filename in os.listdir(subfolder_path):
            img = cv2.imread(os.path.join(subfolder_path, filename))
            img = img[:, :, :3]  # converting RGBA to RGB
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = np.expand_dims(img, axis=-1)
            clahe = cv2.createCLAHE(clipLimit=CLACHE_CLIP_LIMIT, tileGridSize=(CLACHE_TILE_GRID_SIZE, CLACHE_TILE_GRID_SIZE))
            img = clahe.apply(img)

            img = cv2.convertScaleAbs(img, alpha=ALPHA, beta=BETA) # Making image more contrast by changin alpha and beta

            img = Image.fromarray(img)  
            img = np.array(img)
            images.append(img)
            labels.append(label)
    return np.array(images), np.array(labels)

images, labels = load_images_from_folder(dataset_path)

images = images.astype('float32') / 255.0

labels = to_categorical(labels)

train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size=0.2, random_state=42)
# print(f"First image shape: {images.shape}")
# Define the model architecture
model = models.Sequential(
    [
        # Convolutional and pooling layers
        #layers.Conv2D(32, input_shape=(RESO, RESO), padding="same", kernel_size=(3, 3), activation="relu"),
        layers.Conv2D(32, input_shape=(IMG_HEIGHT, IMG_WIDTH ,1 ), padding="same", kernel_size=(3, 3), activation="relu"),
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
        layers.Dense(NUM_CLASSES, activation="softmax"),  # 8 output classes (A+, A-, B+, B-, AB+, AB-, O+, O-)
    ]
)

# Compile the model
model.compile(
    optimizer="adam",  # You can use Adam optimizer for faster convergence
    loss="categorical_crossentropy",  # Categorical crossentropy for multi-class classification
    metrics=["accuracy"],  # Track accuracy during training
)

history = model.fit(train_images, train_labels, epochs=EPOCHS, batch_size=64, validation_data=(val_images, val_labels))

model.save(f"test-{EPOCHS}-epochs.h5")

# Print the model summary
model.summary()

print("Model saved successfully as 'Bloodgroup-detect.h5'")
